import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

// ─────────────────────────────────────────────────────────────────
// Validators exported for reuse in mutations
// ─────────────────────────────────────────────────────────────────

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

// Conditional follow-up for the "careless" bucket. When set, overrides the
// default pillar mapping (careless → T) with the specific root-cause pillar.
export const carelessRootValidator = v.union(
  v.literal("misunderstood"), // → A
  v.literal("slip"), // → S
  v.literal("rushed"), // → T
);

export const pillarValidator = v.union(
  v.literal("F"),
  v.literal("A"),
  v.literal("S"),
  v.literal("T"),
);

export const audienceValidator = v.union(
  v.literal("parent"),
  v.literal("student"),
  v.literal("both"),
);

// Sec 1–4 only. PSLE/JC excluded from v1 (William, 2026-04-15).
export const levelValidator = v.union(
  v.literal("sec1"),
  v.literal("sec2"),
  v.literal("sec3"),
  v.literal("sec4"),
);

// ─────────────────────────────────────────────────────────────────
// Schema
// ─────────────────────────────────────────────────────────────────

export default defineSchema({
  sessions: defineTable({
    createdAt: v.number(),
    audience: v.optional(audienceValidator),
    level: v.optional(levelValidator),
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
    carelessRoot: v.optional(carelessRootValidator),
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
      F: v.number(),
      A: v.number(),
      S: v.number(),
      T: v.number(),
    }),
    topPatterns: v.array(
      v.object({
        label: v.string(),
        count: v.number(),
        qnNumbers: v.array(v.number()),
        interpretation: v.string(),
      }),
    ),
    verdictPillars: v.array(pillarValidator),
    generatedAt: v.number(),
  }).index("by_session", ["sessionId"]),

  leads: defineTable({
    sessionId: v.id("sessions"),
    email: v.optional(v.string()),
    capturedAt: v.number(),
    ctaTaken: v.union(
      v.literal("whatsapp"),
      v.literal("email"),
      v.literal("both"),
      v.literal("none"),
    ),
    source: v.string(),
  }).index("by_session", ["sessionId"]),
});
