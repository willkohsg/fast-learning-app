"use client";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { PILLAR_META, type Pillar } from "@/lib/pillars";

const ORDER: Pillar[] = ["F", "A", "S", "T"];

export function PillarsAccordion({
  pillarScores,
  verdictPillars,
}: {
  pillarScores: Record<Pillar, number>;
  verdictPillars: Pillar[];
}) {
  const others = ORDER.filter((p) => !verdictPillars.includes(p));
  if (others.length === 0) return null;

  return (
    <section className="space-y-3">
      <h2 className="text-xl font-semibold">Your other pillars</h2>
      <p className="text-sm text-muted-foreground">
        These aren't your weakest — but they still shape your overall score.
      </p>
      <Accordion type="multiple" className="w-full">
        {others.map((p) => {
          const meta = PILLAR_META[p];
          return (
            <AccordionItem key={p} value={p}>
              <AccordionTrigger>
                <span className="flex items-center gap-3">
                  <span
                    className={`inline-flex h-8 w-8 items-center justify-center rounded-md ${meta.bgClass} ${meta.textClass} font-bold`}
                  >
                    {p}
                  </span>
                  <span className="text-left">
                    <span className="block font-semibold">{meta.name}</span>
                    <span className="text-xs text-muted-foreground">
                      {pillarScores[p]}% of your errors
                    </span>
                  </span>
                </span>
              </AccordionTrigger>
              <AccordionContent>
                <p className="text-sm text-foreground/80">{meta.oneLiner}</p>
                <p className="text-xs text-muted-foreground mt-2">
                  Method: {meta.method}
                </p>
              </AccordionContent>
            </AccordionItem>
          );
        })}
      </Accordion>
    </section>
  );
}
