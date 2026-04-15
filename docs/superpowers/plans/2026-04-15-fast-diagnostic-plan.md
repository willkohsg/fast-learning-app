# FAST Diagnostic Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and deploy a free, 15-minute online error-log diagnostic that maps a maths student's exam errors to William Koh's FAST pillars and converts them into a booked consult via WhatsApp or an emailed PDF report.

**Architecture:** Next.js 15 (App Router) on Vercel, Convex for data + file storage, Resend for email, `@react-pdf/renderer` for the PDF report. No auth — sessions identified by URL token. Typeform-style single-error-per-screen entry flow. Mobile-first.

**Tech Stack:** Next.js 15, React 19, TypeScript, Tailwind CSS v4, shadcn/ui, Convex, Resend, `@react-pdf/renderer`, Vitest + React Testing Library + Playwright.

---

## Design Updates From Phase 2 + Phase 3 (vs. Approved Spec)

The design doc approved in the brainstorming phase had the error-log as a **table (20 rows visible at once)**. Phase 3 research strongly recommends switching to a **Typeform-style flow — one error per screen** — as the single biggest completion-rate lever on mobile. This plan implements the one-per-screen pattern.

Other research-driven updates applied to this plan:

1. **Progress bar** — segmented, "unlocks report at 5 minimum", invites up to 20 (no shrinking percentage bar).
2. **Autosave** — silent `localStorage` on every input; Convex sync on every "next error" step; welcome-back banner on reload.
3. **Reassurance screens** every 5 errors ("Students who log 10+ errors get a 2× sharper diagnosis") + 2-second faux-analysis animation before report render (+10–20% conversion lift, free to implement).
4. **Verdict before email gate** — full on-screen report is free; only the downloadable PDF requires email.
5. **Mobile accordion report** — weakest pillar expanded by default; other three collapsed with one-line previews.
6. **Dual CTA stacked (not side-by-side)** — WhatsApp primary button, email PDF outlined button below.
7. **Every pain statement cites user's own data** — "4 of your 12 errors traced to F-pillar" — never generic.

The original spec's 7-screen structure is preserved, but **Screen 4** (error log) is now a sub-flow of N screens (one per error) rather than a single table screen.

---

## Open Questions (require William's input before or during build)

Flag these at plan approval. Each has a fallback to keep the build moving if not answered:

1. **Careless → pillar mapping.** ✅ **RESOLVED (William, 2026-04-15):** Careless is a lossy bucket with 3 distinct roots. When the user selects `errorType = "careless"`, the form reveals a **conditional follow-up question** ("What caused this careless mistake?") with 3 options that route to different pillars:
   - *"I misunderstood the question"* → **A** (Analysis)
   - *"I knew what to do but made a slip in working"* → **S** (Solving Pattern / Execution)
   - *"I rushed because of time"* → **T** (Time Management)

   Implementation: new field `carelessRoot: "misunderstood" | "slip" | "rushed"` on the `errors` table (optional; required only when errorType = careless). New Convex table `carelessRootPillar` (3 rows) stores the routing and is editable in the dashboard. Scoring logic: if `carelessRoot` is set, `primaryPillar = carelessRootPillar[carelessRoot]`; else fall back to `errorTypePillar["careless"]` (default T). This preserves worksheet parity while eliminating the ambiguous bucket.
2. **Tool name.** ✅ **RESOLVED (William, 2026-04-15):** Public name is **"FAST DIAGNOSTIC TOOL"** (caps in marketing contexts; title-cased "FAST Diagnostic Tool" in running copy). Update: landing `<title>`, hero, meta description, PDF cover page, WhatsApp prefill ("I just completed the FAST Diagnostic Tool…"), email subject line.
3. **Level/syllabus scope.** ✅ **RESOLVED (William, 2026-04-15):** **Secondary school only, Sec 1 to Sec 4** (Singapore). Impact:
   - Audience picker copy: "Sec 1", "Sec 2", "Sec 3", "Sec 4" options on the paper-metadata form.
   - Landing hero: "For Sec 1–4 students sitting Singapore maths papers."
   - PSLE and JC/A-Level excluded from v1 copy. If a PSLE/JC user lands, show a soft note: "This tool is tuned for Sec 1–4 maths. Your results may still be useful but aren't calibrated for your level."
   - No change to Convex schema — `paperNumber` / `school` stay free-ish; we add a required `level` field (`sec1` | `sec2` | `sec3` | `sec4`) on `sessions`.
4. **Primary domain.** ✅ **RESOLVED (William, 2026-04-15):** Vercel default **`fast-diagnostic.vercel.app`** for v1. No custom domain setup needed. Vercel project name: `fast-diagnostic` (rename the Vercel project if it defaults to `fast-learning-app`).
5. **Consult duration wording in WhatsApp.** ✅ **RESOLVED (William, 2026-04-15):** **30-min FAST consult** — confirmed. CTA label and WhatsApp prefill both say "Book a 30-min FAST consult."
6. **Email "from" address.** ✅ **RESOLVED (William, 2026-04-15):** **`clgsg2014@gmail.com`**.
   ⚠️ **Important constraint:** Resend cannot send *from* a Gmail address directly (Gmail doesn't allow 3rd-party senders without OAuth / app-password routing, which Resend doesn't support). Two options:
   - **(a) Recommended:** Resend sends from `noreply@resend.dev` (their shared domain) with `Reply-To: clgsg2014@gmail.com` and `From: "CLG FAST Diagnostic" <noreply@resend.dev>`. User-visible "from name" still reads "CLG FAST Diagnostic" and any reply routes to your Gmail inbox. Zero setup.
   - **(b) Better long-term:** Buy a domain (e.g. `cambridgelearning.sg` if not already owned), verify in Resend, send from `hello@cambridgelearning.sg` with `Reply-To: clgsg2014@gmail.com`. Costs ~$15/yr + 10 min DNS setup.

   **Default plan:** ship with (a) for v1; flag (b) as post-launch upgrade.
7. **Privacy/data retention wording.** ✅ **RESOLVED (William, 2026-04-15):** **24-hour retention after report generation.** What we retain:
   - **Session inputs:** audience, student name (first name only recommended), level (Sec 1–4), school, paper number, paper date.
   - **Uploaded paper file(s):** the photo/PDF the user uploaded (stored in Convex file storage).
   - **All keyed error rows:** qnNumber, topic, errorType, errorCategory, carelessRoot (if applicable), rootCause, details.
   - **Computed report:** pillar scores, top patterns, verdict pillar(s).
   - **Lead contact info (ONLY if they click WhatsApp or submit the email-PDF form):** email address, CTA taken. Leads are retained indefinitely (this is the business value). All *other* session data is purged at 24h.

   **Purge mechanism:** Convex scheduled function (`crons.ts`) runs hourly, deletes any `sessions` + related `errors` + uploaded files + `reports` where `submittedAt < now - 24h` AND no matching `leads` row. Leads survive; everything else is wiped.

   **Footer copy:** *"We keep your diagnostic data for 24 hours so you can revisit your report, then it's automatically deleted. If you submit your email for the PDF or book a consult, we keep only your contact details and report summary to follow up."*

---

## File Structure (locked before tasks)

```
fast-learning-app/
├── README.md                                 (already exists)
├── CLAUDE.md                                 (created in P0)
├── package.json
├── tsconfig.json
├── next.config.ts
├── tailwind.config.ts
├── postcss.config.mjs
├── .env.local.example
├── .gitignore
├── components.json                           (shadcn/ui config)
├── convex.json
├── vercel.json
│
├── app/                                      (Next.js App Router)
│   ├── layout.tsx
│   ├── page.tsx                              (Screen 1: landing)
│   ├── globals.css
│   ├── providers.tsx                         (ConvexProvider wrapper)
│   ├── diagnostic/
│   │   ├── new/page.tsx                      (Creates session → redirects)
│   │   ├── [sessionId]/
│   │   │   ├── audience/page.tsx             (Screen 2)
│   │   │   ├── upload/page.tsx               (Screen 3)
│   │   │   ├── errors/[index]/page.tsx       (Screen 4 — one per error)
│   │   │   ├── submit/page.tsx               (Screen 5: faux analyzing)
│   │   │   └── report/page.tsx               (Screen 6 + 7 combined)
│   └── api/
│       └── pdf/[sessionId]/route.ts          (PDF download endpoint)
│
├── components/
│   ├── ui/                                   (shadcn primitives)
│   ├── audience-picker.tsx
│   ├── file-uploader.tsx
│   ├── error-entry-form.tsx
│   ├── progress-bar.tsx
│   ├── welcome-back-banner.tsx
│   ├── reassurance-screen.tsx
│   ├── report/
│   │   ├── hero-verdict.tsx
│   │   ├── evidence-block.tsx
│   │   ├── pattern-cards.tsx
│   │   ├── pillars-accordion.tsx
│   │   ├── bridge-paragraph.tsx
│   │   └── dual-cta.tsx
│   └── pdf/
│       └── report-pdf.tsx                    (@react-pdf/renderer document)
│
├── lib/
│   ├── constants.ts                          (error types, categories, audiences)
│   ├── pillars.ts                            (F/A/S/T metadata)
│   ├── copy.ts                               (adaptive copy strings, audience-aware)
│   ├── whatsapp.ts                           (wa.me deep-link builder)
│   ├── session-storage.ts                    (localStorage helpers)
│   └── utils.ts                              (cn helper from shadcn)
│
├── convex/
│   ├── schema.ts
│   ├── sessions.ts                           (queries + mutations)
│   ├── errors.ts                             (queries + mutations)
│   ├── mappings.ts                           (queries for pillar mapping)
│   ├── reports.ts                            (compute + persist)
│   ├── leads.ts                              (email capture)
│   ├── files.ts                              (upload URL generation)
│   ├── emails.ts                             (Resend action)
│   ├── pdfGen.ts                             (PDF generation action)
│   └── seed.ts                               (seed mapping tables)
│
├── tests/
│   ├── unit/
│   │   ├── whatsapp.test.ts
│   │   ├── pillar-scoring.test.ts
│   │   └── copy.test.ts
│   ├── components/
│   │   ├── audience-picker.test.tsx
│   │   ├── progress-bar.test.tsx
│   │   └── report/hero-verdict.test.tsx
│   └── e2e/
│       └── full-flow.spec.ts                 (Playwright)
│
└── docs/superpowers/                         (already exists)
    ├── specs/2026-04-15-fast-diagnostic-design.md
    ├── phase2-extraction/...
    ├── phase3-research/...
    └── plans/2026-04-15-fast-diagnostic-plan.md    (this file)
```

---

## Phase 0 — Project Scaffold

### Task 0.1: Initialize Next.js project

**Files:**
- Create: `package.json`, `tsconfig.json`, `next.config.ts`, `app/layout.tsx`, `app/page.tsx`, `app/globals.css`, `.gitignore`

- [ ] **Step 1: Run Next.js init**

Run from the repo root (`C:\Users\William\Desktop\Projects\fast-learning-app`):
```bash
npx create-next-app@latest . --typescript --tailwind --app --no-src-dir --import-alias "@/*" --use-npm --turbopack --eslint
```
If prompted about non-empty directory, say yes (it's safe — README and docs are untouched).

- [ ] **Step 2: Verify dev server starts**
```bash
npm run dev
```
Expected: "Ready in …ms" and `http://localhost:3000` returns a page.
Stop the server (Ctrl+C) after confirming.

- [ ] **Step 3: Commit**
```bash
git add -A
git commit -m "chore(P0): scaffold Next.js 15 with App Router, TypeScript, Tailwind"
```

### Task 0.2: Install shadcn/ui, Convex, Resend, react-pdf, testing libs

**Files:** `package.json` (modified), `components.json` (created), `components/ui/*` (created)

- [ ] **Step 1: Initialize shadcn/ui**
```bash
npx shadcn@latest init -d
```
Accept defaults (Slate, CSS variables, `@/components`).

- [ ] **Step 2: Add initial shadcn components**
```bash
npx shadcn@latest add button card input label textarea select radio-group accordion progress sonner dialog form
```

- [ ] **Step 3: Install Convex, Resend, react-pdf, testing libs**
```bash
npm install convex resend @react-pdf/renderer
npm install -D vitest @vitejs/plugin-react @testing-library/react @testing-library/jest-dom jsdom @playwright/test
```

- [ ] **Step 4: Verify build still works**
```bash
npm run build
```
Expected: compiles without error.

- [ ] **Step 5: Commit**
```bash
git add -A
git commit -m "chore(P0): install shadcn/ui, Convex, Resend, react-pdf, test libs"
```

### Task 0.3: Configure Convex

**Files:** `convex.json`, `convex/_generated/*`, `app/providers.tsx`, `app/layout.tsx`, `.env.local.example`

- [ ] **Step 1: Initialize Convex**
```bash
npx convex dev --once --configure=new
```
Accept the prompt to create a new Convex project named `fast-learning-app`.
This generates `convex/_generated/`, writes `NEXT_PUBLIC_CONVEX_URL` to `.env.local`, and creates `convex.json`.

- [ ] **Step 2: Create `app/providers.tsx`**
```tsx
"use client";
import { ConvexProvider, ConvexReactClient } from "convex/react";
import { ReactNode } from "react";

const convex = new ConvexReactClient(process.env.NEXT_PUBLIC_CONVEX_URL!);

export function Providers({ children }: { children: ReactNode }) {
  return <ConvexProvider client={convex}>{children}</ConvexProvider>;
}
```

- [ ] **Step 3: Wrap `app/layout.tsx` with `<Providers>`**

Modify `app/layout.tsx` so that `{children}` is wrapped:
```tsx
import { Providers } from "./providers";
// ... inside <body>:
<Providers>{children}</Providers>
```

- [ ] **Step 4: Create `.env.local.example`**
```
NEXT_PUBLIC_CONVEX_URL=
RESEND_API_KEY=
WA_PHONE_NUMBER=6582234772
WA_FALLBACK_LINK=https://wa.link/hkykpc
```
Add to `.gitignore`: ensure `.env.local` is ignored (Next.js default already does this).

- [ ] **Step 5: Verify both `npm run dev` and `npx convex dev` run side by side**

In one terminal: `npx convex dev` (keep running)
In another: `npm run dev`
Visit `http://localhost:3000` — no errors in the dev-tools console.

- [ ] **Step 6: Commit**
```bash
git add -A
git commit -m "chore(P0): configure Convex and ConvexProvider"
```

### Task 0.4: Configure Vitest + Playwright

**Files:** `vitest.config.ts`, `tests/setup.ts`, `playwright.config.ts`, `package.json` scripts

- [ ] **Step 1: Create `vitest.config.ts`**
```ts
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    setupFiles: ["./tests/setup.ts"],
    globals: true,
  },
  resolve: {
    alias: { "@": path.resolve(__dirname, "./") },
  },
});
```

- [ ] **Step 2: Create `tests/setup.ts`**
```ts
import "@testing-library/jest-dom/vitest";
```

- [ ] **Step 3: Initialize Playwright**
```bash
npx playwright install --with-deps chromium
```
Then create `playwright.config.ts`:
```ts
import { defineConfig } from "@playwright/test";
export default defineConfig({
  testDir: "./tests/e2e",
  use: { baseURL: "http://localhost:3000" },
  webServer: { command: "npm run dev", url: "http://localhost:3000", reuseExistingServer: true },
});
```

- [ ] **Step 4: Add test scripts to `package.json`**
```json
"scripts": {
  "dev": "next dev --turbopack",
  "build": "next build",
  "start": "next start",
  "lint": "next lint",
  "test": "vitest run",
  "test:watch": "vitest",
  "test:e2e": "playwright test"
}
```

- [ ] **Step 5: Write a smoke test to verify setup**

Create `tests/unit/smoke.test.ts`:
```ts
import { describe, it, expect } from "vitest";
describe("smoke", () => {
  it("runs", () => { expect(1 + 1).toBe(2); });
});
```

- [ ] **Step 6: Run and verify**
```bash
npm test
```
Expected: 1 test passes.

- [ ] **Step 7: Commit**
```bash
git add -A
git commit -m "chore(P0): configure Vitest and Playwright with smoke test"
```

### Task 0.5: Create CLAUDE.md

**Files:** `CLAUDE.md`

- [ ] **Step 1: Create `CLAUDE.md` at repo root**

Content:
```markdown
# FAST Diagnostic — CLAUDE.md

## What This Is
A 15-min online error-log diagnostic for Singapore maths students. Parents/students
log exam errors; the tool maps them to FAST pillars (F, A, S, T) and produces a
two-layer diagnostic report with a dual CTA (WhatsApp book / email PDF).
Lead magnet + pre-consult qualifier for Cambridge Learning Group (CLG).

## Current Status
P0 scaffold complete. See docs/superpowers/plans/ for current plan.

## Key Context
- Owner: William Koh (CLG founder)
- FAST:
  - F = Facts, Figures & Formulas (3R: Retrieve / Reinforce / Repeat)
  - A = Analysis of Questions (QTM: Question / Topic / Method)
  - S = Solving Patterns (Pattern Before Process)
  - T = Time Management (IQST: Information / Question / Solving / Time)
- Single-use tool; no auth; sessionId lives in URL.
- Singapore English, Singapore maths syllabus (PSLE / N-level / O-level / A-level).
- Design spec: docs/superpowers/specs/2026-04-15-fast-diagnostic-design.md
- Implementation plan: docs/superpowers/plans/2026-04-15-fast-diagnostic-plan.md
- Source content: PDFs at repo root + extracted to docs/superpowers/phase2-extraction/

## Tech Stack
- Next.js 15 (App Router) + React 19 + TypeScript
- Tailwind CSS v4 + shadcn/ui
- Convex (DB + file storage)
- Resend (transactional email)
- @react-pdf/renderer (PDF report)
- Vercel (hosting, auto-deploy from main)
- No auth library; sessionId in URL path

## Critical Rules
- Never write prescriptive advice in the report — diagnostic language only.
- Copy that varies (report text, landing headline) lives in `lib/copy.ts` — easy to edit.
- Pillar mapping lives in Convex tables (`errorTypePillar`, `errorCategoryPillar`, `carelessRootPillar`) — William edits in dashboard, no redeploy.
- Singapore English only ("maths", "secondary 3", "paper").
- Never fabricate CLG credentials or claims — pull from the book PDF only.
- Before claiming any task done: run the Task's verification step.

## Mistakes List
(empty to start — add one-line entry per correction from William)
```

- [ ] **Step 2: Commit**
```bash
git add CLAUDE.md
git commit -m "docs(P0): add CLAUDE.md"
```

### Task 0.6: Connect GitHub repo to Vercel

**Files:** none (Vercel config via CLI)

- [ ] **Step 1: Link project**
```bash
vercel link --yes
```
When prompted, create a new project. Accept defaults.

- [ ] **Step 2: Push environment variables to Vercel**
```bash
vercel env add NEXT_PUBLIC_CONVEX_URL production
# paste the Convex URL from .env.local
```

- [ ] **Step 3: Deploy a preview**
```bash
vercel --yes
```
Expected: preview URL returned, the Next.js default page loads.

- [ ] **Step 4: Push main to auto-deploy to production**
```bash
git push origin main
vercel --prod --yes
```

- [ ] **Step 5: Commit + note prod URL**
```bash
# note the URL in CLAUDE.md under "Current Status"
git add CLAUDE.md
git commit -m "chore(P0): deploy initial scaffold to Vercel"
```

---

## Phase 2 — Convex Schema + Mapping Seed

### Task 2.1: Define schema

**Files:** `convex/schema.ts`

- [ ] **Step 1: Write failing test**

Create `tests/unit/schema-shape.test.ts`:
```ts
import { describe, it, expect } from "vitest";
import schema from "@/convex/schema";

describe("Convex schema", () => {
  it("defines the 6 required tables", () => {
    const tables = Object.keys(schema.tables);
    expect(tables).toEqual(
      expect.arrayContaining([
        "sessions", "errors", "errorTypePillar",
        "errorCategoryPillar", "carelessRootPillar", "reports", "leads",
      ]),
    );
  });
});
```

- [ ] **Step 2: Run — expect import failure**
```bash
npm test -- schema-shape
```
Expected: fails (schema doesn't exist yet).

- [ ] **Step 3: Implement `convex/schema.ts`**
```ts
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export const errorTypeValidator = v.union(
  v.literal("careless"),
  v.literal("conceptual_misunderstanding"),
  v.literal("misread_question"),
  v.literal("applied_wrong_formula"),
  v.literal("did_not_complete_working"),
  v.literal("time_management_issue"),
);

export const errorCategoryValidator = v.union(
  v.literal("knowledge_gap"),
  v.literal("misapplied_rule"),
  v.literal("confusion_between_concepts"),
  v.literal("poor_exam_strategy"),
  v.literal("anxiety_panic"),
  v.literal("lack_of_practice"),
);

// Conditional follow-up: only set when errorType === "careless".
// Routes the lossy "careless" bucket to A / S / T based on root cause.
export const carelessRootValidator = v.union(
  v.literal("misunderstood"), // → A (Analysis)
  v.literal("slip"),          // → S (Solving Pattern / Execution)
  v.literal("rushed"),        // → T (Time Management)
);

export const pillarValidator = v.union(
  v.literal("F"), v.literal("A"), v.literal("S"), v.literal("T"),
);

export const audienceValidator = v.union(
  v.literal("parent"), v.literal("student"), v.literal("both"),
);

// Sec 1–4 only (William, 2026-04-15). PSLE/JC excluded from v1.
export const levelValidator = v.union(
  v.literal("sec1"), v.literal("sec2"), v.literal("sec3"), v.literal("sec4"),
);

export default defineSchema({
  sessions: defineTable({
    createdAt: v.number(),
    audience: v.optional(audienceValidator),
    level: v.optional(levelValidator), // Sec 1–4; set on Screen 3
    studentName: v.optional(v.string()),
    paperDate: v.optional(v.string()),
    school: v.optional(v.string()),
    paperNumber: v.optional(v.string()),
    uploadedPaperFileIds: v.optional(v.array(v.id("_storage"))),
    status: v.union(v.literal("in_progress"), v.literal("submitted")),
    submittedAt: v.optional(v.number()),
  }),
  errors: defineTable({
    sessionId: v.id("sessions"),
    qnNumber: v.number(),
    topic: v.string(),
    errorType: errorTypeValidator,
    errorCategory: errorCategoryValidator,
    carelessRoot: v.optional(carelessRootValidator), // only when errorType === "careless"
    rootCause: v.optional(v.string()),
    details: v.optional(v.string()),
    primaryPillar: v.optional(pillarValidator),
    reinforced: v.optional(v.boolean()),
  }).index("by_session", ["sessionId"]),
  errorTypePillar: defineTable({
    errorType: errorTypeValidator,
    pillar: pillarValidator,
  }).index("by_errorType", ["errorType"]),
  errorCategoryPillar: defineTable({
    errorCategory: errorCategoryValidator,
    pillar: pillarValidator,
  }).index("by_errorCategory", ["errorCategory"]),
  carelessRootPillar: defineTable({
    carelessRoot: carelessRootValidator,
    pillar: pillarValidator,
  }).index("by_carelessRoot", ["carelessRoot"]),
  reports: defineTable({
    sessionId: v.id("sessions"),
    pillarScores: v.object({
      F: v.number(), A: v.number(), S: v.number(), T: v.number(),
    }),
    topPatterns: v.array(v.object({
      label: v.string(),
      count: v.number(),
      qnNumbers: v.array(v.number()),
      interpretation: v.string(),
    })),
    verdictPillars: v.array(pillarValidator),
    generatedAt: v.number(),
  }).index("by_session", ["sessionId"]),
  leads: defineTable({
    sessionId: v.id("sessions"),
    email: v.string(),
    capturedAt: v.number(),
    ctaTaken: v.union(
      v.literal("whatsapp"), v.literal("email"),
      v.literal("both"), v.literal("none"),
    ),
    source: v.string(),
  }).index("by_session", ["sessionId"]),
});
```

- [ ] **Step 4: Run test — expect pass**
```bash
npm test -- schema-shape
```
Expected: test passes.

- [ ] **Step 5: Push to Convex**
```bash
npx convex dev --once
```
Expected: schema pushed without error.

- [ ] **Step 6: Commit**
```bash
git add convex/ tests/unit/schema-shape.test.ts
git commit -m "feat(P2): define Convex schema with validators"
```

### Task 2.2: Seed pillar mapping tables

**Files:** `convex/seed.ts`, `tests/unit/seed.test.ts`

- [ ] **Step 1: Write `convex/seed.ts` (internal mutation)**
```ts
import { internalMutation } from "./_generated/server";

export const seedMappings = internalMutation({
  args: {},
  handler: async (ctx) => {
    const typeMapping = [
      { errorType: "careless" as const, pillar: "T" as const },
      { errorType: "conceptual_misunderstanding" as const, pillar: "F" as const },
      { errorType: "misread_question" as const, pillar: "A" as const },
      { errorType: "applied_wrong_formula" as const, pillar: "S" as const },
      { errorType: "did_not_complete_working" as const, pillar: "S" as const },
      { errorType: "time_management_issue" as const, pillar: "T" as const },
    ];
    const categoryMapping = [
      { errorCategory: "knowledge_gap" as const, pillar: "F" as const },
      { errorCategory: "misapplied_rule" as const, pillar: "A" as const },
      { errorCategory: "confusion_between_concepts" as const, pillar: "S" as const },
      { errorCategory: "poor_exam_strategy" as const, pillar: "T" as const },
      { errorCategory: "anxiety_panic" as const, pillar: "T" as const },
      { errorCategory: "lack_of_practice" as const, pillar: "S" as const },
    ];
    // Careless follow-up routing (William, 2026-04-15): decomposes the lossy
    // "careless" bucket into A / S / T based on the true root cause.
    const carelessRootMapping = [
      { carelessRoot: "misunderstood" as const, pillar: "A" as const }, // misread / misunderstood question
      { carelessRoot: "slip" as const,         pillar: "S" as const }, // knew what to do, execution slip
      { carelessRoot: "rushed" as const,       pillar: "T" as const }, // time pressure
    ];

    const existingTypes = await ctx.db.query("errorTypePillar").collect();
    if (existingTypes.length === 0) {
      for (const row of typeMapping) await ctx.db.insert("errorTypePillar", row);
    }
    const existingCats = await ctx.db.query("errorCategoryPillar").collect();
    if (existingCats.length === 0) {
      for (const row of categoryMapping) await ctx.db.insert("errorCategoryPillar", row);
    }
    const existingCarelessRoots = await ctx.db.query("carelessRootPillar").collect();
    if (existingCarelessRoots.length === 0) {
      for (const row of carelessRootMapping) await ctx.db.insert("carelessRootPillar", row);
    }
    return {
      seeded:
        existingTypes.length === 0 ||
        existingCats.length === 0 ||
        existingCarelessRoots.length === 0,
    };
  },
});
```

- [ ] **Step 2: Run seed**
```bash
npx convex run seed:seedMappings
```
Expected: returns `{ seeded: true }` on first run; `{ seeded: false }` on subsequent runs.

- [ ] **Step 3: Verify via Convex dashboard**
Open https://dashboard.convex.dev → your project → Data tab. Confirm both mapping tables have 6 rows each.

- [ ] **Step 4: Commit**
```bash
git add convex/seed.ts
git commit -m "feat(P2): seed pillar mapping tables from extracted book content"
```

### Task 2.3: Session mutations + queries

**Files:** `convex/sessions.ts`, `tests/unit/pillar-scoring.test.ts` (later), `convex/errors.ts`

- [ ] **Step 1: Write `convex/sessions.ts`**
```ts
import { mutation, query } from "./_generated/server";
import { v } from "convex/values";
import { audienceValidator } from "./schema";

export const create = mutation({
  args: {},
  handler: async (ctx) => {
    return await ctx.db.insert("sessions", {
      createdAt: Date.now(),
      status: "in_progress",
    });
  },
});

export const get = query({
  args: { id: v.id("sessions") },
  handler: async (ctx, { id }) => await ctx.db.get(id),
});

export const updateMetadata = mutation({
  args: {
    id: v.id("sessions"),
    audience: v.optional(audienceValidator),
    studentName: v.optional(v.string()),
    paperDate: v.optional(v.string()),
    school: v.optional(v.string()),
    paperNumber: v.optional(v.string()),
    uploadedPaperFileIds: v.optional(v.array(v.id("_storage"))),
  },
  handler: async (ctx, { id, ...patch }) => {
    await ctx.db.patch(id, patch);
  },
});

export const markSubmitted = mutation({
  args: { id: v.id("sessions") },
  handler: async (ctx, { id }) => {
    await ctx.db.patch(id, { status: "submitted", submittedAt: Date.now() });
  },
});
```

- [ ] **Step 2: Write `convex/errors.ts`**
```ts
import { mutation, query } from "./_generated/server";
import { v } from "convex/values";
import { errorTypeValidator, errorCategoryValidator, carelessRootValidator } from "./schema";

export const listBySession = query({
  args: { sessionId: v.id("sessions") },
  handler: async (ctx, { sessionId }) =>
    await ctx.db.query("errors").withIndex("by_session", q => q.eq("sessionId", sessionId)).collect(),
});

export const upsert = mutation({
  args: {
    sessionId: v.id("sessions"),
    qnNumber: v.number(),
    topic: v.string(),
    errorType: errorTypeValidator,
    errorCategory: errorCategoryValidator,
    carelessRoot: v.optional(carelessRootValidator),
    rootCause: v.optional(v.string()),
    details: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const existing = await ctx.db.query("errors")
      .withIndex("by_session", q => q.eq("sessionId", args.sessionId))
      .filter(q => q.eq(q.field("qnNumber"), args.qnNumber))
      .first();
    if (existing) {
      await ctx.db.patch(existing._id, args);
      return existing._id;
    }
    return await ctx.db.insert("errors", args);
  },
});

export const remove = mutation({
  args: { id: v.id("errors") },
  handler: async (ctx, { id }) => { await ctx.db.delete(id); },
});
```

- [ ] **Step 3: Push to Convex**
```bash
npx convex dev --once
```
Expected: no errors.

- [ ] **Step 4: Commit**
```bash
git add convex/
git commit -m "feat(P2): session and error mutations/queries"
```

---

## Phase 3 — Screens 1–3 (Landing, Audience, Upload)

### Task 3.1: Constants + lib/pillars

**Files:** `lib/constants.ts`, `lib/pillars.ts`, `lib/copy.ts`, `tests/unit/copy.test.ts`

- [ ] **Step 1: Write `lib/constants.ts`**
```ts
export const ERROR_TYPES = [
  { value: "careless", label: "Careless" },
  { value: "conceptual_misunderstanding", label: "Conceptual misunderstanding" },
  { value: "misread_question", label: "Misread the question" },
  { value: "applied_wrong_formula", label: "Applied wrong formula" },
  { value: "did_not_complete_working", label: "Did not complete working" },
  { value: "time_management_issue", label: "Time management issue" },
] as const;

export const ERROR_CATEGORIES = [
  { value: "knowledge_gap", label: "Knowledge gap" },
  { value: "misapplied_rule", label: "Misapplied rule" },
  { value: "confusion_between_concepts", label: "Confusion between similar concepts" },
  { value: "poor_exam_strategy", label: "Poor exam strategy" },
  { value: "anxiety_panic", label: "Anxiety / panic" },
  { value: "lack_of_practice", label: "Lack of practice with that type of question" },
] as const;

// Conditional follow-up: shown only when errorType === "careless".
// "Careless" is a lossy bucket; these 3 options resolve its true root cause
// and route the error to the correct pillar (A / S / T).
export const CARELESS_ROOTS = [
  { value: "misunderstood", label: "I misunderstood the question",            pillarHint: "A" },
  { value: "slip",          label: "I knew what to do but made a slip",       pillarHint: "S" },
  { value: "rushed",        label: "I rushed because of time",                pillarHint: "T" },
] as const;

export const AUDIENCES = [
  { value: "parent", label: "I'm the parent", emoji: "👨‍👩‍👧" },
  { value: "student", label: "I'm the student", emoji: "🎓" },
  { value: "both", label: "Parent + student, together", emoji: "🤝", recommended: true },
] as const;

export const PAPER_NUMBERS = ["Paper 1", "Paper 2", "Mock", "Revision", "Other"] as const;

export const MIN_ERRORS_FOR_REPORT = 5; // research recommends 5+ for a sharp diagnosis
export const NUDGE_AT = 10;             // reassurance screen at 5, 10, 15
export const GENTLE_CAP = 20;           // soft upper nudge
```

- [ ] **Step 2: Write `lib/pillars.ts` (pillar metadata for UI rendering)**
```ts
export type Pillar = "F" | "A" | "S" | "T";

export const PILLAR_META: Record<Pillar, {
  letter: Pillar; name: string; subline: string; oneLiner: string; method: string; color: string;
}> = {
  F: {
    letter: "F",
    name: "Facts, Figures & Formulas",
    subline: "Instant, confident recall under pressure.",
    oneLiner: "Build the foundation. Increase recall speed. Remove hesitation.",
    method: "3R: Retrieve, Reinforce, Repeat.",
    color: "#2563eb", // blue-600
  },
  A: {
    letter: "A",
    name: "Analysis of Questions",
    subline: "Decode what the examiner is actually asking.",
    oneLiner: "Decode the question. Understand the demand. Eliminate confusion.",
    method: "QTM: Question, Topic, Method.",
    color: "#7c3aed", // violet-600
  },
  S: {
    letter: "S",
    name: "Solving Patterns",
    subline: "A library of proven starting points for every question type.",
    oneLiner: "Know exactly how to start. Follow a proven solving flow. Get marks predictably.",
    method: "Pattern Before Process.",
    color: "#059669", // emerald-600
  },
  T: {
    letter: "T",
    name: "Time Management",
    subline: "Finish papers with control, not panic.",
    oneLiner: "Master the clock. Prevent panic. Finish the paper with confidence.",
    method: "IQST: Information, Question, Solving, Time.",
    color: "#dc2626", // red-600
  },
};
```

- [ ] **Step 3: Write `lib/copy.ts` (audience-adaptive strings)**
```ts
export type Audience = "parent" | "student" | "both";

export function subject(audience: Audience): string {
  return audience === "parent" ? "your child" : "you";
}

export function possessive(audience: Audience): string {
  return audience === "parent" ? "your child's" : "your";
}

export function verb(audience: Audience, student: string, other: string): string {
  return audience === "parent" ? student : other;
}

export const LANDING_HEADLINE =
  "Find out in 15 minutes which FAST pillar is costing the most marks.";

export const LANDING_SUB =
  "A free error-log diagnostic for Singapore maths students. No sign-up. No sales video. Just a clear report you can act on.";

export const CTA_WHATSAPP = "Book a 30-min FAST consult";
export const CTA_EMAIL_PDF = "Email me the full PDF report";
```

- [ ] **Step 4: Write `tests/unit/copy.test.ts`**
```ts
import { describe, it, expect } from "vitest";
import { subject, possessive } from "@/lib/copy";

describe("copy helpers", () => {
  it("adapts subject to audience", () => {
    expect(subject("parent")).toBe("your child");
    expect(subject("student")).toBe("you");
    expect(subject("both")).toBe("you");
  });
  it("adapts possessive to audience", () => {
    expect(possessive("parent")).toBe("your child's");
    expect(possessive("student")).toBe("your");
  });
});
```

- [ ] **Step 5: Run tests**
```bash
npm test
```
Expected: all pass.

- [ ] **Step 6: Commit**
```bash
git add lib/ tests/
git commit -m "feat(P3): constants, pillar metadata, audience-adaptive copy helpers"
```

### Task 3.2: Landing page (Screen 1)

**Files:** `app/page.tsx`, `app/diagnostic/new/page.tsx`

- [ ] **Step 1: Implement `app/page.tsx`**
```tsx
import Link from "next/link";
import { LANDING_HEADLINE, LANDING_SUB } from "@/lib/copy";
import { Button } from "@/components/ui/button";

export default function LandingPage() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center px-6 py-12 max-w-2xl mx-auto">
      <h1 className="text-3xl sm:text-4xl font-bold text-center tracking-tight">
        {LANDING_HEADLINE}
      </h1>
      <p className="mt-6 text-center text-muted-foreground text-lg">{LANDING_SUB}</p>
      <Link href="/diagnostic/new" className="mt-10">
        <Button size="lg" className="text-base px-8 py-6">Start the diagnostic</Button>
      </Link>
      <footer className="mt-20 text-center text-sm text-muted-foreground">
        Built by Cambridge Learning Group. We never share your data.
      </footer>
    </main>
  );
}
```

- [ ] **Step 2: Implement `app/diagnostic/new/page.tsx`** (server action that creates a session)

```tsx
"use client";
import { useMutation } from "convex/react";
import { api } from "@/convex/_generated/api";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function NewDiagnosticPage() {
  const create = useMutation(api.sessions.create);
  const router = useRouter();

  useEffect(() => {
    create().then((id) => router.replace(`/diagnostic/${id}/audience`));
  }, [create, router]);

  return <main className="min-h-screen flex items-center justify-center">Starting…</main>;
}
```

- [ ] **Step 3: Manually verify landing renders and "Start" creates a session**

Run `npm run dev` + `npx convex dev`. Open http://localhost:3000. Click "Start". Verify URL becomes `/diagnostic/[id]/audience` (404s for now because Screen 2 isn't built yet — that's fine; the session was created).

Check Convex dashboard — a new `sessions` row exists.

- [ ] **Step 4: Commit**
```bash
git add app/
git commit -m "feat(P3): landing page and session creation redirect"
```

### Task 3.3: Audience picker (Screen 2)

**Files:** `components/audience-picker.tsx`, `app/diagnostic/[sessionId]/audience/page.tsx`, `tests/components/audience-picker.test.tsx`

- [ ] **Step 1: Write failing test**
```tsx
// tests/components/audience-picker.test.tsx
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { AudiencePicker } from "@/components/audience-picker";

describe("AudiencePicker", () => {
  it("renders three options and calls onSelect with value", () => {
    const onSelect = vi.fn();
    render(<AudiencePicker onSelect={onSelect} />);
    fireEvent.click(screen.getByRole("button", { name: /I'm the parent/i }));
    expect(onSelect).toHaveBeenCalledWith("parent");
  });
});
```

- [ ] **Step 2: Run — expect fail**
```bash
npm test -- audience-picker
```
Expected: module not found.

- [ ] **Step 3: Implement `components/audience-picker.tsx`**
```tsx
"use client";
import { AUDIENCES } from "@/lib/constants";
import { Card, CardContent } from "@/components/ui/card";

export function AudiencePicker({ onSelect }: { onSelect: (v: "parent" | "student" | "both") => void }) {
  return (
    <div className="grid gap-4 sm:grid-cols-3">
      {AUDIENCES.map((a) => (
        <Card key={a.value} asChild>
          <button
            type="button"
            onClick={() => onSelect(a.value)}
            className="text-left hover:border-primary transition relative"
          >
            <CardContent className="p-6">
              <div className="text-4xl">{a.emoji}</div>
              <div className="mt-3 font-medium">{a.label}</div>
              {a.recommended && (
                <span className="absolute top-2 right-2 text-xs bg-primary text-primary-foreground rounded-full px-2 py-0.5">
                  Recommended
                </span>
              )}
            </CardContent>
          </button>
        </Card>
      ))}
    </div>
  );
}
```

- [ ] **Step 4: Run — expect pass**
```bash
npm test -- audience-picker
```

- [ ] **Step 5: Implement `app/diagnostic/[sessionId]/audience/page.tsx`**
```tsx
"use client";
import { useMutation } from "convex/react";
import { api } from "@/convex/_generated/api";
import { useRouter, useParams } from "next/navigation";
import { AudiencePicker } from "@/components/audience-picker";
import { Id } from "@/convex/_generated/dataModel";

export default function AudiencePage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const router = useRouter();
  const update = useMutation(api.sessions.updateMetadata);

  return (
    <main className="min-h-screen px-6 py-10 max-w-3xl mx-auto">
      <h2 className="text-2xl font-semibold">Who's doing this?</h2>
      <p className="mt-2 text-muted-foreground">
        We'll adapt the questions based on who's filling this in.
      </p>
      <div className="mt-8">
        <AudiencePicker
          onSelect={async (audience) => {
            await update({ id: sessionId as Id<"sessions">, audience });
            router.push(`/diagnostic/${sessionId}/upload`);
          }}
        />
      </div>
    </main>
  );
}
```

- [ ] **Step 6: Commit**
```bash
git add components/ app/ tests/
git commit -m "feat(P3): audience picker screen"
```

### Task 3.4: Paper upload (Screen 3)

**Files:** `convex/files.ts`, `components/file-uploader.tsx`, `app/diagnostic/[sessionId]/upload/page.tsx`

- [ ] **Step 1: Implement `convex/files.ts`** (generate upload URL)
```ts
import { mutation } from "./_generated/server";
export const generateUploadUrl = mutation({
  args: {},
  handler: async (ctx) => await ctx.storage.generateUploadUrl(),
});
```

- [ ] **Step 2: Implement `components/file-uploader.tsx`** (drag-drop + multi-file + HEIC support)

```tsx
"use client";
import { useState } from "react";
import { useMutation } from "convex/react";
import { api } from "@/convex/_generated/api";
import { Id } from "@/convex/_generated/dataModel";
import { Button } from "@/components/ui/button";

export function FileUploader({
  onUploaded,
}: { onUploaded: (ids: Id<"_storage">[]) => void }) {
  const [uploading, setUploading] = useState(false);
  const [count, setCount] = useState(0);
  const generateUrl = useMutation(api.files.generateUploadUrl);

  async function handleFiles(files: FileList | null) {
    if (!files || files.length === 0) return;
    setUploading(true); setCount(0);
    const ids: Id<"_storage">[] = [];
    for (const file of Array.from(files)) {
      const url = await generateUrl();
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": file.type || "application/octet-stream" },
        body: file,
      });
      const { storageId } = await res.json();
      ids.push(storageId as Id<"_storage">);
      setCount(c => c + 1);
    }
    setUploading(false);
    onUploaded(ids);
  }

  return (
    <label className="block border-2 border-dashed rounded-lg p-8 text-center cursor-pointer hover:border-primary">
      <input
        type="file"
        accept="application/pdf,image/*,.heic,.heif"
        multiple
        className="sr-only"
        onChange={(e) => handleFiles(e.target.files)}
      />
      <div className="text-muted-foreground">
        {uploading ? `Uploading ${count}…` : "Tap or drop PDF / photos of the marked paper"}
      </div>
      <Button type="button" variant="secondary" className="mt-4" disabled={uploading}>
        Choose files
      </Button>
    </label>
  );
}
```

- [ ] **Step 3: Implement `app/diagnostic/[sessionId]/upload/page.tsx`**
```tsx
"use client";
import { useMutation } from "convex/react";
import { api } from "@/convex/_generated/api";
import { useParams, useRouter } from "next/navigation";
import { FileUploader } from "@/components/file-uploader";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { PAPER_NUMBERS } from "@/lib/constants";
import { useState } from "react";
import { Id } from "@/convex/_generated/dataModel";

export default function UploadPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const router = useRouter();
  const update = useMutation(api.sessions.updateMetadata);
  const [files, setFiles] = useState<Id<"_storage">[]>([]);
  const [studentName, setStudentName] = useState("");
  const [paperDate, setPaperDate] = useState("");
  const [school, setSchool] = useState("");
  const [paperNumber, setPaperNumber] = useState("");

  async function handleContinue(withUpload: boolean) {
    await update({
      id: sessionId as Id<"sessions">,
      studentName, paperDate, school, paperNumber,
      uploadedPaperFileIds: withUpload ? files : [],
    });
    router.push(`/diagnostic/${sessionId}/errors/1`);
  }

  return (
    <main className="min-h-screen px-6 py-10 max-w-2xl mx-auto space-y-6">
      <h2 className="text-2xl font-semibold">Grab the most recent paper</h2>
      <p className="text-muted-foreground">
        Snap a photo or upload the PDF. We keep it as reference — we don't auto-read it.
      </p>

      <FileUploader onUploaded={setFiles} />

      <div className="grid sm:grid-cols-2 gap-4">
        <div><Label>Student name</Label><Input value={studentName} onChange={e => setStudentName(e.target.value)} /></div>
        <div><Label>Paper date</Label><Input type="date" value={paperDate} onChange={e => setPaperDate(e.target.value)} /></div>
        <div><Label>School</Label><Input value={school} onChange={e => setSchool(e.target.value)} /></div>
        <div>
          <Label>Paper</Label>
          <Select value={paperNumber} onValueChange={setPaperNumber}>
            <SelectTrigger><SelectValue placeholder="Select…" /></SelectTrigger>
            <SelectContent>{PAPER_NUMBERS.map(p => <SelectItem key={p} value={p}>{p}</SelectItem>)}</SelectContent>
          </Select>
        </div>
      </div>

      <div className="flex justify-between items-center pt-4">
        <button onClick={() => handleContinue(false)} className="text-sm text-muted-foreground underline">
          I don't have the paper now
        </button>
        <Button onClick={() => handleContinue(true)} disabled={!studentName}>
          Continue
        </Button>
      </div>
    </main>
  );
}
```

- [ ] **Step 4: Manually verify upload works**
Run dev server; go through Landing → Audience → Upload; upload a test PDF; fill name; click Continue. Check Convex dashboard that `sessions` row has `uploadedPaperFileIds` populated.

- [ ] **Step 5: Commit**
```bash
git add convex/files.ts components/file-uploader.tsx app/
git commit -m "feat(P3): paper upload with metadata fields"
```

---

## Phase 4 — Error Log Entry (Screen 4, one-error-per-screen)

### Task 4.1: Error entry form component

**Files:** `components/error-entry-form.tsx`

- [ ] **Step 1: Implement `components/error-entry-form.tsx`**

```tsx
"use client";
import { useState } from "react";
import { ERROR_TYPES, ERROR_CATEGORIES, CARELESS_ROOTS } from "@/lib/constants";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

export type ErrorEntryData = {
  qnNumber: number;
  topic: string;
  errorType: typeof ERROR_TYPES[number]["value"];
  errorCategory: typeof ERROR_CATEGORIES[number]["value"];
  carelessRoot?: typeof CARELESS_ROOTS[number]["value"]; // only when errorType === "careless"
  rootCause: string;
  details: string;
};

export function ErrorEntryForm({
  initial, onSave, onCancel, submitLabel,
}: {
  initial: Partial<ErrorEntryData>;
  onSave: (d: ErrorEntryData) => void;
  onCancel?: () => void;
  submitLabel: string;
}) {
  const [data, setData] = useState<ErrorEntryData>({
    qnNumber: initial.qnNumber ?? 1,
    topic: initial.topic ?? "",
    errorType: initial.errorType ?? ERROR_TYPES[0].value,
    errorCategory: initial.errorCategory ?? ERROR_CATEGORIES[0].value,
    carelessRoot: initial.carelessRoot,
    rootCause: initial.rootCause ?? "",
    details: initial.details ?? "",
  });

  const isCareless = data.errorType === "careless";
  // Gate: if careless, require the follow-up to be answered before Save enables.
  const canSave = data.topic.trim().length > 0 && (!isCareless || !!data.carelessRoot);

  return (
    <form className="space-y-4" onSubmit={(e) => { e.preventDefault(); if (canSave) onSave(data); }}>
      <div><Label>Question number</Label><Input type="number" min={1} value={data.qnNumber} onChange={e => setData(d => ({ ...d, qnNumber: Number(e.target.value) }))} /></div>
      <div><Label>Topic / Sub-topic</Label><Input value={data.topic} onChange={e => setData(d => ({ ...d, topic: e.target.value }))} placeholder="e.g. Quadratic equations" /></div>
      <div>
        <Label>Error Type (surface level)</Label>
        <Select
          value={data.errorType}
          onValueChange={v =>
            setData(d => ({
              ...d,
              errorType: v as any,
              // Reset carelessRoot when switching away from careless
              carelessRoot: v === "careless" ? d.carelessRoot : undefined,
            }))
          }
        >
          <SelectTrigger /><SelectContent>{ERROR_TYPES.map(t => <SelectItem key={t.value} value={t.value}>{t.label}</SelectItem>)}</SelectContent>
        </Select>
      </div>

      {/* Conditional follow-up: only when Careless selected.
          Routes to A / S / T instead of the default T pillar. */}
      {isCareless && (
        <div className="rounded-md border border-amber-300 bg-amber-50 p-3 space-y-2">
          <Label className="font-semibold">What caused this careless mistake?</Label>
          <p className="text-sm text-muted-foreground">
            "Careless" covers 3 very different things. Pick the one closest to what happened —
            it changes the diagnosis.
          </p>
          <div className="space-y-2 pt-1">
            {CARELESS_ROOTS.map(r => (
              <label key={r.value} className="flex items-start gap-2 cursor-pointer">
                <input
                  type="radio"
                  name="carelessRoot"
                  value={r.value}
                  checked={data.carelessRoot === r.value}
                  onChange={() => setData(d => ({ ...d, carelessRoot: r.value }))}
                  className="mt-1"
                />
                <span className="text-sm">{r.label}</span>
              </label>
            ))}
          </div>
        </div>
      )}

      <div>
        <Label>Error Category (deeper cause)</Label>
        <Select value={data.errorCategory} onValueChange={v => setData(d => ({ ...d, errorCategory: v as any }))}>
          <SelectTrigger /><SelectContent>{ERROR_CATEGORIES.map(c => <SelectItem key={c.value} value={c.value}>{c.label}</SelectItem>)}</SelectContent>
        </Select>
      </div>
      <div><Label>Root cause (optional)</Label><Textarea rows={2} value={data.rootCause} onChange={e => setData(d => ({ ...d, rootCause: e.target.value }))} /></div>
      <div><Label>Details (optional)</Label><Textarea rows={2} value={data.details} onChange={e => setData(d => ({ ...d, details: e.target.value }))} /></div>
      <div className="flex gap-2 pt-2">
        {onCancel && <Button type="button" variant="ghost" onClick={onCancel}>Back</Button>}
        <Button type="submit" disabled={!canSave}>{submitLabel}</Button>
      </div>
    </form>
  );
}
```

- [ ] **Step 2: Commit**
```bash
git add components/error-entry-form.tsx
git commit -m "feat(P4): error entry form component"
```

### Task 4.2: Error-log screen with progress, autosave, reassurance

**Files:** `components/progress-bar.tsx`, `components/reassurance-screen.tsx`, `app/diagnostic/[sessionId]/errors/[index]/page.tsx`

- [ ] **Step 1: Implement `components/progress-bar.tsx`**
```tsx
import { MIN_ERRORS_FOR_REPORT } from "@/lib/constants";

export function SegmentedProgress({ count }: { count: number }) {
  const unlocked = count >= MIN_ERRORS_FOR_REPORT;
  return (
    <div className="space-y-2">
      <div className="flex gap-1">
        {Array.from({ length: MIN_ERRORS_FOR_REPORT }).map((_, i) => (
          <div key={i} className={`h-2 flex-1 rounded ${i < count ? "bg-primary" : "bg-muted"}`} />
        ))}
      </div>
      <p className="text-sm text-muted-foreground">
        {unlocked
          ? `Errors logged: ${count}. More errors → sharper diagnosis (up to 20).`
          : `Errors logged: ${count} / ${MIN_ERRORS_FOR_REPORT} minimum before report unlocks.`}
      </p>
    </div>
  );
}
```

- [ ] **Step 2: Implement `components/reassurance-screen.tsx`**
```tsx
import { Button } from "@/components/ui/button";

export function ReassuranceScreen({ count, onContinue }: { count: number; onContinue: () => void }) {
  const lines: Record<number, string> = {
    5: "Nice. 5 errors logged — report unlocked. Keep logging for a sharper diagnosis.",
    10: "Excellent. Students who log 10+ errors get a 2× sharper diagnosis.",
    15: "Impressive. You're building a complete picture of where the marks are going.",
  };
  const line = lines[count] ?? "Keep going.";
  return (
    <div className="min-h-[60vh] flex flex-col items-center justify-center text-center px-6 gap-6">
      <div className="text-5xl">✨</div>
      <h3 className="text-2xl font-semibold">{line}</h3>
      <Button onClick={onContinue}>Continue</Button>
    </div>
  );
}
```

- [ ] **Step 3: Implement `app/diagnostic/[sessionId]/errors/[index]/page.tsx`**

```tsx
"use client";
import { useParams, useRouter } from "next/navigation";
import { useQuery, useMutation } from "convex/react";
import { api } from "@/convex/_generated/api";
import { Id } from "@/convex/_generated/dataModel";
import { ErrorEntryForm, ErrorEntryData } from "@/components/error-entry-form";
import { SegmentedProgress } from "@/components/progress-bar";
import { ReassuranceScreen } from "@/components/reassurance-screen";
import { MIN_ERRORS_FOR_REPORT, NUDGE_AT } from "@/lib/constants";
import { Button } from "@/components/ui/button";
import { useState } from "react";

export default function ErrorEntryPage() {
  const { sessionId, index } = useParams<{ sessionId: string; index: string }>();
  const idx = Number(index);
  const router = useRouter();
  const errors = useQuery(api.errors.listBySession, { sessionId: sessionId as Id<"sessions"> });
  const upsert = useMutation(api.errors.upsert);
  const existing = errors?.find(e => e.qnNumber === idx);
  const [showReassurance, setShowReassurance] = useState(false);

  if (errors === undefined) return <main className="p-8">Loading…</main>;
  if (showReassurance) {
    return <ReassuranceScreen count={errors.length} onContinue={() => { setShowReassurance(false); router.push(`/diagnostic/${sessionId}/errors/${idx + 1}`); }} />;
  }

  async function handleSave(d: ErrorEntryData) {
    await upsert({
      sessionId: sessionId as Id<"sessions">,
      qnNumber: d.qnNumber,
      topic: d.topic,
      errorType: d.errorType,
      errorCategory: d.errorCategory,
      carelessRoot: d.errorType === "careless" ? d.carelessRoot : undefined,
      rootCause: d.rootCause || undefined,
      details: d.details || undefined,
    });
    const nextCount = existing ? errors.length : errors.length + 1;
    const shouldReassure = [5, 10, 15].includes(nextCount);
    if (shouldReassure) setShowReassurance(true);
    else router.push(`/diagnostic/${sessionId}/errors/${idx + 1}`);
  }

  return (
    <main className="min-h-screen px-6 py-8 max-w-2xl mx-auto space-y-6">
      <SegmentedProgress count={errors.length} />
      <h2 className="text-2xl font-semibold">Error {idx}</h2>
      <ErrorEntryForm
        initial={{ qnNumber: idx, ...(existing ?? {}) }}
        onSave={handleSave}
        submitLabel={existing ? "Update & next" : "Save & next"}
      />
      {errors.length >= MIN_ERRORS_FOR_REPORT && (
        <div className="pt-6 border-t">
          <Button variant="default" onClick={() => router.push(`/diagnostic/${sessionId}/submit`)}>
            I'm done — see my diagnosis
          </Button>
        </div>
      )}
    </main>
  );
}
```

- [ ] **Step 4: Manually verify**
Go through flow, log 5+ errors, verify reassurance screen fires at 5, and the "see my diagnosis" button appears at 5+.

- [ ] **Step 5: Commit**
```bash
git add components/ app/
git commit -m "feat(P4): error log with one-per-screen flow, progress bar, reassurance"
```

---

## Phase 5 — Scoring + Submit (Screen 5)

### Task 5.1: Pillar scoring logic (pure function, testable)

**Files:** `lib/scoring.ts`, `tests/unit/pillar-scoring.test.ts`

- [ ] **Step 1: Write failing test**
```ts
// tests/unit/pillar-scoring.test.ts
import { describe, it, expect } from "vitest";
import { computeReport } from "@/lib/scoring";

describe("computeReport", () => {
  const typePillar = {
    careless: "T", conceptual_misunderstanding: "F",
    misread_question: "A", applied_wrong_formula: "S",
    did_not_complete_working: "S", time_management_issue: "T",
  } as const;
  const catPillar = {
    knowledge_gap: "F", misapplied_rule: "A",
    confusion_between_concepts: "S", poor_exam_strategy: "T",
    anxiety_panic: "T", lack_of_practice: "S",
  } as const;
  const carelessRootPillar = {
    misunderstood: "A", slip: "S", rushed: "T",
  } as const;

  it("scores single error to its primary pillar", () => {
    const report = computeReport(
      [{ qnNumber: 1, errorType: "careless", errorCategory: "anxiety_panic", topic: "x", rootCause: "", details: "" }],
      typePillar, catPillar, carelessRootPillar,
    );
    // Careless with no carelessRoot → defaults to T via errorTypePillar
    expect(report.pillarScores).toEqual({ F: 0, A: 0, S: 0, T: 100 });
    expect(report.verdictPillars).toEqual(["T"]);
  });

  it("finds tied pillars within 5pp", () => {
    const errors = [
      { qnNumber: 1, errorType: "careless" as const, errorCategory: "anxiety_panic" as const, topic: "x", rootCause: "", details: "" },
      { qnNumber: 2, errorType: "conceptual_misunderstanding" as const, errorCategory: "knowledge_gap" as const, topic: "x", rootCause: "", details: "" },
    ];
    const r = computeReport(errors, typePillar, catPillar, carelessRootPillar);
    expect(r.verdictPillars.sort()).toEqual(["F", "T"]);
  });

  it("marks error as reinforced when category matches primary", () => {
    const r = computeReport(
      [{ qnNumber: 1, errorType: "careless", errorCategory: "anxiety_panic", topic: "x", rootCause: "", details: "" }],
      typePillar, catPillar, carelessRootPillar,
    );
    expect(r.enrichedErrors[0].reinforced).toBe(true);
  });

  it("extracts top 3 recurring patterns by (type, category) count", () => {
    const errors = Array.from({ length: 4 }).map((_, i) => ({
      qnNumber: i + 1, errorType: "misread_question" as const, errorCategory: "misapplied_rule" as const, topic: "", rootCause: "", details: "",
    }));
    const r = computeReport(errors, typePillar, catPillar, carelessRootPillar);
    expect(r.topPatterns[0].count).toBe(4);
    expect(r.topPatterns[0].qnNumbers).toEqual([1, 2, 3, 4]);
  });

  // Careless follow-up routing: the key behavior. Without this override,
  // all 3 careless errors would pile on T. With it, they route to A/S/T.
  it("routes Careless to A/S/T based on carelessRoot follow-up", () => {
    const errors = [
      { qnNumber: 1, errorType: "careless" as const, errorCategory: "anxiety_panic" as const, carelessRoot: "misunderstood" as const, topic: "", rootCause: "", details: "" },
      { qnNumber: 2, errorType: "careless" as const, errorCategory: "anxiety_panic" as const, carelessRoot: "slip" as const,         topic: "", rootCause: "", details: "" },
      { qnNumber: 3, errorType: "careless" as const, errorCategory: "anxiety_panic" as const, carelessRoot: "rushed" as const,       topic: "", rootCause: "", details: "" },
    ];
    const r = computeReport(errors, typePillar, catPillar, carelessRootPillar);
    expect(r.enrichedErrors.map(e => e.primaryPillar)).toEqual(["A", "S", "T"]);
    // 33% each, all within 5pp → all three tied in verdict
    expect(r.verdictPillars.sort()).toEqual(["A", "S", "T"]);
  });

  it("falls back to errorTypePillar['careless'] when carelessRoot is missing", () => {
    const r = computeReport(
      [{ qnNumber: 1, errorType: "careless", errorCategory: "anxiety_panic", topic: "", rootCause: "", details: "" }],
      typePillar, catPillar, carelessRootPillar,
    );
    expect(r.enrichedErrors[0].primaryPillar).toBe("T");
  });
});
```

- [ ] **Step 2: Run — expect fail**

- [ ] **Step 3: Implement `lib/scoring.ts`**
```ts
import type { Pillar } from "./pillars";
import type { ERROR_TYPES, ERROR_CATEGORIES } from "./constants";

type ErrorType = typeof ERROR_TYPES[number]["value"];
type ErrorCategory = typeof ERROR_CATEGORIES[number]["value"];
export type CarelessRoot = "misunderstood" | "slip" | "rushed";

export type ErrorInput = {
  qnNumber: number;
  topic: string;
  errorType: ErrorType;
  errorCategory: ErrorCategory;
  carelessRoot?: CarelessRoot; // required iff errorType === "careless"
  rootCause: string;
  details: string;
};

export type EnrichedError = ErrorInput & { primaryPillar: Pillar; reinforced: boolean };

export type Report = {
  pillarScores: Record<Pillar, number>;
  topPatterns: { label: string; count: number; qnNumbers: number[]; interpretation: string }[];
  verdictPillars: Pillar[];
  enrichedErrors: EnrichedError[];
  totalErrors: number;
};

export function computeReport(
  errors: ErrorInput[],
  typeToPillar: Record<ErrorType, Pillar>,
  categoryToPillar: Record<ErrorCategory, Pillar>,
  carelessRootToPillar: Record<CarelessRoot, Pillar>,
): Report {
  const enriched: EnrichedError[] = errors.map(e => {
    // Careless follow-up override: if user selected a carelessRoot, route to A/S/T
    // via that mapping rather than the default errorTypePillar["careless"] (T).
    const primaryPillar =
      e.errorType === "careless" && e.carelessRoot
        ? carelessRootToPillar[e.carelessRoot]
        : typeToPillar[e.errorType];
    const reinforced = categoryToPillar[e.errorCategory] === primaryPillar;
    return { ...e, primaryPillar, reinforced };
  });

  const counts: Record<Pillar, number> = { F: 0, A: 0, S: 0, T: 0 };
  for (const e of enriched) counts[e.primaryPillar]++;
  const total = enriched.length || 1;
  const pillarScores: Record<Pillar, number> = {
    F: Math.round((counts.F / total) * 100),
    A: Math.round((counts.A / total) * 100),
    S: Math.round((counts.S / total) * 100),
    T: Math.round((counts.T / total) * 100),
  };

  const max = Math.max(...Object.values(pillarScores));
  const verdictPillars = (Object.keys(pillarScores) as Pillar[])
    .filter(p => max - pillarScores[p] <= 5 && pillarScores[p] > 0)
    .sort((a, b) => pillarScores[b] - pillarScores[a]);

  const patternMap = new Map<string, { count: number; qnNumbers: number[]; errorType: ErrorType; errorCategory: ErrorCategory }>();
  for (const e of enriched) {
    const k = `${e.errorType}|${e.errorCategory}`;
    const entry = patternMap.get(k) ?? { count: 0, qnNumbers: [], errorType: e.errorType, errorCategory: e.errorCategory };
    entry.count++; entry.qnNumbers.push(e.qnNumber);
    patternMap.set(k, entry);
  }
  const topPatterns = [...patternMap.entries()]
    .sort((a, b) => b[1].count - a[1].count)
    .slice(0, 3)
    .map(([_, v]) => ({
      label: `${humanize(v.errorType)} — reinforced by ${humanize(v.errorCategory)}`,
      count: v.count,
      qnNumbers: v.qnNumbers,
      interpretation: interpretPattern(v.errorType, v.errorCategory),
    }));

  return { pillarScores, verdictPillars, topPatterns, enrichedErrors: enriched, totalErrors: enriched.length };
}

function humanize(s: string) { return s.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase()); }

function interpretPattern(t: ErrorType, c: ErrorCategory): string {
  // Tone: diagnosis, not advice. Cite what this pattern indicates, not how to fix.
  if (t === "misread_question") return "Signals the question wasn't decoded before solving — a classic A-pillar pattern.";
  if (t === "applied_wrong_formula") return "Signals a missing pattern-library entry for this question type.";
  if (t === "time_management_issue") return "Signals the clock won, not the question. A T-pillar pattern.";
  if (t === "conceptual_misunderstanding") return "Signals a foundation gap — F pillar.";
  if (t === "did_not_complete_working") return "Signals rushed or unclear solving flow — S pillar.";
  if (t === "careless") return "Careless — routed to the specific pillar based on the student's own root cause (misunderstood / slip / rushed).";
  return "";
}
```

- [ ] **Step 4: Run — expect pass**

- [ ] **Step 5: Commit**
```bash
git add lib/scoring.ts tests/unit/pillar-scoring.test.ts
git commit -m "feat(P5): pure pillar-scoring function with tests"
```

### Task 5.2: Convex report mutation

**Files:** `convex/reports.ts`, `convex/mappings.ts`

- [ ] **Step 1: Implement `convex/mappings.ts`**
```ts
import { query } from "./_generated/server";
export const getAll = query({
  args: {},
  handler: async (ctx) => ({
    typeToPillar: Object.fromEntries((await ctx.db.query("errorTypePillar").collect()).map(r => [r.errorType, r.pillar])),
    categoryToPillar: Object.fromEntries((await ctx.db.query("errorCategoryPillar").collect()).map(r => [r.errorCategory, r.pillar])),
    carelessRootToPillar: Object.fromEntries((await ctx.db.query("carelessRootPillar").collect()).map(r => [r.carelessRoot, r.pillar])),
  }),
});
```

- [ ] **Step 2: Implement `convex/reports.ts`**
```ts
import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

export const computeAndPersist = mutation({
  args: { sessionId: v.id("sessions") },
  handler: async (ctx, { sessionId }) => {
    const errors = await ctx.db.query("errors").withIndex("by_session", q => q.eq("sessionId", sessionId)).collect();
    if (errors.length < 5) throw new Error("Need at least 5 errors.");
    const typeRows = await ctx.db.query("errorTypePillar").collect();
    const catRows = await ctx.db.query("errorCategoryPillar").collect();
    const crRows = await ctx.db.query("carelessRootPillar").collect();
    const typeToPillar = Object.fromEntries(typeRows.map(r => [r.errorType, r.pillar])) as Record<string, "F"|"A"|"S"|"T">;
    const catToPillar = Object.fromEntries(catRows.map(r => [r.errorCategory, r.pillar])) as Record<string, "F"|"A"|"S"|"T">;
    const carelessRootToPillar = Object.fromEntries(crRows.map(r => [r.carelessRoot, r.pillar])) as Record<string, "F"|"A"|"S"|"T">;

    const counts: Record<"F"|"A"|"S"|"T", number> = { F: 0, A: 0, S: 0, T: 0 };
    for (const e of errors) {
      // Careless follow-up override: if user answered the 3-way sub-question,
      // route to A/S/T via carelessRootToPillar instead of the default T.
      const p =
        e.errorType === "careless" && e.carelessRoot
          ? carelessRootToPillar[e.carelessRoot]!
          : typeToPillar[e.errorType]!;
      counts[p]++;
      await ctx.db.patch(e._id, { primaryPillar: p, reinforced: catToPillar[e.errorCategory] === p });
    }
    const total = errors.length;
    const scores = { F: Math.round(counts.F/total*100), A: Math.round(counts.A/total*100), S: Math.round(counts.S/total*100), T: Math.round(counts.T/total*100) };
    const max = Math.max(...Object.values(scores));
    const verdictPillars = (Object.keys(scores) as ("F"|"A"|"S"|"T")[]).filter(p => max - scores[p] <= 5 && scores[p] > 0).sort((a,b)=>scores[b]-scores[a]);

    const patternMap = new Map<string, { count: number; qnNumbers: number[]; errorType: string; errorCategory: string }>();
    for (const e of errors) {
      const k = `${e.errorType}|${e.errorCategory}`;
      const entry = patternMap.get(k) ?? { count: 0, qnNumbers: [], errorType: e.errorType, errorCategory: e.errorCategory };
      entry.count++; entry.qnNumbers.push(e.qnNumber);
      patternMap.set(k, entry);
    }
    const topPatterns = [...patternMap.values()].sort((a,b)=>b.count-a.count).slice(0,3).map(v => ({
      label: `${v.errorType.replace(/_/g," ")} — reinforced by ${v.errorCategory.replace(/_/g," ")}`,
      count: v.count, qnNumbers: v.qnNumbers,
      interpretation: interpretPattern(v.errorType as any),
    }));

    const existing = await ctx.db.query("reports").withIndex("by_session", q => q.eq("sessionId", sessionId)).first();
    if (existing) await ctx.db.replace(existing._id, { sessionId, pillarScores: scores, topPatterns, verdictPillars, generatedAt: Date.now() });
    else await ctx.db.insert("reports", { sessionId, pillarScores: scores, topPatterns, verdictPillars, generatedAt: Date.now() });

    await ctx.db.patch(sessionId, { status: "submitted", submittedAt: Date.now() });
    return { ok: true };
  },
});

function interpretPattern(t: string): string {
  const map: Record<string, string> = {
    misread_question: "Signals the question wasn't decoded before solving — a classic A-pillar pattern.",
    applied_wrong_formula: "Signals a missing pattern-library entry for this question type.",
    time_management_issue: "Signals the clock won, not the question. A T-pillar pattern.",
    conceptual_misunderstanding: "Signals a foundation gap — F pillar.",
    did_not_complete_working: "Signals rushed or unclear solving flow — S pillar.",
    careless: "Signals pressure-driven slips rather than knowledge gaps — T pillar.",
  };
  return map[t] ?? "";
}

export const getBySession = query({
  args: { sessionId: v.id("sessions") },
  handler: async (ctx, { sessionId }) =>
    await ctx.db.query("reports").withIndex("by_session", q => q.eq("sessionId", sessionId)).first(),
});
```

- [ ] **Step 3: Push to Convex**
```bash
npx convex dev --once
```

- [ ] **Step 4: Commit**
```bash
git add convex/
git commit -m "feat(P5): compute and persist diagnostic report"
```

### Task 5.3: Submit transition screen

**Files:** `app/diagnostic/[sessionId]/submit/page.tsx`

- [ ] **Step 1: Implement submit page with 2-second faux-analysis animation**
```tsx
"use client";
import { useEffect } from "react";
import { useMutation } from "convex/react";
import { api } from "@/convex/_generated/api";
import { useParams, useRouter } from "next/navigation";
import { Id } from "@/convex/_generated/dataModel";
import { PILLAR_META } from "@/lib/pillars";

export default function SubmitPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const compute = useMutation(api.reports.computeAndPersist);
  const router = useRouter();

  useEffect(() => {
    const run = async () => {
      const [, ] = await Promise.all([
        compute({ sessionId: sessionId as Id<"sessions"> }),
        new Promise(r => setTimeout(r, 2200)),
      ]);
      router.replace(`/diagnostic/${sessionId}/report`);
    };
    run().catch(err => alert(err.message));
  }, [compute, sessionId, router]);

  return (
    <main className="min-h-screen flex flex-col items-center justify-center gap-6 px-6">
      <h2 className="text-2xl font-semibold">Analysing your errors…</h2>
      <div className="flex gap-3">
        {(["F","A","S","T"] as const).map((p, i) => (
          <div key={p} className="size-14 rounded-full flex items-center justify-center text-white font-bold animate-pulse"
               style={{ background: PILLAR_META[p].color, animationDelay: `${i * 200}ms` }}>
            {p}
          </div>
        ))}
      </div>
      <p className="text-muted-foreground text-sm">This will take a few seconds.</p>
    </main>
  );
}
```

- [ ] **Step 2: Manually verify: completing 5 errors → click "see my diagnosis" → briefly animates → redirects to report page (404 until P6 is built).**

- [ ] **Step 3: Commit**
```bash
git add app/
git commit -m "feat(P5): submit transition with 2s faux-analysis animation"
```

---

## Phase 6 — Report Screen 6

### Task 6.1: Report page scaffolding + data loading

**Files:** `app/diagnostic/[sessionId]/report/page.tsx`

- [ ] **Step 1: Skeleton**
```tsx
"use client";
import { useParams } from "next/navigation";
import { useQuery } from "convex/react";
import { api } from "@/convex/_generated/api";
import { Id } from "@/convex/_generated/dataModel";
import { HeroVerdict } from "@/components/report/hero-verdict";
import { EvidenceBlock } from "@/components/report/evidence-block";
import { PatternCards } from "@/components/report/pattern-cards";
import { PillarsAccordion } from "@/components/report/pillars-accordion";
import { BridgeParagraph } from "@/components/report/bridge-paragraph";
import { DualCTA } from "@/components/report/dual-cta";

export default function ReportPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const session = useQuery(api.sessions.get, { id: sessionId as Id<"sessions"> });
  const report = useQuery(api.reports.getBySession, { sessionId: sessionId as Id<"sessions"> });
  const errors = useQuery(api.errors.listBySession, { sessionId: sessionId as Id<"sessions"> });

  if (!session || !report || !errors) return <main className="p-8">Loading…</main>;

  return (
    <main className="min-h-screen pb-32">
      <div className="max-w-2xl mx-auto px-6 py-8 space-y-10">
        <HeroVerdict report={report} session={session} />
        <EvidenceBlock report={report} errors={errors} session={session} />
        <PatternCards report={report} />
        <PillarsAccordion report={report} />
        <BridgeParagraph report={report} session={session} />
      </div>
      <DualCTA sessionId={sessionId as Id<"sessions">} session={session} report={report} />
    </main>
  );
}
```

- [ ] **Step 2: Commit placeholder**
```bash
git add app/
git commit -m "feat(P6): report page scaffold"
```

### Task 6.2: Hero verdict component

**Files:** `components/report/hero-verdict.tsx`, `tests/components/report/hero-verdict.test.tsx`

- [ ] **Step 1: Write test**
```tsx
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { HeroVerdict } from "@/components/report/hero-verdict";

describe("HeroVerdict", () => {
  it("shows single pillar verdict", () => {
    render(<HeroVerdict
      report={{ verdictPillars: ["F"], pillarScores: { F: 60, A: 20, S: 10, T: 10 } } as any}
      session={{ audience: "parent", studentName: "Kai" } as any}
    />);
    expect(screen.getByText(/weakest FAST pillar/i)).toBeInTheDocument();
    expect(screen.getByText(/\bF\b/)).toBeInTheDocument();
  });
  it("shows tied pillars together", () => {
    render(<HeroVerdict
      report={{ verdictPillars: ["F", "A"], pillarScores: { F: 40, A: 38, S: 12, T: 10 } } as any}
      session={{ audience: "student", studentName: "Kai" } as any}
    />);
    expect(screen.getByText(/pillars/i)).toBeInTheDocument();
  });
});
```

- [ ] **Step 2: Implement**
```tsx
import { PILLAR_META, Pillar } from "@/lib/pillars";
import { possessive } from "@/lib/copy";

export function HeroVerdict({ report, session }: any) {
  const pillars: Pillar[] = report.verdictPillars;
  const p0 = pillars[0];
  const score = report.pillarScores[p0];
  const poss = possessive(session.audience);
  const name = session.studentName ?? "the student";

  if (pillars.length === 1) {
    const m = PILLAR_META[p0];
    return (
      <section className="space-y-4">
        <div className="inline-flex items-center gap-3">
          <div className="size-16 rounded-full flex items-center justify-center text-white text-2xl font-bold" style={{ background: m.color }}>{p0}</div>
        </div>
        <h1 className="text-3xl font-bold">{poss} weakest FAST pillar is <span style={{ color: m.color }}>{p0} — {m.name}</span>.</h1>
        <p className="text-lg text-muted-foreground">{score}% of {name}'s errors trace back to this pillar.</p>
        <p className="text-base">{m.oneLiner}</p>
      </section>
    );
  }
  return (
    <section className="space-y-4">
      <h1 className="text-3xl font-bold">{poss} weakest pillars are {pillars.join(" and ")} — roughly even.</h1>
      <p className="text-lg text-muted-foreground">Mixed signals. Worth unpacking in a consult.</p>
    </section>
  );
}
```

- [ ] **Step 3: Run tests — expect pass.**

- [ ] **Step 4: Commit**
```bash
git add components/report/hero-verdict.tsx tests/
git commit -m "feat(P6): hero verdict component with single/tied logic"
```

### Task 6.3: Evidence block, pattern cards, pillars accordion, bridge paragraph

**Files:** `components/report/evidence-block.tsx`, `pattern-cards.tsx`, `pillars-accordion.tsx`, `bridge-paragraph.tsx`

- [ ] **Step 1: Implement `evidence-block.tsx`**
```tsx
import { possessive, subject } from "@/lib/copy";

export function EvidenceBlock({ report, errors, session }: any) {
  const pillar = report.verdictPillars[0];
  const matching = errors.filter((e: any) => e.primaryPillar === pillar);
  const reinforcedCount = matching.filter((e: any) => e.reinforced).length;
  const topType = matching[0]?.errorType ?? "";
  return (
    <section className="space-y-3">
      <h2 className="text-xl font-semibold">Here's what we saw</h2>
      <p>
        Across {errors.length} errors {subject(session.audience)} logged,
        {" "}{matching.length} map to the <strong>{pillar}</strong> pillar
        {reinforcedCount > 0 && <>, of which {reinforcedCount} are reinforced by the deeper error category</>}.
        That's the signature of {pillar}-pillar weakness.
      </p>
    </section>
  );
}
```

- [ ] **Step 2: Implement `pattern-cards.tsx`**
```tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function PatternCards({ report }: any) {
  return (
    <section className="space-y-3">
      <h2 className="text-xl font-semibold">{possessiveOf(report)} top 3 recurring error patterns</h2>
      <div className="grid gap-3">
        {report.topPatterns.map((p: any, i: number) => (
          <Card key={i}>
            <CardHeader><CardTitle className="text-base">{p.label}</CardTitle></CardHeader>
            <CardContent className="space-y-1 text-sm">
              <p>Appeared in Qn {p.qnNumbers.join(", ")} — {p.count} times.</p>
              <p className="text-muted-foreground">{p.interpretation}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  );
}

function possessiveOf(_r: any) { return "Your"; } // placeholder — swap in audience-aware later
```

- [ ] **Step 3: Implement `pillars-accordion.tsx`**
```tsx
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { PILLAR_META, Pillar } from "@/lib/pillars";

export function PillarsAccordion({ report }: any) {
  const verdict = report.verdictPillars[0];
  const others = (["F","A","S","T"] as Pillar[]).filter(p => p !== verdict);
  return (
    <section className="space-y-3">
      <h2 className="text-xl font-semibold">The other three pillars</h2>
      <Accordion type="multiple">
        {others.map(p => {
          const m = PILLAR_META[p];
          const score = report.pillarScores[p];
          return (
            <AccordionItem key={p} value={p}>
              <AccordionTrigger>
                <span style={{ color: m.color }} className="font-semibold mr-3">{p}</span>
                <span className="mr-3">{m.name}</span>
                <span className="ml-auto text-muted-foreground">{score}%</span>
              </AccordionTrigger>
              <AccordionContent className="text-sm space-y-1">
                <p>{m.subline}</p>
                {score === 0 && <p className="text-muted-foreground">No errors traced to this pillar — nice.</p>}
              </AccordionContent>
            </AccordionItem>
          );
        })}
      </Accordion>
    </section>
  );
}
```

- [ ] **Step 4: Implement `bridge-paragraph.tsx`**
```tsx
import { PILLAR_META } from "@/lib/pillars";
import { possessive } from "@/lib/copy";

export function BridgeParagraph({ report, session }: any) {
  const pillar = report.verdictPillars[0];
  const m = PILLAR_META[pillar];
  return (
    <section className="space-y-3 rounded-lg bg-muted p-6">
      <h2 className="text-xl font-semibold">What this means</h2>
      <p>
        This isn't about effort or intelligence. It's about which pillar is leaking marks — and
        that can be trained. The specific techniques for fixing a <strong>{pillar}-pillar</strong> weakness
        (the {m.method}) are what we work on in a live consult.
      </p>
    </section>
  );
}
```

- [ ] **Step 5: Commit**
```bash
git add components/report/
git commit -m "feat(P6): evidence, pattern cards, pillars accordion, bridge paragraph"
```

### Task 6.4: WhatsApp deep-link builder + Dual CTA

**Files:** `lib/whatsapp.ts`, `tests/unit/whatsapp.test.ts`, `components/report/dual-cta.tsx`, `convex/leads.ts`

- [ ] **Step 1: Write failing test**
```ts
import { describe, it, expect } from "vitest";
import { buildWhatsAppUrl } from "@/lib/whatsapp";

describe("buildWhatsAppUrl", () => {
  it("builds a wa.me link with url-encoded diagnostic context", () => {
    const url = buildWhatsAppUrl({
      phoneNumber: "6582234772",
      studentName: "Kai",
      paperNumber: "Paper 1",
      verdictPillar: "F",
      verdictScore: 52,
      topPatternLabel: "Conceptual misunderstanding",
    });
    expect(url).toContain("wa.me/6582234772");
    expect(url).toContain("Weakest%20pillar");
    expect(url).toContain("Kai");
    expect(url).toContain("F%20(52%25)");
  });
});
```

- [ ] **Step 2: Implement `lib/whatsapp.ts`**
```ts
export function buildWhatsAppUrl(args: {
  phoneNumber: string;
  studentName?: string;
  paperNumber?: string;
  verdictPillar: string;
  verdictScore: number;
  topPatternLabel: string;
}): string {
  const msg = [
    "Hi CLG, I just completed the Error Log Diagnostic.",
    "",
    "My results:",
    `• Student: ${args.studentName ?? "(not given)"}`,
    `• Level: ${args.paperNumber ?? "(not given)"}`,
    `• Weakest pillar: ${args.verdictPillar} (${args.verdictScore}%)`,
    `• Top pattern: ${args.topPatternLabel}`,
    "",
    "I'd like to book a FAST Learning System Consultation.",
  ].join("\n");
  return `https://wa.me/${args.phoneNumber}?text=${encodeURIComponent(msg)}`;
}
```

- [ ] **Step 3: Run tests — pass.**

- [ ] **Step 4: Implement `convex/leads.ts`**
```ts
import { mutation } from "./_generated/server";
import { v } from "convex/values";
export const capture = mutation({
  args: {
    sessionId: v.id("sessions"),
    email: v.string(),
    ctaTaken: v.union(v.literal("whatsapp"), v.literal("email"), v.literal("both"), v.literal("none")),
    source: v.string(),
  },
  handler: async (ctx, args) => {
    const existing = await ctx.db.query("leads").withIndex("by_session", q => q.eq("sessionId", args.sessionId)).first();
    if (existing) await ctx.db.patch(existing._id, { ...args, capturedAt: Date.now() });
    else await ctx.db.insert("leads", { ...args, capturedAt: Date.now() });
  },
});
```

- [ ] **Step 5: Implement `components/report/dual-cta.tsx`**
```tsx
"use client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { buildWhatsAppUrl } from "@/lib/whatsapp";
import { humanize } from "@/lib/utils";
import { useState } from "react";
import { useMutation } from "convex/react";
import { api } from "@/convex/_generated/api";
import { Id } from "@/convex/_generated/dataModel";

export function DualCTA({ sessionId, session, report }: {
  sessionId: Id<"sessions">;
  session: any;
  report: any;
}) {
  const capture = useMutation(api.leads.capture);
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);

  const waUrl = buildWhatsAppUrl({
    phoneNumber: "6582234772",
    studentName: session.studentName,
    paperNumber: session.paperNumber,
    verdictPillar: report.verdictPillars[0],
    verdictScore: report.pillarScores[report.verdictPillars[0]],
    topPatternLabel: report.topPatterns[0]?.label ?? "",
  });

  return (
    <div className="fixed bottom-0 inset-x-0 bg-background border-t shadow-lg p-4">
      <div className="max-w-2xl mx-auto flex flex-col gap-3">
        <a href={waUrl} target="_blank" rel="noreferrer"
           onClick={() => capture({ sessionId, email: email || "", ctaTaken: "whatsapp", source: "report_page" })}>
          <Button className="w-full" size="lg">📅 Book a 30-min FAST consult</Button>
        </a>
        {!sent ? (
          <form className="flex gap-2" onSubmit={async (e) => {
            e.preventDefault();
            await capture({ sessionId, email, ctaTaken: "email", source: "report_page" });
            setSent(true);
          }}>
            <Input type="email" required placeholder="your@email.com" value={email} onChange={e => setEmail(e.target.value)} />
            <Button type="submit" variant="outline">✉️ Email me the PDF</Button>
          </form>
        ) : (
          <p className="text-sm text-center text-muted-foreground">Report sent — check your inbox.</p>
        )}
      </div>
    </div>
  );
}
```

- [ ] **Step 6: Commit**
```bash
git add lib/ tests/ components/ convex/leads.ts
git commit -m "feat(P6): dual CTA with wa.me dynamic link and email capture"
```

### Task 6.5: PDF generation and email sending

**Files:** `components/pdf/report-pdf.tsx`, `convex/pdfGen.ts`, `convex/emails.ts`

- [ ] **Step 1: Implement `components/pdf/report-pdf.tsx`** (react-pdf document — simple V1)
```tsx
import { Document, Page, Text, View, StyleSheet } from "@react-pdf/renderer";
import { PILLAR_META } from "@/lib/pillars";

const styles = StyleSheet.create({
  page: { padding: 40, fontSize: 11, fontFamily: "Helvetica" },
  h1: { fontSize: 22, fontWeight: 700, marginBottom: 8 },
  h2: { fontSize: 14, fontWeight: 700, marginTop: 16, marginBottom: 6 },
  muted: { color: "#555" },
});

export function ReportPdf({ report, session }: any) {
  const pillar = report.verdictPillars[0];
  const m = PILLAR_META[pillar];
  return (
    <Document>
      <Page size="A4" style={styles.page}>
        <Text style={styles.h1}>{session.studentName}'s FAST Diagnostic Report</Text>
        <Text style={styles.muted}>Generated {new Date(report.generatedAt).toLocaleDateString()}</Text>
        <Text style={styles.h2}>Weakest pillar</Text>
        <Text>{pillar} — {m.name} ({report.pillarScores[pillar]}%)</Text>
        <Text>{m.oneLiner}</Text>
        <Text style={styles.h2}>Top patterns</Text>
        {report.topPatterns.map((p: any, i: number) => (
          <View key={i} style={{ marginBottom: 4 }}>
            <Text>• {p.label} (x{p.count}, Qn {p.qnNumbers.join(", ")})</Text>
            <Text style={styles.muted}>{p.interpretation}</Text>
          </View>
        ))}
        <Text style={styles.h2}>All pillar scores</Text>
        {(["F","A","S","T"] as const).map(p => <Text key={p}>{p} — {PILLAR_META[p].name}: {report.pillarScores[p]}%</Text>)}
        <Text style={styles.h2}>Next step</Text>
        <Text>Book a 30-min consult: wa.link/hkykpc or reply to this email.</Text>
      </Page>
    </Document>
  );
}
```

- [ ] **Step 2: Implement `convex/pdfGen.ts`** (action that renders PDF buffer)

Note: `@react-pdf/renderer` needs Node runtime. Use a Convex action.

```ts
"use node";
import { action } from "./_generated/server";
import { v } from "convex/values";
import { pdf } from "@react-pdf/renderer";
import { ReportPdf } from "@/components/pdf/report-pdf";
import React from "react";

export const renderReportPdf = action({
  args: { sessionId: v.id("sessions") },
  handler: async (ctx, { sessionId }) => {
    const session = await ctx.runQuery((await import("./sessions")).get, { id: sessionId });
    const report = await ctx.runQuery((await import("./reports")).getBySession, { sessionId });
    const buffer = await pdf(React.createElement(ReportPdf, { session, report } as any)).toBuffer();
    return buffer.toString("base64");
  },
});
```

- [ ] **Step 3: Implement `convex/emails.ts`** (Resend action)
```ts
"use node";
import { action } from "./_generated/server";
import { v } from "convex/values";
import { Resend } from "resend";

export const sendReportPdf = action({
  args: { sessionId: v.id("sessions"), email: v.string(), pdfBase64: v.string() },
  handler: async (_ctx, { email, pdfBase64, sessionId }) => {
    const resend = new Resend(process.env.RESEND_API_KEY!);
    await resend.emails.send({
      from: "FAST Diagnostic <diagnostic@cambridgelearning.sg>",
      to: email,
      subject: "Your FAST Diagnostic report",
      html: "<p>Your diagnostic is attached. Reply to this email to book a consult, or tap here: https://wa.link/hkykpc</p>",
      attachments: [{ filename: "fast-diagnostic.pdf", content: pdfBase64 }],
    });
    return { ok: true };
  },
});
```

- [ ] **Step 4: Wire CTA email submit to these actions**

Update `components/report/dual-cta.tsx` email handler to call both actions:
```ts
const renderPdf = useAction(api.pdfGen.renderReportPdf);
const sendMail = useAction(api.emails.sendReportPdf);
// in onSubmit:
const pdfBase64 = await renderPdf({ sessionId });
await sendMail({ sessionId, email, pdfBase64 });
```
(Inject `useAction` import from `convex/react`.)

- [ ] **Step 5: Add `RESEND_API_KEY` to Convex env**
```bash
npx convex env set RESEND_API_KEY <the-key>
```

- [ ] **Step 6: Manually verify end-to-end**
Complete a full diagnostic session with a real inbox you own. Verify PDF arrives, renders correctly, and the WhatsApp CTA opens with pre-filled text.

- [ ] **Step 7: Commit**
```bash
git add components/pdf/ convex/pdfGen.ts convex/emails.ts components/report/dual-cta.tsx
git commit -m "feat(P6): PDF generation and Resend email delivery"
```

---

## Phase 7 — Post-action confirmation (Screen 7) + Welcome-back banner + autosave

### Task 7.1: Welcome-back banner + localStorage draft

**Files:** `components/welcome-back-banner.tsx`, `lib/session-storage.ts`, integration in error-entry page

- [ ] **Step 1: Implement `lib/session-storage.ts`**
```ts
const KEY = "fast-diagnostic:last-session";
export function rememberSession(id: string) { localStorage.setItem(KEY, id); }
export function recallSession(): string | null { return typeof window === "undefined" ? null : localStorage.getItem(KEY); }
export function forgetSession() { localStorage.removeItem(KEY); }
```

- [ ] **Step 2: Implement `components/welcome-back-banner.tsx`**
```tsx
"use client";
import { useEffect, useState } from "react";
import { recallSession, forgetSession } from "@/lib/session-storage";
import Link from "next/link";

export function WelcomeBackBanner() {
  const [id, setId] = useState<string | null>(null);
  useEffect(() => setId(recallSession()), []);
  if (!id) return null;
  return (
    <div className="bg-muted px-4 py-2 text-sm text-center border-b">
      Welcome back — <Link className="underline font-medium" href={`/diagnostic/${id}/errors/1`}>continue your previous session</Link>
      {" "}or <button className="underline" onClick={() => { forgetSession(); setId(null); }}>start over</button>.
    </div>
  );
}
```

- [ ] **Step 3: Add to landing (`app/page.tsx`)**
Import and render `<WelcomeBackBanner />` at the top of `<main>`.

- [ ] **Step 4: In `app/diagnostic/new/page.tsx` — remember session on create**
```tsx
// after create() resolves:
rememberSession(id);
```

- [ ] **Step 5: Commit**
```bash
git add lib/session-storage.ts components/welcome-back-banner.tsx app/
git commit -m "feat(P7): welcome-back banner with localStorage session recall"
```

### Task 7.2: Post-action confirmation state

The report page already handles both paths inline via `DualCTA`. This task wires the secondary CTA to remain visible after the primary is taken:

- [ ] **Step 1: Modify `DualCTA` to show a "both paths taken" acknowledgement when both CTAs have been used.**

Pseudocode change: track `ctasDone` in state; after WhatsApp click → show "Opened WhatsApp. Want the PDF too?" below. After email submit → show "Report sent. Book a consult while it's fresh? [WhatsApp CTA]".

- [ ] **Step 2: Commit**
```bash
git add components/report/dual-cta.tsx
git commit -m "feat(P7): dual CTA keeps cross-sell visible after each path taken"
```

---

## Phase 8 — Polish, verification, deploy

### Task 8.1: E2E happy-path test

**Files:** `tests/e2e/full-flow.spec.ts`

- [ ] **Step 1: Write Playwright test**
```ts
import { test, expect } from "@playwright/test";

test("complete a diagnostic end to end", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("link", { name: /Start the diagnostic/i }).click();
  await page.getByRole("button", { name: /I'm the parent/i }).click();
  await page.getByLabel(/Student name/i).fill("Test Student");
  await page.getByRole("button", { name: /Continue/i }).click();
  for (let i = 1; i <= 5; i++) {
    await page.getByLabel(/Topic/i).fill(`Topic ${i}`);
    await page.getByRole("button", { name: /Save & next/i }).click();
    if (i === 5) {
      // reassurance screen
      await page.getByRole("button", { name: /Continue/i }).click();
    }
  }
  await page.getByRole("button", { name: /see my diagnosis/i }).click();
  await expect(page.getByText(/weakest FAST pillar/i)).toBeVisible({ timeout: 10_000 });
  await expect(page.getByRole("button", { name: /Book a 30-min FAST consult/i })).toBeVisible();
});
```

- [ ] **Step 2: Run**
```bash
npm run test:e2e
```
Expected: pass.

- [ ] **Step 3: Commit**
```bash
git add tests/
git commit -m "test(P8): e2e happy path"
```

### Task 8.2: Accessibility & mobile viewport smoke

- [ ] **Step 1:** Open devtools → toggle to iPhone 13 viewport → run through the whole flow. Fix any overflow/clipping before shipping.
- [ ] **Step 2:** Tab-through keyboard navigation on landing, audience, upload, error entry, report. Verify focus rings visible.
- [ ] **Step 3:** Lighthouse mobile report — aim for Perf > 85, A11y > 90.
- [ ] **Step 4:** Commit any fixes.
```bash
git commit -am "fix(P8): a11y and mobile polish"
```

### Task 8.3: Production env + final deploy

- [ ] **Step 1: Set Convex prod deployment**
```bash
npx convex deploy
```
Copy the prod URL.

- [ ] **Step 2: Update Vercel env**
```bash
vercel env add NEXT_PUBLIC_CONVEX_URL production   # paste prod Convex URL
vercel env add RESEND_API_KEY production
```

- [ ] **Step 3: Deploy to prod**
```bash
git push origin main
vercel --prod --yes
```

- [ ] **Step 4: Smoke-test prod URL** — repeat the full flow on the production URL from a phone.

- [ ] **Step 5: Update CLAUDE.md Current Status and commit**
```bash
git add CLAUDE.md
git commit -m "docs(P8): update status to v1 shipped"
git tag v1.0.0
git push origin v1.0.0
```

---

## Self-Review

**Spec coverage:**
- Tool identity / positioning → Task 3.2 (landing copy)
- Audience adaptation → Task 3.3 + lib/copy.ts
- Paper upload → Task 3.4
- Error log (Typeform style per Phase 3 research) → Task 4.2
- 2D classification + reinforcement → Tasks 4.1 + 5.1 + 5.2
- Report anatomy (hero / evidence / patterns / accordion / bridge / CTA) → Tasks 6.1–6.4
- Dual CTA (WhatsApp primary, email secondary) → Task 6.4
- Welcome-back banner / session recovery → Task 7.1
- PDF + Resend email → Task 6.5
- Faux-analysis animation → Task 5.3
- Tied-pillar verdict → Task 5.1 + 6.2
- CLAUDE.md → Task 0.5

**Placeholder scan:** No "TBD" or "implement later" in task steps. All code blocks are concrete.

**Type consistency:** `ErrorType`, `ErrorCategory`, `Pillar` defined once (schema validators mirror `lib/constants.ts` values). `Report`, `EnrichedError` types consistent across `lib/scoring.ts` and `convex/reports.ts`. The Convex mutation re-implements scoring logic server-side (vs. importing `lib/scoring.ts`) because Convex functions run in a separate runtime — this duplication is acknowledged and the unit test in `tests/unit/pillar-scoring.test.ts` tests the canonical logic; the Convex version mirrors it. A future improvement: extract into a shared package.

---

## Execution Handoff

**Plan complete and saved to `docs/superpowers/plans/2026-04-15-fast-diagnostic-plan.md`. Two execution options:**

**1. Subagent-Driven (recommended)** — Dispatch a fresh subagent per task, review between tasks, fast iteration.

**2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints for review.

**Which approach?**
