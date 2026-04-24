"use client";

import { useState, useRef } from "react";

// ── Types ───────────────────────────────────────────────────────────────────
interface Source { title: string; url: string; snippet: string }
interface Result {
  verdict: string;
  label: string;
  confidence: number;
  key_findings: string[];
  sources: Source[];
}

// ── Label config ────────────────────────────────────────────────────────────
const LABELS: Record<string, { icon: string; color: string; text: string }> = {
  TRUE:          { icon: "✅", color: "#10b981", text: "VERIFIED TRUE"   },
  MOSTLY_TRUE:   { icon: "🟢", color: "#34d399", text: "MOSTLY TRUE"     },
  "MOSTLY TRUE": { icon: "🟢", color: "#34d399", text: "MOSTLY TRUE"     },
  MIXED:         { icon: "⚖️", color: "#f59e0b", text: "MIXED / DISPUTED"},
  MOSTLY_FALSE:  { icon: "🟠", color: "#f97316", text: "MOSTLY FALSE"    },
  "MOSTLY FALSE":{ icon: "🟠", color: "#f97316", text: "MOSTLY FALSE"    },
  FALSE:         { icon: "❌", color: "#ef4444", text: "VERIFIED FALSE"  },
  UNVERIFIABLE:  { icon: "❓", color: "#94a3b8", text: "UNVERIFIABLE"    },
};

const cssLabel = (l: string) => l.toUpperCase().replace(/\s+/g, "_");

const EXAMPLES = [
  "Did Tesla's global car sales fall by 30% in early 2024?",
  "Is coffee linked to cancer according to latest research?",
  "Was the Great Wall of China visible from space?",
];

const STEPS = [
  "🔎 Searching live web sources…",
  "🧠 Analysing evidence with Llama 3.3…",
  "⚖️  Weighing findings & scoring confidence…",
];

// ── Component ────────────────────────────────────────────────────────────────
export default function Home() {
  const [claim, setClaim] = useState("");
  const [imageUrl, setImageUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(0);
  const [result, setResult] = useState<Result | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<(Result & { claim: string })[]>([]);
  const resultRef = useRef<HTMLDivElement>(null);

  async function handleAnalyze() {
    if (!claim.trim()) return;
    setLoading(true);
    setError(null);
    setResult(null);
    setStep(0);

    // Animate steps
    const stepTimer = setInterval(() => setStep((s) => Math.min(s + 1, STEPS.length - 1)), 2200);

    try {
      const res = await fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ claim: claim.trim(), imageUrl: imageUrl.trim() }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error ?? "Analysis failed");
      setResult(data);
      setHistory((h) => [{ ...data, claim: claim.trim() }, ...h.slice(0, 6)]);
      setTimeout(() => resultRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }), 100);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Something went wrong.");
    } finally {
      clearInterval(stepTimer);
      setLoading(false);
      setStep(0);
    }
  }

  const meta = result ? (LABELS[result.label] ?? LABELS.UNVERIFIABLE) : null;
  const cl = result ? cssLabel(result.label) : "";

  return (
    <main className="wrapper">
      {/* ── Header ──────────────────────────────────────────── */}
      <header className="header">
        <div className="header-logo">
          <div className="header-logo-icon">🛡️</div>
          <span className="header-logo-text">RealityCheck AI</span>
        </div>
        <div className="header-badge">Groq · Llama 3.3 · Tavily</div>
      </header>

      {/* ── Hero ─────────────────────────────────────────────── */}
      <section className="hero">
        <h1 className="hero-title">Truth, Verified.</h1>
        <p className="hero-sub">
          Multi-agent AI that searches the live web, weighs evidence, and delivers a
          confidence-scored verdict on any claim in seconds.
        </p>
        <div className="hero-pills">
          <span className="hero-pill">Live Web Search</span>
          <span className="hero-pill">Llama 3.3 70B</span>
          <span className="hero-pill">Source Citations</span>
          <span className="hero-pill">Confidence Score</span>
        </div>
      </section>

      {/* ── KPI bar ──────────────────────────────────────────── */}
      <div className="kpi-bar">
        <div className="kpi-card">
          <div className="kpi-val">{history.length}</div>
          <div className="kpi-lbl">Claims This Session</div>
        </div>
        <div className="kpi-card">
          <div className="kpi-val">{history.filter(h => ["TRUE","MOSTLY TRUE"].includes(h.label)).length}</div>
          <div className="kpi-lbl">Verified True</div>
        </div>
        <div className="kpi-card">
          <div className="kpi-val">{history.filter(h => ["FALSE","MOSTLY FALSE"].includes(h.label)).length}</div>
          <div className="kpi-lbl">Flagged False</div>
        </div>
        <div className="kpi-card">
          <div className="kpi-val">
            {history.length > 0 ? Math.round(history.reduce((s,h) => s+h.confidence,0)/history.length) + "%" : "—"}
          </div>
          <div className="kpi-lbl">Avg Confidence</div>
        </div>
      </div>

      {/* ── Main two-col grid ─────────────────────────────────── */}
      <div className="grid2">

        {/* LEFT — Input ─────────────────────────────────────── */}
        <div>
          <div className="sec-heading">📥 Ingestion Terminal</div>
          <div className="card mb24">
            <label className="input-label">Claim or Statement</label>
            <textarea
              value={claim}
              onChange={(e) => setClaim(e.target.value)}
              placeholder="e.g. 'Tesla sales fell 30% in Q1 2024' or paste any news excerpt…"
              onKeyDown={(e) => e.key === "Enter" && e.metaKey && handleAnalyze()}
            />

            <div className="divider" />

            <label className="input-label">Image URL (optional)</label>
            <input
              type="text"
              value={imageUrl}
              onChange={(e) => setImageUrl(e.target.value)}
              placeholder="https://example.com/image.jpg"
            />

            <button
              className="btn-primary"
              onClick={handleAnalyze}
              disabled={loading || !claim.trim()}
            >
              {loading ? "Analysing…" : "🔍 Execute Analysis"}
            </button>
          </div>

          {/* Quick examples */}
          <div className="sec-heading">⚡ Quick Examples</div>
          {EXAMPLES.map((ex) => (
            <button
              key={ex}
              className="btn-example"
              onClick={() => { setClaim(ex); setResult(null); setError(null); }}
            >
              → {ex}
            </button>
          ))}

          {/* Session history */}
          {history.length > 0 && (
            <>
              <div className="sec-heading" style={{ marginTop: 28 }}>🕒 Recent Analyses</div>
              {history.map((h, i) => {
                const m = LABELS[h.label] ?? LABELS.UNVERIFIABLE;
                return (
                  <div
                    key={i}
                    className="btn-example"
                    style={{ cursor: "pointer", borderColor: "rgba(79,172,254,0.18)" }}
                    onClick={() => setResult(h)}
                  >
                    <span style={{ color: m.color, fontWeight: 700, fontSize: "0.75rem" }}>
                      {m.icon} {m.text}
                    </span>
                    <div style={{ fontSize: "0.8rem", color: "#64748b", marginTop: 3, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                      {h.claim.slice(0, 60)}{h.claim.length > 60 ? "…" : ""}
                    </div>
                  </div>
                );
              })}
            </>
          )}
        </div>

        {/* RIGHT — Results ──────────────────────────────────── */}
        <div ref={resultRef}>
          <div className="sec-heading">📡 Verdict & Intelligence Report</div>

          {/* Loading */}
          {loading && (
            <div className="card">
              <div className="loading-box">
                <div className="loader-ring" />
                <div className="loading-text">CREW ANALYSING…</div>
                <div className="loading-steps">
                  {STEPS.map((s, i) => (
                    <div key={i} className={`loading-step ${i < step ? "done" : i === step ? "active" : ""}`}>
                      {i < step ? "✓" : i === step ? "›" : "○"} {s}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Error */}
          {!loading && error && (
            <div className="error-box">⚠️ <span>{error}</span></div>
          )}

          {/* Awaiting */}
          {!loading && !result && !error && (
            <div className="awaiting">
              <div className="awaiting-icon">🛡️</div>
              <div>Enter a claim and hit <strong style={{ color: "#4facfe" }}>Execute</strong></div>
            </div>
          )}

          {/* Result */}
          {!loading && result && meta && (
            <>
              {/* Verdict card */}
              <div className={`verdict-card verdict-${cl} mb24`}>
                <div className="verdict-icon">{meta.icon}</div>
                <div className={`verdict-label-badge badge-${cl}`}>{meta.text}</div>
                <p className="verdict-text">{result.verdict}</p>
              </div>

              {/* Confidence */}
              <div className="card conf-section mb24">
                <div className="conf-header">
                  <span className="conf-label">Confidence Score</span>
                  <span className="conf-value" style={{ color: meta.color }}>{result.confidence}%</span>
                </div>
                <div className="conf-bar-track">
                  <div className="conf-bar-fill" style={{ width: `${result.confidence}%`, background: `linear-gradient(90deg, ${meta.color}, ${meta.color}aa)` }} />
                </div>
              </div>

              {/* Key Findings */}
              {result.key_findings?.length > 0 && (
                <div className="card mb24">
                  <div className="sec-heading">🔍 Key Findings</div>
                  <div className="findings-list">
                    {result.key_findings.map((f, i) => (
                      <div key={i} className="finding-item">
                        <span className="finding-dot">›</span>
                        <span>{f}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Sources */}
              {result.sources?.length > 0 && (
                <div className="card">
                  <div className="sec-heading">📎 Cited Sources</div>
                  <div className="sources-grid">
                    {result.sources.slice(0, 6).map((s, i) => {
                      let domain = s.url;
                      try { domain = new URL(s.url).hostname; } catch {}
                      return (
                        <a key={i} href={s.url} target="_blank" rel="noopener noreferrer" className="source-pill" title={s.title}>
                          🔗 {domain}
                        </a>
                      );
                    })}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </main>
  );
}
