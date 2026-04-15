import { mutation, query } from "./_generated/server";
import { v } from "convex/values";
import {
  errorTypeValidator,
  errorCategoryValidator,
  carelessRootValidator,
} from "./schema";

export const listBySession = query({
  args: { sessionId: v.id("sessions") },
  handler: async (ctx, { sessionId }) =>
    await ctx.db
      .query("errors")
      .withIndex("by_session", (q) => q.eq("sessionId", sessionId))
      .collect(),
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
    const existing = await ctx.db
      .query("errors")
      .withIndex("by_session", (q) => q.eq("sessionId", args.sessionId))
      .filter((q) => q.eq(q.field("qnNumber"), args.qnNumber))
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
  handler: async (ctx, { id }) => {
    await ctx.db.delete(id);
  },
});
