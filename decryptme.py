#!/usr/bin/env python3
import string, base64

def step1(s):
    frm = "zyxwvutsrqponZYXWVUTSRQPONmlkjihgfedcbaMLKJIHGFEDCBA"
    to  = "mlkjihgfedcbaMLKJIHGFEDCBAzyxwvutsrqponZYXWVUTSRQPON"
    return s.translate(str.maketrans(frm, to))

def inv_step2(s):
    return base64.b64decode(s).decode("utf-8", errors="replace")

def inv_step3(s, shift=4):
    lower = string.ascii_lowercase
    shifted = lower[shift:] + lower[:shift]
    return s.translate(str.maketrans(shifted, lower))

def decrypt(ct):
    s = ct.strip()
    while s and s[0] in "123":
        op, body = s[0], s[1:]
        if op == "1":
            s = step1(body)          # self-inverse
        elif op == "2":
            s = inv_step2(body)      # base64 decode
        elif op == "3":
            s = inv_step3(body)      # caesar -4
    return s

cipher = input("Paste intercepted message: ").strip()
print("\nDecoded message:\n")
print(decrypt(cipher))
