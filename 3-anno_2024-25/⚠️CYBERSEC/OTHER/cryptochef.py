from chepy import Chepy
ciphertext = "104e137f425954137f74107f525511457f5468134d7f146c4c"

plaintext = Chepy(ciphertext).xor_bruteforce()
#plaintext = "flag{" + str(plaintext) + "}"
print(plaintext)
