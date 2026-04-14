# FAST Diagnostic — Design Spec

**Date:** 2026-04-15
**Owner:** William Koh (Cambridge Learning Group / CLG)
**Status:** Design approved; pending Phase 2 content extraction and Phase 3 research before implementation plan
**Supersedes:** none

---

## 1. Tool Identity & Positioning

**Working name:** FAST Diagnostic (final name TBD)

**One-liner:** A free, 15-minute online error-log diagnostic that tells a parent and their child exactly which FAST pillar is costing them the most marks — and what to do about it.

**Positioning:** Free public lead magnet + pre-consult qualifier. The tool *diagnoses* the pain (fully revealed) but *prescribes* the solution only in a live consult. This creates honest urgency: users feel the pain, understand it's fixable, and the clear next step is to book a consult.

**Why this works:**
- Matches the in-person 30-min error-log exercise William currently runs during consultations
- Surfaces "which pillar is my child weak in?" — the parent's burning question
- The prescription (techniques to fix a pillar) is held back for the consult, which is where the real value transfer happens
- No gating on the diagnosis itself — the pain must be felt to create desire for the cure

**Non-goals (v1):**
- No login / account / password
- No OCR / AI on the uploaded paper (paper is reference-only)
- No prescriptive "how to fix" advice (that's the consult's job)
- No comparison to other students / leaderboards / gamification
- No progress tracking over multiple papers
- No auto-generated practice questions

---

## 2. User Journey (7 screens)

1. **Landing** — Hero, one CTA ("Start the diagnostic")
2. **Audience select** — Parent / Student / Both (adapts copy register downstream)
3. **Upload paper** — Photo/PDF of recent marked math paper (reference only). Fields: student name, date, school, paper number. "Skip upload" path allowed.
4. **Error log table** — No hard cap; gentle nudge at 20 rows. Per row: Qn, Topic, Error Type (6 options), Error Category (6 options), Root Cause, Details. Mirrors existing paper worksheet exactly. Autosave every 5s. Minimum 3 errors required to submit.
5. **Submitting transition** — Brief "analyzing…" state.
6. **Report (the money shot)** — Two-layer diagnostic: verdict → evidence → patterns → other pillars → dual CTA.
7. **Post-action confirmation** — After WhatsApp or email CTA. Always presents the other CTA as a secondary path.

### Cross-screen UX rules
- Mobile first; Tailwind responsive
- Session URL (`?s=[sessionId]`) = recovery mechanism; no auth
- Browser back button preserves data
- Autosave is non-blocking; inline status, no spinners
- Singapore English: "maths", "secondary N", "paper" (not "test" / "9th grade" / "math")
- WCAG AA color contrast, keyboard nav, labelled form controls

---

## 3. Data Model (Convex)

### Tables

```
sessions
  _id, createdAt, audience ("parent" | "student" | "both"),
  studentName, paperDate, school, paperNumber,
  uploadedPaperFileIds (array of Convex file storage IDs),
  status ("in_progress" | "submitted"),
  submittedAt

errors
  _id, sessionId, qnNumber (1–N),
  topic, errorType (enum), errorCategory (enum),
  rootCause, details,
  primaryPillar (derived, denormalized for reports),
  reinforced (boolean, derived)

errorTypePillar    ← primary mapping (IP, 6 rows)
  _id, errorType (enum), pillar (enum)

errorCategoryPillar ← reinforcement mapping (IP, 6 rows)
  _id, errorCategory (enum), pillar (enum)

reports
  _id, sessionId, pillarScores (record<pillar, percent>),
  topPatterns (array of { label, count, qnNumbers, interpretation }),
  verdictPillar, generatedAt

leads
  _id, sessionId, email, capturedAt,
  ctaTaken ("whatsapp" | "email" | "both" | "none"),
  source ("report_pdf_request" | "whatsapp_click" | ...)
```

### Enums

- **ErrorType** (from worksheet): Careless / Conceptual misunderstanding / Misread the question / Applied wrong formula / Did not complete working / Time management issue
- **ErrorCategory** (from worksheet): Knowledge gap / Misapplied rule / Confusion between similar concepts / Poor exam strategy / Anxiety / panic / Lack of practice
- **Pillar:** F / A / S / T (full names TBD from Phase 2 book extraction)

### Pillar mapping — Rule B with reinforcement semantic

**Rule:** Error Type determines the primary pillar. Error Category reinforces (or doesn't) that pillar.

**Computation on submit:**
1. For each error: `primaryPillar = errorTypePillar[errorType]`
2. For each error: `reinforced = errorCategoryPillar[errorCategory] === primaryPillar`
3. Count errors per primary pillar → divide by total → percentage
4. Rank pillars descending by %; top = `verdictPillar`. **Tie-break rule:** if two or more pillars are within 5 percentage points of each other at the top, verdict displays the tied pillars together ("Your weakest pillars are **F** and **A** — roughly even at ~40% each") rather than picking one arbitrarily. Prevents false precision.
5. Top 3 recurring patterns: group errors by (errorType, errorCategory); keep 3 highest-count; carry `details` free text for citation
6. Persist as `reports` row

**Mapping is editable in Convex dashboard without redeploy** — this is William's IP and will be tuned from real data.

---

## 4. Report Anatomy (Screen 6)

### Block structure

1. **Hero verdict** — *"Your weakest FAST pillar is **[PILLAR]**."* + 1 subline with % + 1 sentence of pillar definition (from framework). Visual: single pillar badge with % arc. Above the fold.
2. **"Here's what we saw"** — 1 paragraph citing actual error counts and categories. Dynamically generated.
3. **Top 3 Recurring Patterns** — 3 cards. Each: pattern label, count + Q numbers, 1 line of interpretation. No prescription.
4. **Other 3 pillars** — Accordion, collapsed by default. Honest % per pillar, 1–2 sentences each.
5. **What this means** — Bridge paragraph naming the mechanism (training) + venue (consult) + what's omitted (techniques). Honest prescription-gating.
6. **Dual CTA** — Sticky footer (mobile) / sidebar (desktop):
   - 📅 *Book a 30-min FAST consult* → wa.me dynamic deep link
   - ✉️ *Email me this report as a PDF* → inline email field, Resend delivery
7. **Footer** — Privacy, CLG attribution, "Forget my session" link (24h purge).

### Voice & tone rules

1. Clinical but warm — like a doctor who cares.
2. Second-person always; switches based on Screen 2 audience selection.
3. Specific over general — every Block 2–4 sentence must cite a number or user-typed field.
4. Diagnosis language, not advice language. *"This is a classic F-pillar pattern"* ✅; *"Do past papers daily"* ❌.
5. Singapore English.
6. No scare tactics. Weaknesses framed as fixable and normal.
7. Length budget: Hero ≤25 words, pattern card ≤40 words, full report ≤350 words excluding collapsed sections.
8. Never fabricate credentials or claims for CLG.

**These rules are guardrails.** Phase 2 (pattern-library-builder) will replace them with concrete extracted patterns from William's PDFs.

### WhatsApp deep-link template

Primary: **`wa.me/6582234772?text=[URL-ENCODED]`** with dynamic context.

```
Hi CLG, I just completed the Error Log Diagnostic.

My results:
• Student: [Name]
• Level: [from paper dropdown]
• Weakest pillar: [PILLAR] ([X]%)
• Top pattern: [Top Pattern Label]

I'd like to book a FAST Learning System Consultation.
```

Static `wa.link/hkykpc` retained as fallback for character-limit edge cases.

### Email PDF template

Resend transactional email on submit of email field:
- Subject: *"[Student Name], here's your FAST Diagnostic report"*
- Body: 3-sentence summary + dual CTA (WhatsApp + reply)
- PDF attached, generated server-side via `@react-pdf/renderer` in a Convex action
- Lead captured with `source: "report_pdf_request"`

---

## 5. Tech Stack

| Layer | Choice | Rationale |
|---|---|---|
| Frontend | Next.js 15 (App Router) | Lowest-friction pairing with Vercel |
| Styling | Tailwind CSS + shadcn/ui | Polished form controls without custom design |
| Backend / DB | Convex | Realtime, type-safe, mapping editable in dashboard |
| File storage | Convex built-in | Handles uploaded paper photos/PDFs |
| Email | Resend | Free tier sufficient for MVP; clean API |
| PDF generation | `@react-pdf/renderer` | Server-side in Convex action |
| Booking CTA | wa.me dynamic deep link | Existing WhatsApp workflow; no new tooling |
| Auth | None | Session token in URL; zero friction |
| Hosting | Vercel | Auto-deploy from GitHub main |
| Analytics | Vercel Analytics | Funnel visibility for free |
| Repo | GitHub (willkohsg/fast-learning-app) | Already created |

---

## 6. Build Phases

| # | Phase | Owning skill | Output |
|---|---|---|---|
| P0 | Project scaffold | executing-plans | Next.js + Convex + Tailwind + shadcn + Resend client wired; Vercel deploy from main |
| P1 | Content extraction | source-preprocessor → knowledge-extractor → pattern-library-builder | Clean text, FAST pillar definitions, error→pillar mapping, voice patterns |
| P2 | Convex schema + seed | TDD | Tables deployed; mapping seeded from P1 |
| P3 | Screens 1–3 | TDD | Landing, audience, upload flow end-to-end; session recovery |
| P4 | Screen 4 | TDD | Error log table, autosave, 3-error min validation |
| P5 | Computation + Screen 5 | TDD | Pillar scoring, reinforcement, top-3 patterns, report persistence |
| P6 | Screen 6 + PDF | TDD + pattern-based-generator | Report UI using extracted voice; PDF export |
| P7 | Dual CTA + Screen 7 | TDD | wa.me dynamic link, Resend email, leads capture |
| P8 | Polish + deploy | verification-before-completion → finishing-a-development-branch | Vercel prod URL; e2e smoke test; CLAUDE.md updated; tag v1.0 |

---

## 7. Risks & Mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| PDF extraction garbled | Medium | OCR fallback in source-preprocessor; spot-check with William |
| Voice feels off | Medium | pattern-library-builder; William reviews 3–5 sample reports pre-ship; copy in Convex |
| Pillar mapping ambiguous from PDFs | Medium | If fuzzy, pause and interview William on 6 Error Types → pillar direct |
| Mobile file upload fails (HEIC) | Low-Med | Explicit HEIC config; "skip upload" path |
| WhatsApp message truncated | Low | Cap <350 chars; `wa.link` fallback |
| Convex free-tier exceeded | Very Low | Dashboard monitoring; trivial upgrade |
| Bounce after upload | Medium | Autosave + session URL recovery; email nudge (post-v1) |
| Report feels generic | High (if P1 rushed) | P1 is the biggest quality lever — proportionate time invested |

---

## 8. Success Metrics

### Funnel (leading)
- Landing → Start clicks
- Start → Errors logged (≥3)
- Errors logged → Report viewed
- Report viewed → CTA clicked

### Outcomes (lagging)
- WhatsApp clicks → actual bookings (manual tracking via WhatsApp initially)
- Email captures → bookings (attribution via follow-up)
- Completion rate (reach Screen 6 out of starters)
- Avg errors logged per completed session

### Benchmark targets (v1; refine after 50 users)
- ≥50% landing → start
- ≥60% start → Screen 6
- ≥30% report-view → CTA click
- ≥10% WhatsApp click → booking

If below after 50 sessions: iterate copy before adding features.

---

## 9. "Done" Definition for v1

- Live URL on Vercel
- 5 real end-to-end test runs (3 dummy by Claude, 2 real by William)
- CLAUDE.md updated with pillar names, voice rules, known limits
- Design doc, implementation plan, all PRs merged
- README with deploy instructions + Convex dashboard link
- Shareable to 10 parents without embarrassment

---

## 10. Open Items Deferred to Phase 2

- Full names of FAST pillars (F, A, S, T stand for what)
- Authoritative errorType → pillar mapping (6 rows)
- Authoritative errorCategory → pillar mapping (6 rows)
- Voice pattern library (sentence structures, metaphors, phrasings unique to William's content)
- Level/syllabus scoping (PSLE only? O-level? A-level? all?)
- Any framework-specific copy for Block 1 pillar definition and Block 5 bridge paragraph

## 11. Open Items Deferred to Phase 3 (parallel research)

- Anti-patterns in similar single-use diagnostic tools
- Best UX patterns for ~15-min assessment tools on mobile
- Benchmark conversion rates for similar lead magnets in education niche

---

**Next step after spec approval:** Invoke `writing-plans` skill to produce the detailed implementation plan.
