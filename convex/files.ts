import { mutation } from "./_generated/server";

/**
 * Generates a short-lived URL the client can POST a file to. Returned URL
 * uploads directly to Convex file storage and yields a storage ID.
 */
export const generateUploadUrl = mutation(async (ctx) => {
  return await ctx.storage.generateUploadUrl();
});
