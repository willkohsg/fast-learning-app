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
// Decomposes the lossy "careless" bucket and routes to A / S / T.
export const CARELESS_ROOTS = [
  { value: "misunderstood", label: "I misunderstood the question", pillarHint: "A" },
  { value: "slip", label: "I knew what to do but made a slip", pillarHint: "S" },
  { value: "rushed", label: "I rushed because of time", pillarHint: "T" },
] as const;

export const AUDIENCES = [
  { value: "parent", label: "I'm the parent", emoji: "👨‍👩‍👧" },
  { value: "student", label: "I'm the student", emoji: "🎓" },
  { value: "both", label: "Parent + student, together", emoji: "🤝", recommended: true },
] as const;

export const LEVELS = [
  { value: "sec1", label: "Sec 1" },
  { value: "sec2", label: "Sec 2" },
  { value: "sec3", label: "Sec 3" },
  { value: "sec4", label: "Sec 4" },
] as const;

export const PAPER_NUMBERS = ["Paper 1", "Paper 2", "Mock", "Revision", "Other"] as const;

export const MIN_ERRORS_FOR_REPORT = 5;
export const NUDGE_AT = [5, 10, 15] as const;
export const GENTLE_CAP = 20;

// Branding
export const TOOL_NAME = "FAST Diagnostic Tool";
export const BRAND = "Cambridge Learning Group";
export const WHATSAPP_NUMBER = "6582234772"; // +65 8223 4772
export const CONSULT_DURATION_MIN = 30;
