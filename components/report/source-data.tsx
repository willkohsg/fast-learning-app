"use client";
import { useQuery } from "convex/react";
import { api } from "@/convex/_generated/api";
import type { Id } from "@/convex/_generated/dataModel";
import {
  ERROR_TYPES,
  ERROR_CATEGORIES,
  CARELESS_ROOTS,
} from "@/lib/constants";

type ErrorRow = {
  _id: Id<"errors">;
  qnNumber: number;
  topic: string;
  errorType: string;
  errorCategory: string;
  carelessRoot?: string;
  rootCause?: string;
  details?: string;
  primaryPillar?: string;
  reinforced?: boolean;
};

function labelFor<T extends { value: string; label: string }>(
  list: readonly T[],
  value: string | undefined,
): string {
  if (!value) return "—";
  return list.find((x) => x.value === value)?.label ?? value;
}

function PaperFile({ url }: { url: string }) {
  // Convex storage URLs don't carry an extension; use HEAD-less heuristics:
  // try image first, fall back to <object> (handles PDFs in-browser).
  // We render both and let CSS hide whichever fails via onError.
  return (
    <div className="border rounded-md overflow-hidden bg-muted/30">
      <object
        data={url}
        type="application/pdf"
        className="w-full h-[600px] hidden sm:block"
      >
        {/* Fallback for non-PDFs (images) and small screens */}
        <img
          src={url}
          alt="Uploaded paper page"
          className="w-full h-auto block"
        />
      </object>
      {/* Mobile fallback: just show as image (most uploads are phone photos) */}
      <img
        src={url}
        alt="Uploaded paper page"
        className="w-full h-auto block sm:hidden"
      />
      <div className="px-3 py-2 text-xs text-muted-foreground flex justify-between items-center">
        <span>Uploaded paper</span>
        <a
          href={url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-primary underline"
        >
          Open in new tab ↗
        </a>
      </div>
    </div>
  );
}

export function SourceData({
  sessionId,
  errors,
}: {
  sessionId: Id<"sessions">;
  errors: ErrorRow[];
}) {
  const papers = useQuery(api.files.getSessionPaperUrls, { sessionId });

  const sortedErrors = [...errors].sort((a, b) => a.qnNumber - b.qnNumber);

  return (
    <section className="space-y-6 pt-2">
      <div>
        <h2 className="text-xl font-semibold tracking-tight">
          Source data for this report
        </h2>
        <p className="text-sm text-muted-foreground mt-1">
          The uploaded paper and every error you logged — included here so you
          can review exactly what the report was built from.
        </p>
      </div>

      {/* Uploaded paper(s) */}
      <div className="space-y-3">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground">
          Uploaded paper
        </h3>
        {papers === undefined ? (
          <p className="text-sm text-muted-foreground">Loading paper…</p>
        ) : papers.length === 0 ? (
          <p className="text-sm text-muted-foreground italic">
            No paper was uploaded for this session.
          </p>
        ) : (
          <div className="space-y-3">
            {papers.map((p) => (
              <PaperFile key={p.storageId} url={p.url} />
            ))}
          </div>
        )}
      </div>

      {/* Error log entries */}
      <div className="space-y-3">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-muted-foreground">
          Error log entries ({sortedErrors.length})
        </h3>
        {sortedErrors.length === 0 ? (
          <p className="text-sm text-muted-foreground italic">
            No errors were logged.
          </p>
        ) : (
          <ol className="space-y-3">
            {sortedErrors.map((e) => (
              <li
                key={e._id}
                className="border rounded-md p-4 bg-card space-y-2"
              >
                <div className="flex items-baseline justify-between gap-2 flex-wrap">
                  <div className="font-semibold">
                    Question {e.qnNumber}
                    {e.topic ? (
                      <span className="text-muted-foreground font-normal">
                        {" "}
                        · {e.topic}
                      </span>
                    ) : null}
                  </div>
                  {e.primaryPillar && (
                    <span className="text-xs px-2 py-0.5 rounded-full bg-primary/10 text-primary font-medium">
                      Pillar: {e.primaryPillar}
                    </span>
                  )}
                </div>

                <dl className="grid grid-cols-1 sm:grid-cols-[max-content_1fr] gap-x-4 gap-y-1.5 text-sm">
                  <dt className="text-muted-foreground">Error type</dt>
                  <dd>{labelFor(ERROR_TYPES, e.errorType)}</dd>

                  <dt className="text-muted-foreground">Error category</dt>
                  <dd>{labelFor(ERROR_CATEGORIES, e.errorCategory)}</dd>

                  {e.carelessRoot && (
                    <>
                      <dt className="text-muted-foreground">Careless root</dt>
                      <dd>{labelFor(CARELESS_ROOTS, e.carelessRoot)}</dd>
                    </>
                  )}

                  {e.rootCause && (
                    <>
                      <dt className="text-muted-foreground">Root cause</dt>
                      <dd className="whitespace-pre-wrap">{e.rootCause}</dd>
                    </>
                  )}

                  {e.details && (
                    <>
                      <dt className="text-muted-foreground">Details</dt>
                      <dd className="whitespace-pre-wrap">{e.details}</dd>
                    </>
                  )}

                  {e.reinforced !== undefined && (
                    <>
                      <dt className="text-muted-foreground">Reinforced</dt>
                      <dd>{e.reinforced ? "Yes" : "No"}</dd>
                    </>
                  )}
                </dl>
              </li>
            ))}
          </ol>
        )}
      </div>
    </section>
  );
}
