# Korean no-ㄴ word joins (표준국어대사전)

Word-part pairs where standard Korean adds **no** ㄴ sound at the join, though the sounds around it
would allow one (금-요일 [그묘일], 첫-인상 [처딘상]). The Hanabi app uses it so its pronunciation
rules do not add a wrong ㄴ. Published here as its CC BY-SA licence asks.

## Files

| File | What it is |
|---|---|
| `no-n-insertion.tsv` | One line per pair: first part, second part. 1,391 lines. |
| `build_no_n.py` | The script that makes the list from the dictionary's XML. |
| `LICENSE` | Creative Commons 저작자표시-동일조건변경허락 2.0 대한민국 (CC BY-SA 2.0 KR), full text. |

SHA-256 of `no-n-insertion.tsv`: `2ef756d7aaf97743ad39591a377fb3709162aee7ab555958f6a9ae36932297eb`

## Source and credit

**표준국어대사전** (Standard Korean Language Dictionary), **국립국어원** (National Institute of Korean
Language), https://stdict.korean.go.kr/, licensed CC BY-SA 2.0 KR.
Taken from the XML download as mirrored at https://github.com/spellcheck-ko/korean-dict-nikl,
folder `stdict/`, commit `42c0d01889f34536e9cf94fe57f62bd2055b1bde` (data dated 2026-06-05).

## Changes from the source

- Kept only word-part pairs from the dictionary's "-" marks where the first part ends in a consonant
  and the second starts with 이/야/여/요/유.
- Kept a pair only when every word and every listed pronunciation with it adds no ㄴ. 48 pairs listed
  both ways were left out, and so were second parts 이/이다 (suffixes).
- Dropped meanings, examples and every other field.

## Rebuild

```
python3 -I build_no_n.py <path to the mirror's stdict folder>
```

The script checks the SHA-256 of the 88 XML files before it writes anything. (In the Hanabi source tree
it writes to the app's resources folder; edit `OUT` at the top to write somewhere else.)

## Licence

`no-n-insertion.tsv` is licensed under CC BY-SA 2.0 KR (see `LICENSE`). If you share a changed version,
it must use the same licence (or a later version of it), credit 국립국어원 as above, and say what you changed.
