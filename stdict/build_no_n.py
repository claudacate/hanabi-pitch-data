"""Builds HanabiCore's list of word joins where standard Korean adds no ㄴ (금-요일 [그묘일], 첫-인상 [처딘상]).

Usage: python3 -I tools/ko-dic/build_no_n.py <stdict folder>
Source: 표준국어대사전 (National Institute of Korean Language, CC BY-SA 2.0 KR) XML as mirrored at
github.com/spellcheck-ko/korean-dict-nikl, folder stdict/, commit 42c0d01889f34536e9cf94fe57f62bd2055b1bde
(data dated 2026-06-05); SHA-256 of the 88 XML files joined in name order checked below.

The dictionary marks word parts with "-" and gives each word's pronunciation. A join counts when the first
part ends in a consonant and the second starts with 이/야/여/요/유 (where mecab-ko-dic hints make Hanabi add
ㄴ); it is an ㄴ join when the pronunciation keeps the first syllable's final sound and starts the next with
ㄴ/ㄹ (색-연필 [생년필]), otherwise not. Writes Resources/stdict/no-n-insertion.tsv: first part, second part,
for every part pair that never takes ㄴ in any word or listed pronunciation. Second parts 이/이다 (suffixes) are
left out. The output stays CC BY-SA (2.0 KR or later).
"""
import collections
import hashlib
import os
import re
import sys
import xml.etree.ElementTree as ET

SHA = "18db8741d78dfb40fefee86c0d6c6192ebabc496dcb162065fde60c4fa21325e"
OUT = os.path.join(os.path.dirname(__file__), "../../Packages/HanabiCore/Sources/HanabiCore/Resources/stdict")

def hangul(s): return all(0xAC00 <= ord(c) <= 0xD7A3 for c in s)
def coda(c): return (ord(c) - 0xAC00) % 28
def onset(c): return (ord(c) - 0xAC00) // 588
def vowel(c): return (ord(c) - 0xAC00) % 588 // 28
IEUNG, NIEUN, RIEUL = 11, 2, 5
I_VOWELS = {20, 2, 6, 12, 17}  # ㅣ ㅑ ㅕ ㅛ ㅠ

folder = sys.argv[1]
files = sorted(f for f in os.listdir(folder) if f.endswith(".xml"))
digest = hashlib.sha256()
for f in files:
    digest.update(open(os.path.join(folder, f), "rb").read())
if digest.hexdigest() != SHA:
    sys.exit("stdict XML does not match the pinned SHA-256: " + digest.hexdigest())

seen = collections.defaultdict(set)  # (first, second) → {True (ㄴ), False (no ㄴ)}
for f in files:
    for _, item in ET.iterparse(os.path.join(folder, f)):
        if item.tag != "item":
            continue
        info = item.find("word_info")
        word = (info.findtext("word") or "").strip() if info is not None else ""
        parts = word.split("-")
        if len(parts) > 1 and all(p and hangul(p) for p in parts):
            plain = "".join(parts)
            prons = [re.sub(r"[:ː]", "", p.findtext("pronunciation") or "").strip()
                     for p in info.findall("pronunciation_info")]
            prons = [p for p in prons if hangul(p) and len(p) == len(plain)]
            at = 0
            for a, b in zip(parts, parts[1:]):
                at += len(a)
                if coda(a[-1]) and onset(b[0]) == IEUNG and vowel(b[0]) in I_VOWELS and b not in ("이", "이다"):
                    for p in prons:
                        seen[(a, b)].add(coda(p[at - 1]) != 0 and onset(p[at]) in (NIEUN, RIEUL))
        item.clear()

pairs = sorted(k for k, v in seen.items() if v == {False})
os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "no-n-insertion.tsv"), "w", encoding="utf-8") as out:
    out.writelines(f"{a}\t{b}\n" for a, b in pairs)
print(len(pairs), "no-ㄴ pairs;", sum(v == {True} for v in seen.values()), "ㄴ pairs;",
      sum(len(v) == 2 for v in seen.values()), "both (left out)")
