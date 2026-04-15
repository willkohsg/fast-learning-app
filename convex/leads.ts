import { mutation, query } from "./_generated/server";
import { v } from "convex/values";
import { api } from "./_generated/api";

/**
 * Captures a lead row when the user requests the PDF report by email.
 * Phase 7 will wire an action that triggers Resend; for now this records
 * the email + intent so we never lose a lead even if email send fails later.
 */
export const requestReportEmail = mutation({
  args: {
    sessionId: v.id("sessions"),
    email: v.string(),
  },
  handler: async (ctx, { sessionId, email }) => {
    const trimmed = email.trim().toLowerCase();
    if (!trimmed.includes("@")) {
      throw new Error("Invalid email address.");
    }
    const existing = await ctx.db
      .query("leads")
      .withIndex("by_session", (q) => q.eq("sessionId", sessionId))
      .first();
    let leadId;
    if (existing) {
      await ctx.db.patch(existing._id, {
        email: trimmed,
        ctaTaken: existing.ctaTaken === "whatsapp" ? "both" : "email",
      });
      leadId = existing._id;
    } else {
      leadId = await ctx.db.insert("leads", {
        sessionId,
        email: trimmed,
        capturedAt: Date.now(),
        ctaTaken: "email",
        source: "report",
      });
    }
    // Fire-and-forget: schedule the PDF + email send in the node runtime.
    await ctx.scheduler.runAfter(0, api.email.sendReportEmail, {
      sessionId,
      email: trimmed,
    });
    return { ok: true, leadId };
  },
});

export const recordWhatsAppClick = mutation({
  args: { sessionId: v.id("sessions") },
  handler: async (ctx, { sessionId }) => {
    const existing = await ctx.db
      .query("leads")
      .withIndex("by_session", (q) => q.eq("sessionId", sessionId))
      .first();
    if (existing) {
      await ctx.db.patch(existing._id, {
        ctaTaken: existing.ctaTaken === "email" ? "both" : "whatsapp",
      });
      return { ok: true, leadId: existing._id };
    }
    const leadId = await ctx.db.insert("leads", {
      sessionId,
      capturedAt: Date.now(),
      ctaTaken: "whatsapp",
      source: "report",
    });
    return { ok: true, leadId };
  },
});

export const getBySession = query({
  args: { sessionId: v.id("sessions") },
  handler: async (ctx, { sessionId }) =>
    await ctx.db
      .query("leads")
      .withIndex("by_session", (q) => q.eq("sessionId", sessionId))
      .first(),
});
