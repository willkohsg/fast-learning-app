import { mutation, query } from "./_generated/server";
import { v } from "convex/values";
import { audienceValidator, levelValidator } from "./schema";

export const create = mutation({
  args: {},
  handler: async (ctx) => {
    const id = await ctx.db.insert("sessions", {
      createdAt: Date.now(),
      status: "in_progress",
    });
    return id;
  },
});

export const get = query({
  args: { id: v.id("sessions") },
  handler: async (ctx, { id }) => await ctx.db.get(id),
});

export const setAudience = mutation({
  args: { id: v.id("sessions"), audience: audienceValidator },
  handler: async (ctx, { id, audience }) => {
    await ctx.db.patch(id, { audience });
  },
});

export const setPaperMeta = mutation({
  args: {
    id: v.id("sessions"),
    level: v.optional(levelValidator),
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
    await ctx.db.patch(id, {
      status: "submitted",
      submittedAt: Date.now(),
    });
  },
});
