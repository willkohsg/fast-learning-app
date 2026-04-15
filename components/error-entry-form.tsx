"use client";
import { useState } from "react";
import {
  ERROR_TYPES,
  ERROR_CATEGORIES,
  CARELESS_ROOTS,
} from "@/lib/constants";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export type ErrorEntryData = {
  qnNumber: number;
  topic: string;
  errorType: (typeof ERROR_TYPES)[number]["value"];
  errorCategory: (typeof ERROR_CATEGORIES)[number]["value"];
  carelessRoot?: (typeof CARELESS_ROOTS)[number]["value"];
  rootCause: string;
  details: string;
};

export function ErrorEntryForm({
  initial,
  onSave,
  onCancel,
  submitLabel,
}: {
  initial: Partial<ErrorEntryData>;
  onSave: (d: ErrorEntryData) => void | Promise<void>;
  onCancel?: () => void;
  submitLabel: string;
}) {
  const [data, setData] = useState<ErrorEntryData>({
    qnNumber: initial.qnNumber ?? 1,
    topic: initial.topic ?? "",
    errorType: initial.errorType ?? ERROR_TYPES[0].value,
    errorCategory: initial.errorCategory ?? ERROR_CATEGORIES[0].value,
    carelessRoot: initial.carelessRoot,
    rootCause: initial.rootCause ?? "",
    details: initial.details ?? "",
  });
  const [saving, setSaving] = useState(false);

  const isCareless = data.errorType === "careless";
  // Gate: if careless, require follow-up before Save enables.
  const canSave =
    data.topic.trim().length > 0 && (!isCareless || !!data.carelessRoot);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!canSave) return;
    setSaving(true);
    try {
      await onSave(data);
    } finally {
      setSaving(false);
    }
  }

  return (
    <form className="space-y-4" onSubmit={handleSubmit}>
      <div>
        <Label htmlFor="qnNumber">Question number</Label>
        <Input
          id="qnNumber"
          type="number"
          inputMode="numeric"
          min={1}
          value={data.qnNumber}
          onChange={(e) =>
            setData((d) => ({ ...d, qnNumber: Number(e.target.value) || 1 }))
          }
          className="mt-1"
        />
      </div>

      <div>
        <Label htmlFor="topic">Topic / Sub-topic</Label>
        <Input
          id="topic"
          value={data.topic}
          onChange={(e) => setData((d) => ({ ...d, topic: e.target.value }))}
          placeholder="e.g. Quadratic equations, Trigonometry, Vectors"
          className="mt-1"
        />
      </div>

      <div>
        <Label>Error Type (what went wrong on the surface)</Label>
        <Select
          value={data.errorType}
          onValueChange={(v) =>
            setData((d) => ({
              ...d,
              errorType: v as ErrorEntryData["errorType"],
              // Reset carelessRoot when switching away from careless
              carelessRoot: v === "careless" ? d.carelessRoot : undefined,
            }))
          }
        >
          <SelectTrigger className="mt-1">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {ERROR_TYPES.map((t) => (
              <SelectItem key={t.value} value={t.value}>
                {t.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Conditional follow-up: "Careless" decomposes into 3 root causes
          that route to different pillars (A / S / T). Required before save. */}
      {isCareless && (
        <div className="rounded-md border-2 border-amber-300 bg-amber-50 p-4 space-y-3">
          <div>
            <Label className="font-semibold text-amber-900">
              What caused this careless mistake?
            </Label>
            <p className="text-sm text-amber-800 mt-1">
              "Careless" covers 3 very different things. Pick the one closest
              to what happened — it changes the diagnosis.
            </p>
          </div>
          <div className="space-y-2">
            {CARELESS_ROOTS.map((r) => (
              <label
                key={r.value}
                className={`flex items-start gap-3 cursor-pointer p-2 rounded-md transition ${
                  data.carelessRoot === r.value
                    ? "bg-amber-100 border border-amber-400"
                    : "hover:bg-amber-100/50"
                }`}
              >
                <input
                  type="radio"
                  name="carelessRoot"
                  value={r.value}
                  checked={data.carelessRoot === r.value}
                  onChange={() =>
                    setData((d) => ({ ...d, carelessRoot: r.value }))
                  }
                  className="mt-1"
                />
                <span className="text-sm text-amber-900">{r.label}</span>
              </label>
            ))}
          </div>
        </div>
      )}

      <div>
        <Label>Error Category (the deeper cause)</Label>
        <Select
          value={data.errorCategory}
          onValueChange={(v) =>
            setData((d) => ({
              ...d,
              errorCategory: v as ErrorEntryData["errorCategory"],
            }))
          }
        >
          <SelectTrigger className="mt-1">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {ERROR_CATEGORIES.map((c) => (
              <SelectItem key={c.value} value={c.value}>
                {c.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div>
        <Label htmlFor="rootCause">Root cause (optional)</Label>
        <Textarea
          id="rootCause"
          rows={2}
          value={data.rootCause}
          onChange={(e) =>
            setData((d) => ({ ...d, rootCause: e.target.value }))
          }
          placeholder="Your own words — what actually went wrong?"
          className="mt-1"
        />
      </div>

      <div>
        <Label htmlFor="details">Details (optional)</Label>
        <Textarea
          id="details"
          rows={2}
          value={data.details}
          onChange={(e) => setData((d) => ({ ...d, details: e.target.value }))}
          placeholder="Any extra context — the actual working, etc."
          className="mt-1"
        />
      </div>

      <div className="flex gap-2 pt-2">
        {onCancel && (
          <Button type="button" variant="ghost" onClick={onCancel}>
            Back
          </Button>
        )}
        <Button type="submit" disabled={!canSave || saving} className="flex-1">
          {saving ? "Saving…" : submitLabel}
        </Button>
      </div>
    </form>
  );
}
