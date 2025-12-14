import struct
import binascii

enc = open("flag.enc","rb").read()

PNG = bytes([0x89,0x50,0x4E,0x47,0x0D,0x0A,0x1A,0x0A])
ks = [enc[i] ^ PNG[i] for i in range(8)]

def lfsr(seed, length, taps, nbytes):
    state = seed
    out = []
    for _ in range(nbytes):
        b = 0
        for i in range(8):
            bit = state & 1
            b |= bit << i
            fb = 0
            for t in taps:
                fb ^= (state >> (length - t)) & 1
            state = (state >> 1) | (fb << (length - 1))
        out.append(b)
    return out

# -----------------------------
# Precompute ALL Register-2 outputs
# -----------------------------
print("[*] Building Register-2 lookup table...")

r2_table = {}
for seed2 in range(1, 2**19):
    out = tuple(lfsr(seed2, 19, [5,11], 8))
    r2_table[out] = seed2

print("[+] Register-2 table built")

# -----------------------------
# Brute-force Register-1
# -----------------------------
print("[*] Brute-forcing Register-1...")

for seed1 in range(1, 2**12):
    r1 = lfsr(seed1, 12, [2,7], 8)
    needed = tuple((ks[i] - r1[i]) % 255 for i in range(8))

    if needed in r2_table:
        seed2 = r2_table[needed]
        print("[+] Keys found!")
        print("R1 seed:", seed1)
        print("R2 seed:", seed2)

        r1f = lfsr(seed1, 12, [2,7], len(enc))
        r2f = lfsr(seed2, 19, [5,11], len(enc))
        plain = bytes(enc[i] ^ ((r1f[i] + r2f[i]) % 255) for i in range(len(enc)))

        # Validate PNG
        if plain[:8] == PNG:
            crc = struct.unpack(">I", plain[29:33])[0]
            calc = binascii.crc32(b'IHDR' + plain[16:29]) & 0xffffffff
            if crc == calc:
                open("recovered.png","wb").write(plain)
                print("[+] recovered.png written")
                break
