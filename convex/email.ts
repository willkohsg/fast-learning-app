"use node";
import { action } from "./_generated/server";
import { internal } from "./_generated/api";
import { v } from "convex/values";
import { Resend } from "resend";
import { renderToBuffer } from "@react-pdf/renderer";
import React from "react";
import { ReportPDF } from "../lib/report-pdf";
import {
  EMAIL_FROM,
  EMAIL_REPLY_TO,
  TOOL_NAME,
  CONSULT_DURATION_MIN,
} from "../lib/constants";
import { PILLAR_META, type Pillar } from "../lib/pillars";
import { buildWhatsAppLink } from "../lib/whatsapp";

/**
 * Generates the PDF report and sends it via Resend.
 * Idempotent-ish: callable multiple times; will resend.
 */
export const sendReportEmail = action({
  args: {
    sessionId: v.id("sessions"),
    email: v.string(),
  },
  handler: async (ctx, { sessionId, email }): Promise<{ ok: boolean; id?: string }> => {
    const apiKey = process.env.RESEND_API_KEY;
    if (!apiKey) throw new Error("RESEND_API_KEY not configured");

    const bundle = await ctx.runQuery(internal.internal_queries.getReportBundle, {
      sessionId,
    });
    if (!bundle) throw new Error("Report not found for this session.");

    const { session, report, errors } = bundle;
    const verdictPillars = report.verdictPillars as Pillar[];
    const pillarScores = report.pillarScores as Record<Pillar, number>;
    const primary = verdictPillars[0];
    const meta = PILLAR_META[primary];

    // Topics from errors that contributed to the weakest pillar.
    const weakestTopics = Array.from(
      new Set(
        errors
          .filter((e) => e.primaryPillar === primary && e.topic?.trim())
          .map((e) => e.topic.trim()),
      ),
    );

    const whatsappLink = buildWhatsAppLink({
      studentName: session.studentName,
      level: session.level,
      verdictPillars,
      topPatternLabel: report.topPatterns[0]?.label,
      pillarPercent: pillarScores[primary],
    });

    const docElement = React.createElement(ReportPDF, {
      studentName: session.studentName,
      level: session.level,
      totalErrors: errors.length,
      pillarScores,
      verdictPillars,
      topPatterns: report.topPatterns,
      weakestTopics,
      whatsappLink,
    });
    // ReportPDF returns <Document>; cast to satisfy renderToBuffer's narrow type.
    const pdfBuffer = await renderToBuffer(
      docElement as Parameters<typeof renderToBuffer>[0],
    );

    const greeting = session.studentName ? `Hi ${session.studentName},` : "Hi,";
    const subject = `Your FAST Diagnostic — weakest pillar: ${meta.name}`;
    const html = `
      <div style="font-family: -apple-system, system-ui, Helvetica, Arial, sans-serif; max-width: 560px; margin: 0 auto; color: #1f2937; line-height: 1.5;">
        <p>${greeting}</p>
        <p>Your <strong>${TOOL_NAME}</strong> report is attached as a PDF.</p>
        <p>
          The headline: your weakest FAST pillar is
          <strong>${meta.name} (${meta.letter})</strong>${
            verdictPillars.length > 1
              ? ` — tied with ${verdictPillars.slice(1).join(", ")}`
              : ""
          },
          accounting for <strong>${pillarScores[primary]}%</strong> of your logged errors.
        </p>
        <p>
          Most students try to fix this with more practice. The ${meta.name} pillar
          actually responds to <strong>${meta.method.toLowerCase()}</strong> — that's the piece
          we'd walk through together in a ${CONSULT_DURATION_MIN}-min FAST consult.
        </p>
        <p>
          <a href="${whatsappLink}"
             style="display: inline-block; background: #16a34a; color: #fff; text-decoration: none; padding: 12px 20px; border-radius: 8px; font-weight: 600;">
            Book on WhatsApp
          </a>
        </p>
        <p style="font-size: 12px; color: #6b7280; margin-top: 32px; border-top: 1px solid #e5e7eb; padding-top: 12px;">
          This report is a starting point, not a diagnosis. Reply to this email if you have any questions —
          it goes straight to William at Cambridge Learning Group.
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
      attachments: [
        {
          filename: "fast-diagnostic-report.pdf",
          content: pdfBuffer,
        },
      ],
    });

    if (result.error) {
      throw new Error(`Resend error: ${result.error.message}`);
    }
    return { ok: true, id: result.data?.id };
  },
});
