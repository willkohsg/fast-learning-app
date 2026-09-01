# QTM Game — Design Spec

A Blooket-style, MCQ-based maths game built on question images cropped from
Singapore prelim / EOY papers. Two levels per question:

1. **Level 1 — QTM (Question Topic Matching):** "What topic is being tested?"
2. **Level 2 — Method Phrasing:** "What is the correct approach / formula to use?"

Level 2 is unlocked per question only after Level 1 is answered. A player never
has to *solve* the question — the whole game trains recognition and method
selection, which is exactly the gap the FAST diagnostic keeps surfacing (A =
Application, wrong-formula and confusion-between-concepts errors).

---

## 1. Content model

### Question
The atomic unit. One cropped image from a paper.

| Field | Notes |
|---|---|
| `imageStorageId` | the crop (PNG/JPG) — stored in Convex file storage |
| `school`, `year`, `paperNumber` (`P1`/`P2`), `qnNumber` | provenance |
| `level` | sec1–sec4 (reuse existing `levelValidator`) |
| `subject` | `emath` \| `amath` (room for others later) |
| `marks` | optional, used for difficulty weighting |
| `topicId` | **the QTM answer** |
| `methodOptions` | 4 options, exactly one correct (Level 2 answer) |
| `qtmDistractors` | optional hand-picked wrong topics; otherwise auto-generated |
| `explanation` | shown after Level 2 — one or two lines, the "why" |
| `status` | `draft` \| `published` (nothing half-tagged reaches players) |

### Topic
A flat, curated taxonomy (not free text — free text is what makes the existing
`errors.topic` field hard to aggregate).

`topics: { name, subject, level[], strand }` — e.g. strand = Algebra, Geometry
& Measurement, Statistics & Probability. Strand matters because it drives
distractor quality (see §3).

### GameSet
A playable pack of 10–20 questions. Two ways to build one, same table:

- `kind: "paper"` — Paper 1 + Paper 2 of one school/year = one set.
- `kind: "topical"` — 10–15 questions of the same topic across schools.

`gameSets: { title, kind, school?, year?, topicId?, level, subject, questionIds[], status }`

A question can belong to many sets; the join is the ordered `questionIds` array
on the set, so reordering is a single write.

---

## 2. Game flow

```
Host creates room from a GameSet  →  join code (6 chars)
Players join with a nickname (no accounts for v1)
  For each question, in set order:
    ┌ Level 1 (QTM)      image + 4 topic options   → 12s
    └ Level 2 (Method)   same image + 4 methods    → 20s
  Reveal: correct answer + explanation + live leaderboard
End: per-player breakdown by topic and by level
```

Scoring (Blooket-ish, tuned so method phrasing is what wins games):

- Level 1 correct: **100** + speed bonus up to 50
- Level 2 correct: **200** + speed bonus up to 100
- Level 2 is worth double because it is the harder, more transferable skill.
- Streak multiplier: 3 consecutive Level 2 correct → ×1.5 until broken.
- Wrong answers score 0 — never negative. Guessing is fine; the data still tells
  us what they confuse.

**Solo mode** matters as much as the live mode: same set, no room, no timer
pressure (or a relaxed one), for homework. Same tables, `mode: "solo" | "live"`.

---

## 3. Distractor quality (the thing that makes or breaks this)

Bad distractors make the game trivially winnable and teach nothing.

- **Level 1 distractors:** pull 3 topics from the *same strand* as the answer,
  preferring topics that appear at the same level. "Circle Properties" vs
  "Trigonometry" is a real confusion; "Circle Properties" vs "Set Notation" is
  not.
- **Level 2 distractors:** hand-written per question, and each should be a
  *plausible* method — the classic ones being:
  1. the right formula applied to the wrong quantity,
  2. a method from an adjacent topic (cosine rule where Pythagoras is needed),
  3. a valid-but-insufficient first step.

Write them as imperative one-liners the student would say out loud:
> "Use the cosine rule to find the third side, then area = ½ab sin C."

This is why Level 2 options are authored, not generated.

---

## 4. Authoring pipeline

The bottleneck is not the game, it's getting tagged questions in. Target:
a paper (roughly 25 questions) tagged in under an hour.

1. **Upload** the paper PDF.
2. **Crop** each question to an image. v1: a browser cropping tool over the
   rendered PDF pages — drag a box, it becomes a question. (Auto-detection of
   question boundaries is a v2 nicety; manual cropping is fast enough and never
   wrong.)
3. **Tag** each crop: pick topic (searchable list), type 4 method options, mark
   the correct one, write the one-line explanation.
4. **Publish** — validation blocks publish unless every question has a topic,
   exactly 4 method options, and exactly one marked correct.

An AI-assist pass (suggest topic + draft 4 method options from the crop, human
confirms) fits cleanly at step 3 once the manual flow works. Build manual first;
the suggestions are only as good as the taxonomy, and the taxonomy is earned by
tagging a few real papers by hand.

---

## 5. Data captured (why this beats a quiz)

Every answer row: `{ playerId, questionId, level, chosenOptionId, correct, msToAnswer }`.

That gives, per student and per class:

- topics they can't *recognise* (Level 1 wrong)
- topics they recognise but can't *plan* (Level 1 right, Level 2 wrong) — the
  single most useful signal, and the one no marks-based report produces
- the specific wrong method chosen, i.e. the exact confusion, by name
- hesitation via `msToAnswer` — slow-and-correct is still a gap

This maps straight onto FAST: Level 1 failure ≈ F (Foundation), Level 2 failure
≈ A (Application), fast-and-wrong ≈ S/T. A class report out of a game session is
the same shape as the existing diagnostic report.

---

## 6. Build order

1. Schema (`topics`, `questions`, `gameSets`) + topic seed data for one subject.
2. Admin authoring UI: upload → crop → tag → publish.
3. Solo play of a published set (no realtime, proves the whole loop end to end).
4. Live rooms: host screen, join code, Convex subscriptions for state.
5. Reports: per-player and per-class breakdown.
6. AI-assisted tagging; avatars/power-ups if the Blooket feel needs them.

Steps 1–3 are the real product. Everything after is amplification.

---

## 7. Open questions

- **Copyright:** cropped school prelim images are re-used third-party content.
  Fine for internal CLG use; needs a decision before anything public.
- **Taxonomy source:** derive topic list from the MOE syllabus document, or from
  the topics already appearing in the diagnostic's `errors.topic` field?
- **Same app or separate?** This shares the FAST vocabulary and could share
  student identity, but has its own admin surface. Recommend: same Convex
  deployment, new `app/game` route tree, separate tables.
