import re
import fitz  # PyMuPDF

print("[+] Starting Salt Discovery Analysis")
pdf_path = "Lab 6 - Salted Hashes (1).pdf"

# -----------------------------
# Step 1: Extract text from PDF
# -----------------------------
try:
    doc = fitz.open(pdf_path)
    print(f"[+] PDF opened successfully. Total pages: {doc.page_count}")
except Exception as e:
    print(f"[!] Failed to open PDF: {e}")
    exit()

full_text = ""
for i, page in enumerate(doc, start=1):
    full_text += page.get_text("text")
    print(f"    - Extracted text from page {i}")
doc.close()

# -----------------------------
# Step 2: Analyze text
# -----------------------------
lines = [line.strip() for line in full_text.splitlines() if line.strip()]
print(f"[+] Total text lines to analyze: {len(lines)}")

salt_candidates = set()

for line in lines:
    # Detect unusual standalone words or tokens
    if len(line.split()) == 1 and len(line) > 3:
        if not line.lower().startswith(("secure", "communication", "overview", "lab", "task")):
            salt_candidates.add(line)

    # Detect words containing special symbols like '.' or '-' that look out of place
    if re.search(r"[A-Za-z0-9]+[.\-@][A-Za-z0-9]+", line):
        salt_candidates.add(line)

# -----------------------------
# Step 3: Print findings
# -----------------------------
if salt_candidates:
    print("\n[***] Potential salt-like candidates discovered:")
    for item in salt_candidates:
        print(f"     → {item}")
else:
    print("[!] No unusual patterns found — manual inspection required.")
