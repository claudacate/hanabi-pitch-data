# Hanabi pitch-accent data

The Japanese pitch-accent table used by the Hanabi app, published here as its
CC BY-SA 4.0 licence requires.

The `stdict/` folder holds a separate Korean word list from 표준국어대사전 under its own licence
(CC BY-SA 2.0 KR); see `stdict/README.md`. The files below are only the pitch-accent data.

## Files

| File | What it is |
|---|---|
| `accents.tsv` | One line per word: word, reading (hiragana), accent numbers (comma-separated). 174,287 lines. |
| `build.py` | The script that makes `accents.tsv` from Kanjium's `accents.txt`. |
| `LICENSE` | Creative Commons Attribution-ShareAlike 4.0 International, full text. |

SHA-256 of `accents.tsv`: `a536806540f1d353cba948b275cc3a1309694c2ae562edc02bba92cdaef3ee9c`

## Source and credit

Pitch-accent data: **Kanjium** by mifunetoshiro, https://github.com/mifunetoshiro/kanjium,
file `data/source_files/raw/accents.txt`, commit `685d4d723d6d20bf9beb169103aeac188eb067ad`
(2024-06-16), licensed CC BY-SA 4.0.

Kanjium's README: "The pitch accent notation, verb particle data, phonetics, homonyms and other
additions or modifications to EDICT, KANJIDIC or KRADFILE were provided by Uros O. through his free
database." Most of Kanjium's word data comes from the Electronic Dictionary Research and Development
Group (EDRDG), used under the EDRDG licence (https://www.edrdg.org/edrdg/licence.html).

## Changes from the source

- Kept the word, reading and accent numbers only (part-of-speech labels such as "(副)" removed;
  numbers kept in order, duplicates dropped).
- Wrote katakana readings in hiragana.
- Added lines keyed by the reading for words written in kana, when every entry with that reading has
  the same accent (有る/在る ある 1 → ある ある 1; いる is left out: 居る 0, 射る 1).
- Sorted the lines by word.

## Rebuild

```
python3 -I build.py <path to Kanjium accents.txt>
```

The script checks the input's SHA-256 before it writes anything. (In the Hanabi source tree it writes
to the app's resources folder; edit `OUT` at the top to write somewhere else.)

## Licence

`accents.tsv` is licensed under CC BY-SA 4.0 (see `LICENSE`). If you share a changed version, it must
use the same licence, credit Kanjium as above, and say what you changed.
