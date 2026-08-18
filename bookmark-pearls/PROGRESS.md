# Bookmark → Pearl Conversion — Progress

**Sources (two rounds):**
- **Round 1** — `source/my-bookmarks-2026-08-14.json` — 3,275 bookmarked MCQs → 105 batches
- **Round 2** — `source/all_bookmarks_converted.json` — 898 MCQs, of which **866 were new**
  (32 duplicated round-1 questions and were dropped up front) → 31 batches

**Checked against:** `source/pearls-clean.json` (810 existing pearls) + the 21 consolidated `.md` files in the parent folder
**Output:** 19 subject files in this folder (`bookmark-pearls/`), separate from the existing pearl collection

## Settings (confirmed with user)
- Retention target: **~40%** of questions become pearls
- Filing: **by content**, not by the bookmark's subject tag (mis-tagged questions are re-routed)
- Anything already covered by an existing pearl is dropped
- **Format: the house structure below — matches the existing pearl files, NOT the terse PEARL/TRAP form**

## Pearl format (mandatory — every pearl)

```
## Title

**PEARL:** The single core fact, stated flatly. Bold the words that matter.

**UNDERSTAND:** Why it is so — the mechanism or logic that makes the fact
inevitable rather than arbitrary. (Omit only when the fact is pure convention.)

**MUST KNOW:**
- 3–5 bullets of the associated high-yield material: related numbers, the
  differential, the classic associations, clinical application.
- Drawn from the question's explanation AND from wider knowledge of what
  NEET-PG / INI-CET actually ask around this topic.

**EXAM CONNECTION:** How the point is actually asked — the stem shape, the
"all EXCEPT" answer, the intended distractor.

**REMEMBER:** *One-line memory hook, in italics.*

`Q<id>, Q<id>`   ← source bookmark IDs; merged duplicates list all
```

Optional blocks: **IMAGE:** (with the original URL) when the visual itself is
the learning point; **TRAP:**/**CUTOFF:** where a separate call-out helps.

## Round 1 — batches completed 105 / 105 ✅ COMPLETE

| Subject | Batches done | Total batches |
|---|---|---|
| Anatomy | 8 | 8 ✅ |
| Anesthesia | 3 | 3 ✅ |
| Biochemistry | 6 | 6 ✅ |
| Dermatology | 4 | 4 ✅ |
| ENT | 2 | 2 ✅ |
| Forensic Medicine | 2 | 2 ✅ |
| Medicine | 6 | 6 ✅ |
| Microbiology | 6 | 6 ✅ |
| OBG | 8 | 8 ✅ |
| Ophthalmology | 3 | 3 ✅ |
| Orthopedics | 3 | 3 ✅ |
| PSM | 3 | 3 ✅ |
| Paediatrics | 7 | 7 ✅ |
| Pathology | 4 | 4 ✅ |
| Pharmacology | 4 | 4 ✅ |
| Physiology | 4 | 4 ✅ |
| Psychiatry | 5 | 5 ✅ |
| Radiology | 5 | 5 ✅ |
| Surgery | 5 | 5 ✅ |
| UNSORTED (General / Mid-Day) | 17 | 17 ✅ |

*(Pearls are filed under the subject they belong to, so the Anatomy and Anesthesia
batches also contributed pearls to Microbiology, OBG, Surgery, Ophthalmology,
Paediatrics, ENT, Dermatology, Pharmacology and Medicine.)*

## Round 2 — batches completed 31 / 31 ✅ COMPLETE

866 new questions, no UNSORTED bucket (every question mapped to one of the 19
subjects). Round-2 part files are named `<Subject>-z<nn>.md` so they sort **after**
all round-1 parts and append cleanly to the end of each subject file.

| Subject | Batches | | Subject | Batches |
|---|---|---|---|---|
| Anatomy | 1 ✅ | | Paediatrics | 2 ✅ |
| Anesthesia | 1 ✅ | | Pathology | 3 ✅ |
| Biochemistry | 2 ✅ | | Pharmacology | 2 ✅ |
| Dermatology | 1 ✅ | | Physiology | 1 ✅ |
| ENT | 1 ✅ | | PSM | 3 ✅ |
| Forensic Medicine | 1 ✅ | | Psychiatry | 1 ✅ |
| Medicine | 2 ✅ | | Radiology | 1 ✅ |
| Microbiology | 2 ✅ | | Surgery | 2 ✅ |
| OBG | 2 ✅ | | Ophthalmology | 1 ✅ |
| Orthopedics | 2 ✅ | | | |

## Pearl count — 1,961 (1,572 round 1 + 389 round 2)

| Subject | Round 1 | Round 2 | Total |
|---|---|---|---|
| OBG | 176 | +22 | 198 |
| Medicine | 154 | +33 | 187 |
| Biochemistry | 123 | +29 | 152 |
| Microbiology | 131 | +21 | 152 |
| Paediatrics | 125 | +21 | 146 |
| Anatomy | 114 | +15 | 129 |
| Pharmacology | 77 | +27 | 104 |
| Surgery | 80 | +24 | 104 |
| Orthopedics | 70 | +23 | 93 |
| Pathology | 51 | +40 | 91 |
| Ophthalmology | 74 | +15 | 89 |
| Dermatology | 66 | +15 | 81 |
| PSM | 51 | +26 | 77 |
| Radiology | 51 | +14 | 65 |
| Physiology | 52 | +12 | 64 |
| Anesthesia | 48 | +15 | 63 |
| Forensic Medicine | 46 | +12 | 58 |
| Psychiatry | 44 | +11 | 55 |
| ENT | 39 | +14 | 53 |

Round-2 retention was **~45%** (389 pearls from 866 questions) — slightly above the
40% target because this was a fresh question bank with less internal duplication,
though a substantial fraction of each batch was still dropped as already covered
by round-1 pearls.

## How it is built
1. **Prep.** `tools/prep.py` (round 1) and `tools/prep2.py` (round 2) split the
   source JSON into working batches of 35 questions, written to `tools/work/` and
   `tools/work2/` respectively — regenerable, not committed. `prep.py` also writes
   `_existing_index.txt`, the dedup index of the 810 pre-existing pearls;
   `prep2.py` drops any question whose text already appeared in the round-1 dump.
2. **Write.** Each batch's pearls go to `.parts/<Subject>-<batch>.md`
   (245 round-1 parts + 30 round-2 `-z` parts = 275 files).
3. **Assemble.** `tools/assemble.py` concatenates the parts per subject in
   filename order and renumbers the `##` headings into the 19 subject `.md` files.
   Re-running is idempotent — subject files are always rebuilt from `.parts/`.

`.parts/` is the source of truth; the subject `.md` files are generated output.
