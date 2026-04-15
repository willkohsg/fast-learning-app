/* eslint-disable */
/**
 * Generated `api` utility.
 *
 * THIS CODE IS AUTOMATICALLY GENERATED.
 *
 * To regenerate, run `npx convex dev`.
 * @module
 */

import type * as crons from "../crons.js";
import type * as email from "../email.js";
import type * as errors from "../errors.js";
import type * as files from "../files.js";
import type * as internal_queries from "../internal_queries.js";
import type * as leads from "../leads.js";
import type * as mappings from "../mappings.js";
import type * as purge from "../purge.js";
import type * as reports from "../reports.js";
import type * as seed from "../seed.js";
import type * as sessions from "../sessions.js";

import type {
  ApiFromModules,
  FilterApi,
  FunctionReference,
} from "convex/server";

declare const fullApi: ApiFromModules<{
  crons: typeof crons;
  email: typeof email;
  errors: typeof errors;
  files: typeof files;
  internal_queries: typeof internal_queries;
  leads: typeof leads;
  mappings: typeof mappings;
  purge: typeof purge;
  reports: typeof reports;
  seed: typeof seed;
  sessions: typeof sessions;
}>;

/**
 * A utility for referencing Convex functions in your app's public API.
 *
 * Usage:
 * ```js
 * const myFunctionReference = api.myModule.myFunction;
 * ```
 */
export declare const api: FilterApi<
  typeof fullApi,
  FunctionReference<any, "public">
>;

/**
 * A utility for referencing Convex functions in your app's internal API.
 *
 * Usage:
 * ```js
 * const myFunctionReference = internal.myModule.myFunction;
 * ```
 */
export declare const internal: FilterApi<
  typeof fullApi,
  FunctionReference<any, "internal">
>;

export declare const components: {};
