---
name: MS
description: "Build a CLG three-colour Marking Scheme: a step-by-step worked-solutions DOCX where question text is black, working is blue, and M/A/B mark allocations plus examiner's notes are red. Use whenever William / Mr Koh or a CLG tutor asks for a marking scheme, worked solutions, an answer key, a model-answer booklet, M/A/B mark breakdowns, a grading or self-mark scheme, or 'the answers with workings' for any exam or prelim paper (A-Math, E-Math, or any other subject with worked steps). Also triggers on '/MS', 'make the marking scheme', 'do the worked solutions in the usual format', 'answer key with marks', or 'solutions with examiner notes'. Always follow this skill's colour contract and mark-code conventions rather than inventing a layout."
---

# MS — Marking Scheme (CLG three-colour house format)

Produces a worked-solutions DOCX in the CLG marking-scheme house style.

## The colour contract

Three colours carry meaning. Never mix their roles.

| Element | Colour | Hex | Applies to |
|---|---|---|---|
| Question text | black | `000000` | question wording, part labels, headings |
| Working | blue | `1F4E9C` | every step of the solution, and the final answer |
| Marks & notes | red | `C00000` | `M1` / `A1` / `B1` codes, examiner's notes |

## Mark codes

Print this legend on the cover page of every marking scheme:

- **M** — method mark: awarded for a correct method, even if the arithmetic that follows is wrong.
- **A** — accuracy mark: awarded for a correct answer or intermediate value; dependent on the preceding M mark.
- **B** — independent mark: awarded for a correct statement, value or result on its own, with no method required.

State that follow-through (ft) applies throughout: a correct method applied to a candidate's own earlier incorrect value still earns the M mark.

## Non-negotiables

1. **The mark codes must sum to the paper total.** The builder asserts this. If it fails, the allocation is wrong — fix it, don't lower the assertion.
2. **Every question gets at least one examiner's note** explaining where candidates lose marks, not merely restating the answer. This is what makes the document worth more than an answer list.
3. **Verify the mathematics before writing it up.** Check identities numerically, recombine partial fractions, substitute roots back. A marking scheme with a wrong answer is worse than none.
4. **Mark codes sit at a right-aligned tab**, never inline in the middle of a step.
5. **One step per line.** Do not chain three manipulations into one paragraph — the tutor must be able to point at the line that earns each mark.

## Building it

Use `scripts/omml.py` (bundled) so all mathematics is real OMML — editable in Word's equation editor, not styled text. `scripts/ms_builder.py` is a working template: copy it, replace the content calls, keep the helpers.

Helper API:

```python
qhead(num, topic, marks)        # black heading + rule + total for the question
qtext("... $x^2$ ...")          # black question wording
part("(a)  Simplify $...$  [2]")# black part label
work("$...$ working", "M1")     # blue step, red mark code at the margin
ans("$x = 4$", "A1")            # blue answer line, red mark code
note("where candidates slip")   # red examiner's note
```

Text passed to any of these may contain `$...$` spans, which become OMML. `\$` writes a literal dollar sign.

## Renderer caveats (learned the hard way)

These are LibreOffice/StarMath limitations when converting DOCX to PDF. The DOCX is always correct in Word; the PDF is where they show.

- **Colour on maths is dropped.** LibreOffice discards `w:rPr` colour on OMML runs, so equations render black in an LO-generated PDF while Word shows them blue. The markup is correct — say so when delivering, and treat the DOCX as the primary artifact.
- **A maths span must not open or close on a relation.** `$= 5x$` renders as an error glyph. `omml.py` auto-pads a leading relation with a zero-width space; a *trailing* one is not fixable — end the span before it, or wrap the right-hand side, e.g. `$... = \text{RHS}$`.
- **Braces and pipes are grouping characters.** `\{ \}` and `|k|` render as literal escapes or `∨`. Put set braces in prose text and express a modulus another way (`k^2 > 1`, or "k < −1 or k > 1").
- **Multi-letter names** are emitted one run per letter by `omml.py`, avoiding a StarMath mis-parse that turns `DEF` into an error glyph.
- **Always render and read the PDF before delivering.** Grep the extracted text for `¿`, `\frac`, `\text` and `Rightarrow` — each indicates a markup problem that is invisible in the source.

## Delivering

Ship the DOCX and the PDF. Render at 90 dpi or more and actually look at the pages — this format fails visibly (wrong colour, error glyphs) and silently (wrong mark totals), so check both.
