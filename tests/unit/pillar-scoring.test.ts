import { describe, it, expect } from "vitest";
import { computeReport } from "@/lib/scoring";

describe("computeReport", () => {
  const typePillar = {
    careless: "T",
    conceptual_misunderstanding: "F",
    misread_question: "A",
    applied_wrong_formula: "S",
    did_not_complete_working: "S",
    time_management_issue: "T",
  } as const;
  const catPillar = {
    knowledge_gap: "F",
    misapplied_rule: "A",
    confusion_between_concepts: "S",
    poor_exam_strategy: "T",
    anxiety_panic: "T",
    lack_of_practice: "S",
  } as const;
  const carelessRootPillar = {
    misunderstood: "A",
    slip: "S",
    rushed: "T",
  } as const;

  it("scores single careless error with no carelessRoot to default T", () => {
    const r = computeReport(
      [
        {
          qnNumber: 1,
          errorType: "careless",
          errorCategory: "anxiety_panic",
          topic: "x",
        },
      ],
      typePillar,
      catPillar,
      carelessRootPillar,
    );
    expect(r.pillarScores).toEqual({ F: 0, A: 0, S: 0, T: 100 });
    expect(r.verdictPillars).toEqual(["T"]);
  });

  it("finds tied pillars within 5pp", () => {
    const errors = [
      {
        qnNumber: 1,
        errorType: "careless" as const,
        errorCategory: "anxiety_panic" as const,
        topic: "x",
      },
      {
        qnNumber: 2,
        errorType: "conceptual_misunderstanding" as const,
        errorCategory: "knowledge_gap" as const,
        topic: "x",
      },
    ];
    const r = computeReport(errors, typePillar, catPillar, carelessRootPillar);
    expect(r.verdictPillars.sort()).toEqual(["F", "T"]);
  });

  it("marks error as reinforced when category matches primary", () => {
    const r = computeReport(
      [
        {
          qnNumber: 1,
          errorType: "careless",
          errorCategory: "anxiety_panic",
          topic: "x",
        },
      ],
      typePillar,
      catPillar,
      carelessRootPillar,
    );
    expect(r.enrichedErrors[0].reinforced).toBe(true);
  });

  it("extracts top 3 patterns by (type, category) count", () => {
    const errors = Array.from({ length: 4 }).map((_, i) => ({
      qnNumber: i + 1,
      errorType: "misread_question" as const,
      errorCategory: "misapplied_rule" as const,
      topic: "",
    }));
    const r = computeReport(errors, typePillar, catPillar, carelessRootPillar);
    expect(r.topPatterns[0].count).toBe(4);
    expect(r.topPatterns[0].qnNumbers).toEqual([1, 2, 3, 4]);
  });

  it("routes Careless to A/S/T based on carelessRoot follow-up", () => {
    const errors = [
      {
        qnNumber: 1,
        errorType: "careless" as const,
        errorCategory: "anxiety_panic" as const,
        carelessRoot: "misunderstood" as const,
        topic: "",
      },
      {
        qnNumber: 2,
        errorType: "careless" as const,
        errorCategory: "anxiety_panic" as const,
        carelessRoot: "slip" as const,
        topic: "",
      },
      {
        qnNumber: 3,
        errorType: "careless" as const,
        errorCategory: "anxiety_panic" as const,
        carelessRoot: "rushed" as const,
        topic: "",
      },
    ];
    const r = computeReport(errors, typePillar, catPillar, carelessRootPillar);
    expect(r.enrichedErrors.map((e) => e.primaryPillar)).toEqual([
      "A",
      "S",
      "T",
    ]);
    // 33% each → all three tied in verdict (within 5pp)
    expect(r.verdictPillars.sort()).toEqual(["A", "S", "T"]);
  });

  it("falls back to errorTypePillar['careless'] when carelessRoot missing", () => {
    const r = computeReport(
      [
        {
          qnNumber: 1,
          errorType: "careless",
          errorCategory: "anxiety_panic",
          topic: "",
        },
      ],
      typePillar,
      catPillar,
      carelessRootPillar,
    );
    expect(r.enrichedErrors[0].primaryPillar).toBe("T");
  });
});
