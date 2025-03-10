#!/usr/bin/env python3
from pwn import *
import binascii

# Imposta HOST e PORT secondo il target reale
HOST = "spg.challs.territoriali.olicyber.it"
PORT = 38002

def cbc_bitflip(prev_block, pos, orig_byte, target_byte):
    """
    Modifica il byte in prev_block in posizione pos per far
    variare il byte decriptato corrispondente da orig_byte a target_byte.
    """
    delta = orig_byte ^ target_byte
    prev_block[pos] ^= delta

def get_token(conn, username):
    conn.recvuntil(b"> ")
    conn.sendline(b"1")  # Scegli l'opzione 1: Genera passphrase
    conn.recvuntil(b"Username? ")
    conn.sendline(username.encode())
    # Il servizio mostra la passphrase e poi il token
    data = conn.recvuntil(b"Token:")
    token_line = conn.recvline().strip()
    token_hex = token_line.decode().split()[-1]
    log.info("Token originale: " + token_hex)
    return token_hex

def modify_token(token_hex):
    # Il token è: IV || ciphertext, ogni blocco è di 16 byte
    token = bytearray(binascii.unhexlify(token_hex))
    iv = token[:16]
    ciphertext = token[16:]
    
    # Dividi in blocchi (includendo l'IV come blocco 0)
    blocks = [bytearray(iv)]
    for i in range(0, len(ciphertext), 16):
        blocks.append(bytearray(ciphertext[i:i+16]))
    
    log.info("Blocchi originali:")
    for i, blk in enumerate(blocks):
        log.info("Blocco {}: {}".format(i, binascii.hexlify(blk).decode()))
    
    # Supponiamo che, per username "AAA", il token decriptato sia simile a:
    # "username=AAA;index0=12;index1=17;index2=11;index3=19"
    # E ipotizziamo che questi campi siano nel blocco 2 (terzo blocco).
    # In modalità CBC, per modificare il blocco 2 bisogna agire sul blocco 1.
    #
    # Esempio di offset ipotetici (da determinare sperimentalmente):
    fields = {
        0: {"block": 2, "offset": 3,  "current": b"12", "target": b"00"},
        1: {"block": 2, "offset": 11, "current": b"17", "target": b"01"},
        2: {"block": 2, "offset": 19, "current": b"11", "target": b"02"},
        3: {"block": 2, "offset": 27, "current": b"19", "target": b"03"},
    }
    
    # Modifica il blocco precedente (bloc 1) per influenzare il blocco 2
    for idx in fields:
        info = fields[idx]
        target_block = info["block"]
        block_to_modify = blocks[target_block - 1]  # blocco 1 per modificare blocco 2
        for i in range(len(info["current"])):
            pos = info["offset"] + i
            orig = info["current"][i]
            target = info["target"][i]
            log.info(f"Modifica index{idx} - pos {pos}: {hex(block_to_modify[pos])} -> ", end="")
            cbc_bitflip(block_to_modify, pos, orig, target)
            log.info(hex(block_to_modify[pos]))
    
    # Ricostruisci il token modificato
    new_iv = bytes(blocks[0])
    new_ciphertext = b"".join(bytes(b) for b in blocks[1:])
    modified_token = new_iv + new_ciphertext
    modified_token_hex = binascii.hexlify(modified_token).decode()
    log.info("Token modificato: " + modified_token_hex)
    return modified_token_hex

def recover_token(conn, modified_token_hex):
    conn.recvuntil(b"> ")
    conn.sendline(b"2")  # Scegli l'opzione 2: Recupera passphrase
    conn.recvuntil(b"Token? ")
    conn.sendline(modified_token_hex.encode())
    result = conn.recvline(timeout=2)
    return result

def main():
    # Connessione al servizio
    conn = remote(HOST, PORT)
    conn.recvuntil(b"> ")
    
    # Step 1: Registrazione e ottenimento del token
    username = "AAA"  # puoi usare "AAA" come nell'esempio
    token_hex = get_token(conn, username)
    
    # Step 2: Modifica del token tramite bit-flipping
    modified_token_hex = modify_token(token_hex)
    
    # Step 3: Invio del token modificato per recuperare la passphrase (e quindi la flag)
    result = recover_token(conn, modified_token_hex)
    log.success("Risultato della recovery: " + result.decode())
    
    conn.close()

if __name__ == "__main__":
    main()
