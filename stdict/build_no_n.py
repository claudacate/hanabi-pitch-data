"""Builds HanabiCore's lists of word joins where standard Korean adds no ㄴ (금-요일 [그묘일], 첫-인상 [처딘상])
and of whole words that do add one (장-염 [장념], 눈-요기 [눈뇨기]).

Usage: python3 -I tools/ko-dic/build_no_n.py <stdict folder> <krdict folder>
Source: 표준국어대사전 (National Institute of Korean Language, CC BY-SA 2.0 KR) XML as mirrored at
github.com/spellcheck-ko/korean-dict-nikl, folder stdict/, commit 42c0d01889f34536e9cf94fe57f62bd2055b1bde
(data dated 2026-06-05); SHA-256 of the 88 XML files joined in name order checked below.

The dictionary marks word parts with "-" and gives each word's pronunciation. A join counts when the first
part ends in a consonant and the second starts with 이/야/여/요/유 (where mecab-ko-dic hints make Hanabi add
ㄴ); it is an ㄴ join when the pronunciation keeps the first syllable's final sound and starts the next with
ㄴ/ㄹ (색-연필 [생년필]), otherwise not. Writes Resources/stdict/no-n-insertion.tsv: first part, second part,
for every part pair that never takes ㄴ in any word or listed pronunciation. Second parts 이/이다 (suffixes) are
left out. Also writes adds-n-insertion.tsv: word (parts joined), number of syllables before the join, for joins
where every pronunciation of every entry spelled that way adds ㄴ (or, if homographs disagree, every leveled entry in
한국어기초사전 does); Hanabi uses it for words mecab-ko-dic keeps
whole. Also writes tensed-words.tsv: noun, index of a syllable whose plain consonant ㄱㄷㅂㅅㅈ is said tense after a
vowel or ㄴ/ㄹ/ㅁ/ㅇ, where no rule predicts it (창가 [창까], 치과 [치꽈], 일주일 [일쭈일]), kept only when every pronunciation
of every entry with that spelling agrees, or, when 표준 homographs disagree (인기 人氣 [인끼] vs 人器 [인기]), when every
entry with a learner level in 한국어기초사전 (krdict/, same mirror commit, SHA-256 below) agrees: it lists only common words.
Entries with no pronunciation are ignored. The output stays CC BY-SA (2.0 KR or later).
"""
import collections
import hashlib
import os
import re
import sys
import xml.etree.ElementTree as ET

SHA = "18db8741d78dfb40fefee86c0d6c6192ebabc496dcb162065fde60c4fa21325e"
KRDICT_SHA = "294cc3d7ed5fcccae838123a97f3a9eb7e05a63d42767b31391a541c7a9d0c02"
OUT = os.path.join(os.path.dirname(__file__), "../../Packages/HanabiCore/Sources/HanabiCore/Resources/stdict")

def hangul(s): return all(0xAC00 <= ord(c) <= 0xD7A3 for c in s)
def coda(c): return (ord(c) - 0xAC00) % 28
def onset(c): return (ord(c) - 0xAC00) // 588
def vowel(c): return (ord(c) - 0xAC00) % 588 // 28
IEUNG, NIEUN, RIEUL = 11, 2, 5
TENSE = {0: 1, 3: 4, 7: 8, 9: 10, 12: 13}  # onset ㄱㄷㅂㅅㅈ → ㄲㄸㅃㅆㅉ
SONORANT_CODAS = {0, 4, 8, 16, 21}  # none, ㄴ, ㄹ, ㅁ, ㅇ: no rule tenses what follows
I_VOWELS = {20, 2, 6, 12, 17}  # ㅣ ㅑ ㅕ ㅛ ㅠ

def checked(folder, sha, name):
    files = sorted(f for f in os.listdir(folder) if f.endswith(".xml"))
    digest = hashlib.sha256()
    for f in files:
        digest.update(open(os.path.join(folder, f), "rb").read())
    if digest.hexdigest() != sha:
        sys.exit(f"{name} XML does not match the pinned SHA-256: " + digest.hexdigest())
    return files

folder, kr_folder = sys.argv[1], sys.argv[2]
files = checked(folder, SHA, "stdict")
# 한국어기초사전 is not strict XML, so its fields are read by pattern: word → base pronunciations of leveled entries.
learner = collections.defaultdict(set)
feat = lambda name: re.compile(r'<feat att="%s" val="([^"]*)"' % name)
for f in checked(kr_folder, KRDICT_SHA, "krdict"):
    for entry in open(os.path.join(kr_folder, f), encoding="utf-8", errors="replace").read().split("<LexicalEntry")[1:]:
        head = entry.split("<Sense ")[0]
        word, level = feat("writtenForm").search(head), feat("vocabularyLevel").search(head)
        prons = [re.sub(r"[:ː]", "", p) for p in feat("pronunciation").findall(head)]
        if word and level and level.group(1) not in ("없음", "") and prons and len(prons[0]) == len(word.group(1)):
            learner[word.group(1)].add(prons[0])

seen = collections.defaultdict(set)  # (first, second) → {True (ㄴ), False (no ㄴ)}
joins = collections.defaultdict(set)  # word → syllables before each qualifying join
spoken = collections.defaultdict(set)  # word → every listed pronunciation of every entry with that spelling
kinds = collections.defaultdict(set)  # word → parts of speech of its entries
def inserted(p, at): return coda(p[at - 1]) != 0 and onset(p[at]) in (NIEUN, RIEUL)
for f in files:
    for _, item in ET.iterparse(os.path.join(folder, f)):
        if item.tag != "item":
            continue
        info = item.find("word_info")
        # Homographs carry a number (창-가01, 여권01); without stripping it those entries were skipped.
        word = re.sub(r"\d+$", "", (info.findtext("word") or "").strip()) if info is not None else ""
        parts = word.split("-")
        if all(p and hangul(p) for p in parts):
            plain = "".join(parts)
            prons = [re.sub(r"[:ː]", "", p.findtext("pronunciation") or "").strip()
                     for p in info.findall("pronunciation_info")]
            prons = [p for p in prons if hangul(p) and len(p) == len(plain)]
            spoken[plain].update(prons)
            if prons:
                kinds[plain].add(item.findtext(".//pos") or "")
            at = 0
            for a, b in zip(parts, parts[1:]):
                at += len(a)
                if coda(a[-1]) and onset(b[0]) == IEUNG and vowel(b[0]) in I_VOWELS:
                    joins[plain].add(at)
                    if b not in ("이", "이다"):
                        for p in prons:
                            seen[(a, b)].add(inserted(p, at))
        item.clear()

pairs = sorted(k for k, v in seen.items() if v == {False})
os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "no-n-insertion.tsv"), "w", encoding="utf-8") as out:
    out.writelines(f"{a}\t{b}\n" for a, b in pairs)
def adds_at(w, at):
    # Homographs that disagree (장염 腸炎 [장념] vs 長髥 [장염]) are settled by the learner dictionary, as for tensing.
    said = spoken[w] if len({inserted(p, at) for p in spoken[w]}) == 1 else learner.get(w, set())
    return bool(said) and all(hangul(p) and len(p) == len(w) and inserted(p, at) for p in said)
words = sorted((w, at) for w, ats in joins.items() for at in ats if adds_at(w, at))
with open(os.path.join(OUT, "adds-n-insertion.tsv"), "w", encoding="utf-8") as out:
    out.writelines(f"{w}\t{at}\n" for w, at in words)
def tensed_at(w, j):
    said = spoken[w] if len({onset(p[j]) for p in spoken[w]}) == 1 else learner.get(w, set())
    return bool(said) and all(hangul(p) and len(p) == len(w) and onset(p[j]) == TENSE[onset(w[j])] for p in said)
tensed = sorted((w, j) for w in spoken if spoken[w] and kinds[w] <= {"명사", "의존 명사"}
                for j in range(1, len(w)) if onset(w[j]) in TENSE and coda(w[j - 1]) in SONORANT_CODAS and tensed_at(w, j))
with open(os.path.join(OUT, "tensed-words.tsv"), "w", encoding="utf-8") as out:
    out.writelines(f"{w}\t{j}\n" for w, j in tensed)
print(len(tensed), "tensed nouns;", len(words), "adds-ㄴ words;", len(pairs), "no-ㄴ pairs;", sum(v == {True} for v in seen.values()), "ㄴ pairs;",
      sum(len(v) == 2 for v in seen.values()), "both (left out)")
