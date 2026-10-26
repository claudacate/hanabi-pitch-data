# Korean pronunciation lists (표준국어대사전, 한국어기초사전)

Three word lists the Hanabi app uses so its Korean pronunciation rules match the dictionary where rules alone
get it wrong. Published here as their CC BY-SA licence asks.

## Files

| File | What it is | Lines | SHA-256 |
|---|---|---|---|
| `no-n-insertion.tsv` | Word-part pairs that add **no** ㄴ sound at the join (금-요일 [그묘일], 첫-인상 [처딘상]): first part, second part. | 1,444 | `e781b6234c5b5ec4475c0dda58ad1369bbabacb9186e8271f8e8be2967c8d06d` |
| `adds-n-insertion.tsv` | Words that **do** add ㄴ at a join (눈-요기 [눈뇨기], 장염 [장념]): word, syllables before the join. | 2,000 | `1cbba1b011fb857fbab1a44e1d1e042d11f2999c9a5cded50e1c0ec87a6122ea` |
| `tensed-words.tsv` | Nouns with a plain consonant said tense where no rule predicts it (창가 [창까], 치과 [치꽈]): word, index of that syllable. | 13,865 | `6a72c80611bd030d95eb50477e94c1a18cbf4536e2341214cc0d2c3b21ca5544` |
| `build_no_n.py` | The script that makes all three from the dictionaries' XML. | | |
| `LICENSE` | Creative Commons 저작자표시-동일조건변경허락 2.0 대한민국 (CC BY-SA 2.0 KR), full text. | | |

## Source and credit

**표준국어대사전** (Standard Korean Language Dictionary) and **한국어기초사전** (Basic Korean Dictionary),
**국립국어원** (National Institute of Korean Language), https://stdict.korean.go.kr/ and https://krdict.korean.go.kr/,
licensed CC BY-SA 2.0 KR. Taken from the XML downloads as mirrored at
https://github.com/spellcheck-ko/korean-dict-nikl, folders `stdict/` (data dated 2026-06-05) and `krdict/`,
commit `42c0d01889f34536e9cf94fe57f62bd2055b1bde`.

## Changes from the source

- Kept only what each list needs (word, part pairs, syllable positions). Meanings, examples and every other
  field were dropped.
- **ㄴ lists:** joins from 표준's "-" marks where the first part ends in a consonant and the second starts with
  이/야/여/요/유. A pair goes in the no-ㄴ list only when every word and pronunciation with it adds no ㄴ. 51 pairs
  listed both ways were left out, and so were second parts 이/이다 (suffixes).
- **Tensed nouns:** 표준 nouns whose pronunciation tenses ㄱㄷㅂㅅㅈ after a vowel or ㄴ/ㄹ/ㅁ/ㅇ.
- **Agreement:** a word is kept only when every entry with that spelling agrees. When homographs disagree
  (인기 人氣 [인끼] vs 人器 [인기]), the entries with a learner level in 한국어기초사전 decide. That dictionary lists only
  common words. Entries with no pronunciation are ignored.

## Rebuild

```
python3 -I build_no_n.py <path to the mirror's stdict folder> <path to the mirror's krdict folder>
```

The script checks the SHA-256 of both folders' XML files before it writes anything. (In the Hanabi source tree it
writes to the app's resources folder; edit `OUT` at the top to write somewhere else.)

## Licence

The lists are licensed under CC BY-SA 2.0 KR (see `LICENSE`). If you share a changed version, it must use the same
licence (or a later version of it), credit 국립국어원 as above, and say what you changed.
