import { PILLAR_META, type Pillar } from "@/lib/pillars";

/**
 * Bridge block (Block 4): names the mechanism (training, not more practice)
 * and the venue (30-min FAST consult). Keeps voice rule §3: specific, not salesy.
 */
export function BridgeParagraph({
  verdictPillars,
}: {
  verdictPillars: Pillar[];
}) {
  const primary = verdictPillars[0];
  const meta = PILLAR_META[primary];

  return (
    <section className="space-y-3 rounded-xl border bg-muted/40 p-5 sm:p-6">
      <h2 className="text-xl font-semibold">What this means</h2>
      <p className="text-base text-foreground/80 leading-relaxed">
        Most students try to fix this by doing <em>more</em> questions. That
        rarely works — because the gap isn't in how much they practise, it's in{" "}
        <strong>how</strong> they practise. The {meta.name} pillar responds to a
        specific kind of training: <strong>{meta.method.toLowerCase()}</strong>
        . That's the piece we'd walk through in a 30-min FAST consult — not a
        sales pitch, just a look at your paper together and the two or three
        moves that would unlock the most marks.
      </p>
    </section>
  );
}
