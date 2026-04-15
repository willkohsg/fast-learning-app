import {
  Document,
  Page,
  Text,
  View,
  StyleSheet,
} from "@react-pdf/renderer";
import { PILLAR_META, type Pillar } from "./pillars";
import { CONSULT_DURATION_MIN, BRAND, TOOL_NAME } from "./constants";

/**
 * React-PDF document for the diagnostic report. Mirrors the on-screen
 * report blocks but tuned for print: greyscale-friendly, no images,
 * single-page where possible. Rendered server-side in a Convex node action.
 */

const styles = StyleSheet.create({
  page: {
    padding: 40,
    fontSize: 11,
    fontFamily: "Helvetica",
    color: "#1f2937",
  },
  brandRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    fontSize: 9,
    color: "#6b7280",
    marginBottom: 18,
    borderBottom: "1pt solid #e5e7eb",
    paddingBottom: 8,
  },
  hero: {
    border: "2pt solid #1f2937",
    borderRadius: 8,
    padding: 16,
    marginBottom: 18,
  },
  heroBadge: {
    fontSize: 28,
    fontFamily: "Helvetica-Bold",
    marginBottom: 4,
  },
  heroLabel: {
    fontSize: 9,
    color: "#6b7280",
    textTransform: "uppercase",
    letterSpacing: 1,
    marginBottom: 4,
  },
  heroHeadline: {
    fontSize: 16,
    fontFamily: "Helvetica-Bold",
    marginBottom: 8,
  },
  heroSubline: {
    fontSize: 11,
    color: "#374151",
    marginTop: 8,
    paddingTop: 8,
    borderTop: "1pt solid #e5e7eb",
  },
  h2: {
    fontSize: 13,
    fontFamily: "Helvetica-Bold",
    marginTop: 14,
    marginBottom: 6,
  },
  para: {
    fontSize: 11,
    lineHeight: 1.5,
    color: "#374151",
  },
  patternCard: {
    border: "1pt solid #e5e7eb",
    borderRadius: 6,
    padding: 10,
    marginBottom: 8,
  },
  patternHead: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginBottom: 4,
  },
  patternLabel: {
    fontSize: 11,
    fontFamily: "Helvetica-Bold",
    flex: 1,
  },
  patternCount: {
    fontSize: 9,
    fontFamily: "Helvetica-Bold",
    color: "#1f2937",
  },
  patternMeta: {
    fontSize: 9,
    color: "#6b7280",
    marginBottom: 4,
  },
  pillarRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    paddingVertical: 6,
    borderBottom: "1pt solid #f3f4f6",
  },
  ctaBox: {
    marginTop: 16,
    padding: 12,
    border: "1pt solid #1f2937",
    borderRadius: 6,
  },
  ctaTitle: {
    fontSize: 12,
    fontFamily: "Helvetica-Bold",
    marginBottom: 4,
  },
  small: {
    fontSize: 8,
    color: "#9ca3af",
    marginTop: 16,
    textAlign: "center",
  },
  bold: { fontFamily: "Helvetica-Bold" },
});

const ORDER: Pillar[] = ["F", "A", "S", "T"];

export function ReportPDF({
  studentName,
  level,
  totalErrors,
  pillarScores,
  verdictPillars,
  topPatterns,
  weakestTopics,
  whatsappLink,
}: {
  studentName?: string;
  level?: string;
  totalErrors: number;
  pillarScores: Record<Pillar, number>;
  verdictPillars: Pillar[];
  topPatterns: {
    label: string;
    count: number;
    qnNumbers: number[];
    interpretation: string;
  }[];
  weakestTopics: string[];
  whatsappLink: string;
}) {
  const primary = verdictPillars[0];
  const meta = PILLAR_META[primary];
  const pct = pillarScores[primary];
  const tied = verdictPillars.length > 1;
  const greeting = studentName ? `${studentName}, ` : "";
  const levelLabel = level ? level.replace(/^sec/, "Sec ") : "";

  return (
    <Document>
      <Page size="A4" style={styles.page}>
        <View style={styles.brandRow}>
          <Text>{TOOL_NAME} · {BRAND}</Text>
          <Text>{new Date().toLocaleDateString("en-SG", { year: "numeric", month: "short", day: "numeric" })}</Text>
        </View>

        {/* Hero verdict */}
        <View style={styles.hero}>
          <Text style={styles.heroBadge}>
            {tied ? verdictPillars.join("/") : primary}
          </Text>
          <Text style={styles.heroLabel}>Your weakest FAST pillar</Text>
          <Text style={styles.heroHeadline}>
            {tied
              ? `${greeting}your weakest pillars are ${verdictPillars.join(" & ")} — tied at ~${pct}% each.`
              : `${greeting}your weakest pillar is ${meta.name} — ${pct}% of your errors.`}
          </Text>
          <Text style={styles.heroSubline}>{meta.subline}</Text>
        </View>

        {/* Evidence */}
        <Text style={styles.h2}>Here's what we saw</Text>
        <Text style={styles.para}>
          Of your <Text style={styles.bold}>{totalErrors}</Text> logged errors,{" "}
          <Text style={styles.bold}>
            {Math.round((pct / 100) * totalErrors)}
          </Text>{" "}
          traced back to the{" "}
          <Text style={styles.bold}>{meta.letter} pillar</Text> ({meta.name}).
          {weakestTopics.length > 0
            ? ` Clustering was strongest in ${weakestTopics.slice(0, 3).join(", ")}. `
            : " "}
          That's {pct}% of your mistakes driven by one pattern — which means
          it's also one of the fastest things to fix.
        </Text>

        {/* Patterns */}
        {topPatterns.length > 0 && (
          <>
            <Text style={styles.h2}>Top recurring patterns</Text>
            {topPatterns.map((p, i) => (
              <View key={i} style={styles.patternCard}>
                <View style={styles.patternHead}>
                  <Text style={styles.patternLabel}>{p.label}</Text>
                  <Text style={styles.patternCount}>{p.count}×</Text>
                </View>
                <Text style={styles.patternMeta}>
                  Q{p.qnNumbers.join(", Q")}
                </Text>
                <Text style={styles.para}>{p.interpretation}</Text>
              </View>
            ))}
          </>
        )}

        {/* Pillar scores */}
        <Text style={styles.h2}>Your full FAST breakdown</Text>
        {ORDER.map((p) => (
          <View key={p} style={styles.pillarRow}>
            <Text>
              <Text style={styles.bold}>{p}</Text> — {PILLAR_META[p].name}
            </Text>
            <Text style={styles.bold}>{pillarScores[p]}%</Text>
          </View>
        ))}

        {/* Bridge + CTA */}
        <View style={styles.ctaBox}>
          <Text style={styles.ctaTitle}>What this means</Text>
          <Text style={styles.para}>
            Most students try to fix this with more practice. The {meta.name}{" "}
            pillar responds to a specific kind of training:{" "}
            <Text style={styles.bold}>{meta.method.toLowerCase()}</Text>. That's
            what we'd walk through in a {CONSULT_DURATION_MIN}-min FAST consult.
          </Text>
          <Text style={[styles.para, { marginTop: 8 }]}>
            <Text style={styles.bold}>Book on WhatsApp:</Text> {whatsappLink}
          </Text>
        </View>

        <Text style={styles.small}>
          {levelLabel ? `${levelLabel} · ` : ""}This report is a starting point,
          not a diagnosis. Data held 24h then purged. © {BRAND}
        </Text>
      </Page>
    </Document>
  );
}
