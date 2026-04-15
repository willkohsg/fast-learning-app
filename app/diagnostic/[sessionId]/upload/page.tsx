"use client";
import { useParams, useRouter } from "next/navigation";
import { useMutation, useQuery } from "convex/react";
import { api } from "@/convex/_generated/api";
import type { Id } from "@/convex/_generated/dataModel";
import { useState } from "react";
import { LEVELS, PAPER_NUMBERS } from "@/lib/constants";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export default function UploadPage() {
  const { sessionId } = useParams<{ sessionId: string }>();
  const router = useRouter();
  const session = useQuery(api.sessions.get, {
    id: sessionId as Id<"sessions">,
  });
  const setPaperMeta = useMutation(api.sessions.setPaperMeta);
  const generateUploadUrl = useMutation(api.files.generateUploadUrl);

  const [studentName, setStudentName] = useState("");
  const [level, setLevel] = useState<(typeof LEVELS)[number]["value"] | "">(
    "",
  );
  const [school, setSchool] = useState("");
  const [paperNumber, setPaperNumber] = useState("");
  const [paperDate, setPaperDate] = useState("");
  const [uploadedIds, setUploadedIds] = useState<Id<"_storage">[]>([]);
  const [uploading, setUploading] = useState(false);
  const [saving, setSaving] = useState(false);

  async function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const files = Array.from(e.target.files ?? []);
    if (files.length === 0) return;
    setUploading(true);
    const ids: Id<"_storage">[] = [];
    for (const file of files) {
      const url = await generateUploadUrl();
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": file.type },
        body: file,
      });
      const { storageId } = (await res.json()) as {
        storageId: Id<"_storage">;
      };
      ids.push(storageId);
    }
    setUploadedIds((prev) => [...prev, ...ids]);
    setUploading(false);
  }

  async function save(opts: { skip?: boolean } = {}) {
    setSaving(true);
    await setPaperMeta({
      id: sessionId as Id<"sessions">,
      level: (level || undefined) as any,
      studentName: studentName || undefined,
      paperDate: paperDate || undefined,
      school: school || undefined,
      paperNumber: paperNumber || undefined,
      uploadedPaperFileIds: opts.skip ? [] : uploadedIds,
    });
    router.push(`/diagnostic/${sessionId}/errors/1`);
  }

  const canContinue = !!level && !!studentName.trim() && !uploading;

  if (session === undefined) {
    return (
      <main className="min-h-screen flex items-center justify-center px-6">
        <p className="text-muted-foreground">Loading…</p>
      </main>
    );
  }

  return (
    <main className="min-h-screen px-6 py-10 max-w-2xl mx-auto space-y-6">
      <div>
        <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Step 2 of 4
        </p>
        <h1 className="text-3xl font-bold mt-1">Tell us about the paper</h1>
        <p className="text-muted-foreground mt-2">
          Upload a photo/PDF of the marked paper for your own reference (we
          don't read it automatically). Then fill in a few details.
        </p>
      </div>

      <div className="space-y-4">
        <div>
          <Label htmlFor="studentName">Student's first name *</Label>
          <Input
            id="studentName"
            value={studentName}
            onChange={(e) => setStudentName(e.target.value)}
            placeholder="e.g. Aiden"
            className="mt-1"
          />
        </div>

        <div>
          <Label htmlFor="level">Level *</Label>
          <Select value={level} onValueChange={(v) => setLevel(v as any)}>
            <SelectTrigger id="level" className="mt-1">
              <SelectValue placeholder="Choose Sec 1–4" />
            </SelectTrigger>
            <SelectContent>
              {LEVELS.map((l) => (
                <SelectItem key={l.value} value={l.value}>
                  {l.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <Label htmlFor="paperNumber">Paper</Label>
            <Select value={paperNumber} onValueChange={setPaperNumber}>
              <SelectTrigger id="paperNumber" className="mt-1">
                <SelectValue placeholder="Optional" />
              </SelectTrigger>
              <SelectContent>
                {PAPER_NUMBERS.map((p) => (
                  <SelectItem key={p} value={p}>
                    {p}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div>
            <Label htmlFor="paperDate">Paper date</Label>
            <Input
              id="paperDate"
              type="date"
              value={paperDate}
              onChange={(e) => setPaperDate(e.target.value)}
              className="mt-1"
            />
          </div>
        </div>

        <div>
          <Label htmlFor="school">School</Label>
          <Input
            id="school"
            value={school}
            onChange={(e) => setSchool(e.target.value)}
            placeholder="Optional"
            className="mt-1"
          />
        </div>

        <div className="pt-2 border-t">
          <Label htmlFor="file">Upload paper (optional)</Label>
          <Input
            id="file"
            type="file"
            accept="image/*,application/pdf"
            multiple
            onChange={handleFileChange}
            disabled={uploading}
            className="mt-1"
          />
          {uploading && (
            <p className="text-sm text-muted-foreground mt-2">Uploading…</p>
          )}
          {uploadedIds.length > 0 && (
            <p className="text-sm text-emerald-700 mt-2">
              ✓ {uploadedIds.length} file
              {uploadedIds.length > 1 ? "s" : ""} uploaded
            </p>
          )}
        </div>
      </div>

      <div className="flex flex-col gap-2 pt-4">
        <Button
          onClick={() => save()}
          disabled={!canContinue || saving}
          size="lg"
        >
          {saving ? "Saving…" : "Continue to error log →"}
        </Button>
        <button
          type="button"
          onClick={() => save({ skip: true })}
          disabled={!canContinue || saving}
          className="text-sm text-muted-foreground hover:underline disabled:opacity-50"
        >
          Skip upload — I'll just type the errors
        </button>
      </div>
    </main>
  );
}
