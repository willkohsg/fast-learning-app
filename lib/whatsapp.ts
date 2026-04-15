import { WHATSAPP_NUMBER, CONSULT_DURATION_MIN } from "./constants";
import type { Pillar } from "./pillars";

/**
 * Builds a wa.me deep link with a pre-filled message summarizing the
 * student's diagnostic. Message is URL-encoded. Falls back gracefully
 * when optional fields are missing.
 */
export function buildWhatsAppLink(params: {
  studentName?: string;
  level?: string; // sec1-4
  verdictPillars: Pillar[];
  topPatternLabel?: string;
  pillarPercent?: number;
}) {
  const levelLabel = params.level
    ? params.level.replace(/^sec/, "Sec ")
    : "(level not set)";

  const pillarStr =
    params.verdictPillars.length === 1
      ? params.verdictPillars[0]
      : params.verdictPillars.join(" & ");

  const pctStr =
    params.pillarPercent !== undefined
      ? ` (${params.pillarPercent}%)`
      : "";

  const lines = [
    `Hi CLG, I just completed the FAST Diagnostic Tool.`,
    ``,
    `My results:`,
    `• Student: ${params.studentName ?? "(not given)"}`,
    `• Level: ${levelLabel}`,
    `• Weakest pillar: ${pillarStr}${pctStr}`,
    params.topPatternLabel ? `• Top pattern: ${params.topPatternLabel}` : null,
    ``,
    `I'd like to book a ${CONSULT_DURATION_MIN}-min FAST consult.`,
  ].filter(Boolean);

  const text = encodeURIComponent(lines.join("\n"));
  return `https://wa.me/${WHATSAPP_NUMBER}?text=${text}`;
}
