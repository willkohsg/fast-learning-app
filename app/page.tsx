import Link from "next/link";

export default function LandingPage() {
  return (
    <main className="min-h-screen px-6 py-12 max-w-2xl mx-auto">
      <div className="space-y-8">
        <div className="space-y-2">
          <p className="text-sm font-semibold uppercase tracking-wider text-primary">
            FAST DIAGNOSTIC TOOL
          </p>
          <h1 className="text-4xl font-bold leading-tight sm:text-5xl">
            Find the <span className="text-primary">one pillar</span> costing
            your child the most marks.
          </h1>
          <p className="text-lg text-muted-foreground pt-2">
            A free, 15-minute error-log diagnostic for Sec 1–4 maths students in
            Singapore. Upload a recent paper, log the mistakes, and get a
            personalised report pinpointing the <strong>F</strong>,{" "}
            <strong>A</strong>, <strong>S</strong>, or <strong>T</strong>{" "}
            pillar you need to strengthen.
          </p>
        </div>

        <Link
          href="/diagnostic/new"
          className="inline-flex items-center justify-center rounded-lg bg-primary px-8 py-4 text-lg font-semibold text-primary-foreground shadow-sm hover:opacity-90 transition"
        >
          Start the diagnostic →
        </Link>

        <div className="pt-8 border-t space-y-4 text-sm text-muted-foreground">
          <div className="grid sm:grid-cols-3 gap-4">
            <div>
              <p className="font-semibold text-foreground">⏱ 15 minutes</p>
              <p>One error per screen. No fluff.</p>
            </div>
            <div>
              <p className="font-semibold text-foreground">🔒 Private</p>
              <p>No login. Auto-deleted in 24 hours.</p>
            </div>
            <div>
              <p className="font-semibold text-foreground">📊 Specific</p>
              <p>Every insight cites your own errors.</p>
            </div>
          </div>
          <p className="pt-4">
            By Cambridge Learning Group — maths tuition, Singapore.
          </p>
        </div>
      </div>
    </main>
  );
}
