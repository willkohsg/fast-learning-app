"use client";
import { Button } from "@/components/ui/button";

/**
 * Inserted every 5 errors (5, 10, 15). Research shows these "plan-building"
 * reassurance screens lift conversion 10-20% by reframing effort as investment
 * (UX research §1.1 Noom, §2.1).
 */
export function ReassuranceScreen({
  count,
  onContinue,
}: {
  count: number;
  onContinue: () => void;
}) {
  const message =
    count === 5
      ? {
          headline: "Great — your report is now unlocked.",
          sub: "But 5 errors is the minimum. Students who log 10+ get a meaningfully sharper diagnosis. Keep going — or stop here if you're short on time.",
        }
      : count === 10
        ? {
            headline: "10 errors — diagnostic-grade detail.",
            sub: "This is the volume we look at in a live consult. Every extra error now makes one of the FAST pillars harder to mis-identify. Push to 15 for the sharpest read.",
          }
        : {
            headline: "15 errors — rigorous sample.",
            sub: "You can stop any time from here. More is still better, but the marginal gain levels off. Wrap up when you're ready.",
          };

  return (
    <main className="min-h-screen flex items-center justify-center px-6 py-10">
      <div className="max-w-md space-y-6 text-center">
        <div className="text-5xl">📊</div>
        <div className="space-y-2">
          <h2 className="text-2xl font-bold">{message.headline}</h2>
          <p className="text-muted-foreground">{message.sub}</p>
        </div>
        <Button onClick={onContinue} size="lg" className="w-full">
          Keep logging errors →
        </Button>
      </div>
    </main>
  );
}
