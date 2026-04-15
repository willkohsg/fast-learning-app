"use node";
import { action } from "./_generated/server";
import { internal } from "./_generated/api";
import { v } from "convex/values";
import { Resend } from "resend";
import {
  EMAIL_FROM,
  EMAIL_REPLY_TO,
  TOOL_NAME,
  CONSULT_DURATION_MIN,
} from "../lib/constants";
import { PILLAR_META, type Pillar } from "../lib/pillars";
import { buildWhatsAppLink } from "../lib/whatsapp";

const ORDER: Pillar[] = ["F", "A", "S", "T"];

// Per-pillar inline color palette for email (matches on-screen hero card).
// Email clients don't support Tailwind, so we hand-pick light bg / border / dark text.
const PILLAR_EMAIL_PALETTE: Record<
  Pillar,
  { bg: string; border: string; text: string }
> = {
  F: { bg: "#eff6ff", border: "#bfdbfe", text: "#1d4ed8" },
  A: { bg: "#faf5ff", border: "#e9d5ff", text: "#6d28d9" },
  S: { bg: "#ecfdf5", border: "#a7f3d0", text: "#047857" },
  T: { bg: "#fff7ed", border: "#fed7aa", text: "#c2410c" },
};

/**
 * Sends the diagnostic report by email.
 *
 * v1: HTML-only (no PDF attachment). The report itself stays interactive
 * on the web; the email is a high-quality recap + WhatsApp + report link.
 * (PDF generation via @react-pdf/renderer is incompatible with React 19
 * in the Node action runtime — revisit later if attachment is needed.)
 */
export const sendReportEmail = action({
  args: {
    sessionId: v.id("sessions"),
    email: v.string(),
  },
  handler: async (
    ctx,
    { sessionId, email },
  ): Promise<{ ok: boolean; id?: string }> => {
    const apiKey = process.env.RESEND_API_KEY;
    if (!apiKey) throw new Error("RESEND_API_KEY not configured");

    const bundle = await ctx.runQuery(
      internal.internal_queries.getReportBundle,
      { sessionId },
    );
    if (!bundle) throw new Error("Report not found for this session.");

    const { session, report, errors } = bundle;
    const verdictPillars = report.verdictPillars as Pillar[];
    const pillarScores = report.pillarScores as Record<Pillar, number>;
    const primary = verdictPillars[0];
    const meta = PILLAR_META[primary];

    const weakestTopics = Array.from(
      new Set(
        errors
          .filter((e) => e.primaryPillar === primary && e.topic?.trim())
          .map((e) => e.topic.trim()),
      ),
    ).slice(0, 3);

    const whatsappLink = buildWhatsAppLink({
      studentName: session.studentName,
      level: session.level,
      verdictPillars,
      topPatternLabel: report.topPatterns[0]?.label,
      pillarPercent: pillarScores[primary],
    });

    const appUrl =
      process.env.NEXT_PUBLIC_APP_URL ?? "https://fast-diagnostic.vercel.app";
    const reportUrl = `${appUrl}/diagnostic/${sessionId}/report`;

    const greeting = session.studentName
      ? `Hi ${session.studentName},`
      : "Hi,";
    const subject = `Your FAST Diagnostic — weakest pillar: ${meta.name}`;

    const breakdownRows = ORDER.map(
      (p) =>
        `<tr>
          <td style="padding: 6px 12px 6px 0; border-bottom: 1px solid #f3f4f6; font-weight: 600;">${p} — ${PILLAR_META[p].name}</td>
          <td style="padding: 6px 0; border-bottom: 1px solid #f3f4f6; text-align: right; font-weight: 600;">${pillarScores[p]}%</td>
        </tr>`,
    ).join("");

    const patternList =
      report.topPatterns.length > 0
        ? `<ul style="padding-left: 20px; margin: 8px 0 0;">
            ${report.topPatterns
              .map(
                (p) =>
                  `<li style="margin-bottom: 6px;"><strong>${escapeHtml(p.label)}</strong> (${p.count}× — Q${p.qnNumbers.join(", Q")})</li>`,
              )
              .join("")}
          </ul>`
        : "";

    const topicsLine =
      weakestTopics.length > 0
        ? `<p>Clustering was strongest in <strong>${escapeHtml(weakestTopics.join(", "))}</strong>.</p>`
        : "";

    const palette = PILLAR_EMAIL_PALETTE[primary];
    const tied = verdictPillars.length > 1;
    const heroBadge = tied ? verdictPillars.join("/") : primary;
    const greetingName = session.studentName ? `${session.studentName}, ` : "";
    const heroHeadline = tied
      ? `${escapeHtml(greetingName)}your weakest pillars are <span style="color: ${palette.text};">${verdictPillars.join(" &amp; ")}</span> &mdash; tied at ~${pillarScores[primary]}% each.`
      : `${escapeHtml(greetingName)}your weakest pillar is <span style="color: ${palette.text};">${escapeHtml(meta.name)}</span> &mdash; ${pillarScores[primary]}% of your errors.`;

    const html = `
      <div style="font-family: -apple-system, system-ui, Helvetica, Arial, sans-serif; max-width: 560px; margin: 0 auto; color: #1f2937; line-height: 1.55; font-size: 15px; padding: 12px;">

        <!-- Hero verdict card -->
        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background: ${palette.bg}; border: 2px solid ${palette.border}; border-radius: 16px; margin-bottom: 24px;">
          <tr>
            <td style="padding: 24px;">
              <table role="presentation" cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td style="vertical-align: top; padding-right: 16px;">
                    <div style="width: 56px; height: 56px; background: #ffffff; border-radius: 14px; text-align: center; line-height: 56px; font-size: 28px; font-weight: 900; color: ${palette.text}; box-shadow: 0 1px 2px rgba(0,0,0,0.04);">
                      ${heroBadge}
                    </div>
                  </td>
                  <td style="vertical-align: top;">
                    <p style="margin: 0 0 6px; font-size: 11px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: ${palette.text};">Your weakest FAST pillar</p>
                    <h1 style="margin: 0; font-size: 22px; line-height: 1.25; color: #111827; font-weight: 700;">${heroHeadline}</h1>
                  </td>
                </tr>
              </table>
              <p style="margin: 16px 0 0; padding-top: 14px; border-top: 1px solid rgba(255,255,255,0.7); font-size: 14px; color: #374151;">
                ${escapeHtml(meta.subline)}
              </p>
            </td>
          </tr>
        </table>

        <p style="margin: 0 0 12px;">${greeting}</p>
        <p style="margin: 0 0 8px;">Of your <strong>${errors.length}</strong> logged errors, <strong>${pillarScores[primary]}%</strong> traced back to the <strong>${escapeHtml(meta.name)}</strong> pillar.</p>
        ${topicsLine}

        <h2 style="font-size: 16px; margin: 24px 0 8px;">Top recurring patterns</h2>
        ${patternList}

        <h2 style="font-size: 16px; margin: 24px 0 8px;">Your full FAST breakdown</h2>
        <table style="width: 100%; border-collapse: collapse; font-size: 14px;">${breakdownRows}</table>

        <h2 style="font-size: 16px; margin: 24px 0 8px;">What this means</h2>
        <p>Most students try to fix this with more practice. The ${meta.name} pillar actually responds to <strong>${meta.method.toLowerCase()}</strong> — that's what we'd walk through together in a ${CONSULT_DURATION_MIN}-min FAST consult.</p>

        <div style="margin: 28px 0;">
          <a href="${whatsappLink}" style="display: inline-block; background: #16a34a; color: #fff; text-decoration: none; padding: 12px 22px; border-radius: 8px; font-weight: 600; margin-right: 8px;">Book on WhatsApp</a>
          <a href="${reportUrl}" style="display: inline-block; background: #fff; color: #1f2937; text-decoration: none; padding: 12px 22px; border-radius: 8px; font-weight: 600; border: 1px solid #d1d5db;">View full report online</a>
        </div>

        <p style="font-size: 12px; color: #6b7280; margin-top: 32px; border-top: 1px solid #e5e7eb; padding-top: 12px;">
          This report is a starting point, not a diagnosis. Reply to this email if you have any questions — it goes straight to William at Cambridge Learning Group.
        </p>
      </div>
    `;

    const resend = new Resend(apiKey);
    const result = await resend.emails.send({
      from: EMAIL_FROM,
      to: email,
      replyTo: EMAIL_REPLY_TO,
      subject,
      html,
    });

    if (result.error) {
      throw new Error(`Resend error: ${result.error.message}`);
    }
    return { ok: true, id: result.data?.id };
  },
});

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}
