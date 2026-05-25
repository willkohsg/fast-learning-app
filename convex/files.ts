import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

/**
 * Generates a short-lived URL the client can POST a file to. Returned URL
 * uploads directly to Convex file storage and yields a storage ID.
 */
export const generateUploadUrl = mutation(async (ctx) => {
  return await ctx.storage.generateUploadUrl();
});

/**
 * Returns signed URLs for the uploaded paper files attached to a session.
 * Each entry preserves the original storage id so the client can key on it.
 */
export const getSessionPaperUrls = query({
  args: { sessionId: v.id("sessions") },
  handler: async (ctx, { sessionId }) => {
    const session = await ctx.db.get(sessionId);
    if (!session?.uploadedPaperFileIds?.length) return [];
    const urls = await Promise.all(
      session.uploadedPaperFileIds.map(async (id) => ({
        storageId: id,
        url: await ctx.storage.getUrl(id),
      })),
    );
    return urls.filter((u): u is { storageId: typeof u.storageId; url: string } => u.url !== null);
  },
});
