"""Builds HanabiCore's pitch-accent table from Kanjium's accents.txt (CC BY-SA 4.0).

Usage: python3 -I tools/pitch-data/build.py <accents.txt>
Source: github.com/mifunetoshiro/kanjium data/source_files/raw/accents.txt, commit
685d4d723d6d20bf9beb169103aeac188eb067ad (2024-06-16), SHA-256 checked below.

Writes Resources/pitch/accents.tsv: word, reading (hiragana), accent numbers (comma-separated).
Changes from the source: part-of-speech labels such as "(副)" are dropped (numbers kept in order),
katakana readings are written in hiragana, lines are sorted by word. For words written in kana (ある,
ここ), lines keyed by the reading are added when every entry with that reading has the same accent
(有る/在る ある 1 → ある ある 1; いる is left out: 居る 0, 射る 1). The output stays CC BY-SA 4.0.
"""
import hashlib
import os
import re
import sys

SHA = "8bd0dd127dab32ceec94cb03ab1ba6b68858ea73421dfa1731af2f373deb4f20"
OUT = os.path.join(os.path.dirname(__file__), "../../Packages/HanabiCore/Sources/HanabiCore/Resources/pitch")

def hiragana(s): return "".join(chr(ord(c) - 0x60) if 0x30A1 <= ord(c) <= 0x30F6 else c for c in s)

data = open(sys.argv[1], "rb").read()
if hashlib.sha256(data).hexdigest() != SHA:
    sys.exit("accents.txt does not match the pinned SHA-256")
rows = set()
for line in data.decode("utf-8").splitlines():
    parts = line.split("\t")
    if len(parts) != 3:
        continue
    numbers = re.findall(r"\d+", parts[2])
    if parts[0] and parts[1] and numbers:
        rows.add((parts[0], hiragana(parts[1]), ",".join(dict.fromkeys(numbers))))
by_kana = {}
for w, k, a in rows:
    by_kana.setdefault(k, set()).add(a.split(",")[0])
words = {w for w, _, _ in rows}
for k, accents in by_kana.items():
    if len(accents) == 1 and k not in words:
        rows.add((k, k, accents.pop()))
os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "accents.tsv"), "w", encoding="utf-8") as f:
    f.writelines(f"{w}\t{k}\t{a}\n" for w, k, a in sorted(rows, key=lambda r: (r[0].encode(), r[1])))
print(len(rows), "entries")
