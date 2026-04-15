"use client";
import { useState } from "react";
import { useMutation } from "convex/react";
import { api } from "@/convex/_generated/api";
import type { Id } from "@/convex/_generated/dataModel";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { buildWhatsAppLink } from "@/lib/whatsapp";
import type { Pillar } from "@/lib/pillars";
import { CONSULT_DURATION_MIN } from "@/lib/constants";

/**
 * Block 5: stacked dual CTA. Primary = WhatsApp deep link (pre-filled msg).
 * Secondary = email the PDF. Email form expands inline when tapped.
 */
export function DualCTA({
  sessionId,
  studentName,
  level,
  verdictPillars,
  pillarPercent,
  topPatternLabel,
}: {
  sessionId: Id<"sessions">;
  studentName?: string;
  level?: string;
  verdictPillars: Pillar[];
  pillarPercent?: number;
  topPatternLabel?: string;
}) {
  const [showEmailForm, setShowEmailForm] = useState(false);
  const [email, setEmail] = useState("");
  const [sending, setSending] = useState(false);
  const [sent, setSent] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const requestEmail = useMutation(api.leads.requestReportEmail);

  const waLink = buildWhatsAppLink({
    studentName,
    level,
    verdictPillars,
    pillarPercent,
    topPatternLabel,
  });

  async function handleSendEmail() {
    if (!email.includes("@")) {
      setError("Please enter a valid email.");
      return;
    }
    setError(null);
    setSending(true);
    try {
      await requestEmail({ sessionId, email: email.trim() });
      setSent(true);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong.");
    } finally {
      setSending(false);
    }
  }

  return (
    <section className="space-y-3">
      <h2 className="text-xl font-semibold">What's next</h2>
      <div className="space-y-3">
        <a
          href={waLink}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center justify-center gap-2 w-full rounded-xl bg-green-600 hover:bg-green-700 text-white font-semibold px-6 py-4 text-base shadow-sm transition"
        >
          <svg
            viewBox="0 0 24 24"
            className="h-5 w-5 fill-current"
            aria-hidden="true"
          >
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51l-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.693.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z" />
          </svg>
          Book a {CONSULT_DURATION_MIN}-min FAST consult on WhatsApp
        </a>

        {!showEmailForm && !sent && (
          <button
            type="button"
            onClick={() => setShowEmailForm(true)}
            className="w-full text-sm text-muted-foreground hover:text-foreground underline-offset-4 hover:underline transition py-2"
          >
            Or email me the PDF report
          </button>
        )}

        {showEmailForm && !sent && (
          <div className="rounded-xl border p-4 space-y-3 bg-card">
            <Label htmlFor="email-pdf">Email me the PDF</Label>
            <div className="flex flex-col sm:flex-row gap-2">
              <Input
                id="email-pdf"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={sending}
              />
              <Button onClick={handleSendEmail} disabled={sending}>
                {sending ? "Sending…" : "Send"}
              </Button>
            </div>
            {error && <p className="text-sm text-destructive">{error}</p>}
            <p className="text-xs text-muted-foreground">
              We'll send one email with your PDF and a booking link. No spam.
            </p>
          </div>
        )}

        {sent && (
          <div className="rounded-xl border border-green-200 bg-green-50 p-4 text-sm text-green-800 space-y-2">
            <p>✓ Sent to <strong>{email}</strong>. Check your inbox in a minute or two.</p>
            <button
              type="button"
              onClick={() => {
                setSent(false);
                setEmail("");
              }}
              className="text-xs underline text-green-900"
            >
              Send to a different email
            </button>
          </div>
        )}
      </div>
    </section>
  );
}
