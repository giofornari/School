#!/usr/bin/env python3
import os
import sys
import binascii
import string

# The SBOX used in the encryption.
SBOX = [23, 46, 93, 178, 209, 80, 169, 227, 246, 14, 79, 139, 196, 109, 176, 76,
        188, 74, 163, 187, 130, 110, 101, 241, 202, 239, 53, 117, 114, 72, 131, 217,
        71, 55, 253, 45, 212, 191, 59, 30, 104, 190, 251, 20, 94, 211, 84, 85, 68,
        73, 237, 205, 174, 97, 197, 199, 36, 180, 100, 215, 107, 62, 89, 81, 111, 119,
        32, 156, 214, 88, 183, 238, 18, 125, 231, 92, 127, 219, 138, 193, 141, 103,
        37, 236, 157, 41, 158, 135, 120, 9, 250, 172, 106, 136, 2, 123, 247, 248,
        26, 52, 54, 57, 204, 232, 7, 15, 140, 66, 245, 170, 144, 22, 203, 1, 56,
        167, 34, 244, 137, 19, 225, 143, 6, 184, 10, 60, 151, 165, 91, 40, 133, 70,
        128, 121, 220, 16, 152, 13, 58, 185, 254, 154, 198, 113, 160, 132, 206, 50,
        122, 116, 192, 179, 153, 47, 95, 200, 112, 145, 5, 126, 105, 243, 164, 181,
        146, 161, 129, 3, 48, 182, 189, 33, 148, 162, 69, 43, 234, 35, 39, 63, 150,
        142, 61, 90, 64, 78, 42, 83, 21, 155, 168, 229, 96, 173, 208, 207, 221, 82,
        242, 240, 27, 4, 186, 115, 17, 51, 159, 175, 75, 201, 44, 29, 218, 216, 108,
        8, 99, 28, 102, 118, 24, 230, 195, 86, 226, 166, 11, 0, 171, 65, 228, 38,
        223, 31, 67, 77, 49, 194, 124, 249, 222, 177, 252, 98, 235, 12, 210, 134,
        233, 87, 255, 147, 149, 213, 25, 224]

# Build the inverse SBOX mapping
INV_SBOX = [0] * 256
for i, val in enumerate(SBOX):
    INV_SBOX[val] = i

def xor_bytes(data: bytes, key: bytes) -> bytes:
    """XOR data with a repeating key."""
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

def decrypt(ciphertext: bytes, candidate_key: bytes) -> bytes:
    """
    Reverse the encryption:
       1. XOR the ciphertext with candidate_key.
       2. Apply the inverse SBOX substitution.
    """
    xored = xor_bytes(ciphertext, candidate_key)
    # Reverse the SBOX substitution
    return bytes(INV_SBOX[b] for b in xored)

def score_text(text: bytes) -> float:
    """
    Score a candidate plaintext based on character frequency and printability.
    Higher score means text is more likely to be valid ASCII.
    """
    score = 0
    for b in text:
        # Give a bonus if b is a common printable character
        if 32 <= b <= 126:
            score += 1
            # Extra bonus for common letters and space
            if chr(b) in string.ascii_letters + " ":
                score += 1
        else:
            # Penalize non-printable characters heavily
            score -= 5
    return score

def break_repeating_xor(ciphertext: bytes) -> (bytes, bytes):
    """
    Try key lengths from 6 to 12.
    For each key length, solve each key byte independently.
    Return the candidate key and the corresponding decrypted plaintext that
    scores best and contains a '|' (expected delimiter).
    """
    best_score = float('-inf')
    best_plaintext = None
    best_key = None
    for key_len in range(6, 13):
        candidate_key = bytearray(key_len)
        # For each key byte position, solve using frequency analysis on the corresponding bytes.
        for i in range(key_len):
            # Gather all ciphertext bytes that were XOR-ed with the same key byte.
            block = ciphertext[i::key_len]
            best_key_score = float('-inf')
            best_key_byte = 0
            # Try every possible byte for this key position.
            for candidate in range(256):
                # For each ciphertext byte, undo the XOR with candidate and then the SBOX substitution.
                # That is, candidate plaintext byte = INV_SBOX[c ^ candidate]
                trial_bytes = bytes(INV_SBOX[b ^ candidate] for b in block)
                current_score = score_text(trial_bytes)
                if current_score > best_key_score:
                    best_key_score = current_score
                    best_key_byte = candidate
            candidate_key[i] = best_key_byte
        # Decrypt entire ciphertext with candidate_key.
        plaintext = decrypt(ciphertext, candidate_key)
        current_score = score_text(plaintext)
        # We expect a '|' character in the plaintext.
        if b"|" not in plaintext:
            current_score -= 100  # harsh penalty if missing delimiter
        if current_score > best_score:
            best_score = current_score
            best_plaintext = plaintext
            best_key = bytes(candidate_key)
    return best_key, best_plaintext

def main():
    filename = "/home/user/schoolproject3B/CYBERSEC/territoriale/crypto/again_output.txt"

    
    # Read the ciphertext hex string from the file.
    with open(filename, "r") as f:
        ciphertext_hex = f.read().strip()
    
    try:
        ciphertext = binascii.unhexlify(ciphertext_hex)
    except Exception as e:
        print("[-] Failed to decode hex from file.")
        sys.exit(1)
    
    print("[*] Attempting to break the encryption...")
    candidate_key, plaintext = break_repeating_xor(ciphertext)
    
    print("\n[*] Candidate key (hex):", candidate_key.hex())
    try:
        decoded = plaintext.decode()
    except UnicodeDecodeError:
        decoded = plaintext.hex()
    print("[*] Decrypted plaintext:")
    print(decoded)
    
    # Expect plaintext of the form: flag_part1 + "|" + flag_part2
    if b"|" in plaintext:
        parts = plaintext.split(b"|", 1)
        flag_part2 = parts[1].strip()
        try:
            flag_text = flag_part2.decode()
        except UnicodeDecodeError:
            flag_text = flag_part2.hex()
        print("\n[+] Recovered flag:")
        print("flag{" + flag_text + "}")
    else:
        print("[-] Decrypted text does not contain the expected delimiter '|'.")

if __name__ == "__main__":
    main()
