export type Pillar = "F" | "A" | "S" | "T";

export const PILLAR_META: Record<
  Pillar,
  {
    letter: Pillar;
    name: string;
    subline: string;
    oneLiner: string;
    method: string;
    color: string;
    bgClass: string;
    textClass: string;
    borderClass: string;
  }
> = {
  F: {
    letter: "F",
    name: "Facts, Figures & Formulas",
    subline: "Instant, confident recall under pressure.",
    oneLiner:
      "Build the foundation. Increase recall speed. Remove hesitation.",
    method: "3R: Retrieve, Reinforce, Repeat.",
    color: "#2563eb",
    bgClass: "bg-blue-50",
    textClass: "text-blue-700",
    borderClass: "border-blue-200",
  },
  A: {
    letter: "A",
    name: "Analysis of Questions",
    subline: "Decode what the question actually asks before solving.",
    oneLiner:
      "Slow down at the start. Decode the question. Map known to unknown.",
    method: "Read–Restate–Plan.",
    color: "#7c3aed",
    bgClass: "bg-purple-50",
    textClass: "text-purple-700",
    borderClass: "border-purple-200",
  },
  S: {
    letter: "S",
    name: "Solving Patterns",
    subline: "Recognise the question type and apply the right method.",
    oneLiner:
      "Build a library of question patterns. Match new problems to them.",
    method: "Pattern matching, not improvisation.",
    color: "#059669",
    bgClass: "bg-emerald-50",
    textClass: "text-emerald-700",
    borderClass: "border-emerald-200",
  },
  T: {
    letter: "T",
    name: "Time Management",
    subline: "Get the marks you can, in the time you have.",
    oneLiner:
      "Pace per mark. Skip and return. Calm under the clock.",
    method: "Mark-budget per question; cut your losses.",
    color: "#ea580c",
    bgClass: "bg-orange-50",
    textClass: "text-orange-700",
    borderClass: "border-orange-200",
  },
};
