import { tavily } from "@tavily/core";
import Groq from "groq-sdk";
import { NextRequest, NextResponse } from "next/server";

export const maxDuration = 60; // Vercel Pro max; free tier will cap at 10s

export async function POST(req: NextRequest) {
  // Move client initialization inside the handler to prevent build-time crashes if keys are missing
  const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });
  const tv = tavily({ apiKey: process.env.TAVILY_API_KEY! });

  const { claim, imageUrl } = await req.json();

  if (!claim?.trim()) {
    return NextResponse.json({ error: "No claim provided" }, { status: 400 });
  }

  // ── 1. Live web search ──────────────────────────────────────────────────
  let searchContext = "";
  const sources: { title: string; url: string; snippet: string }[] = [];
  try {
    const searchResult = await tv.search(claim, {
      searchDepth: "advanced",
      maxResults: 6,
      includeAnswer: true,
    });

    if (searchResult.answer) {
      searchContext += `SEARCH SUMMARY: ${searchResult.answer}\n\n`;
    }
    searchContext += "TOP SOURCES:\n";
    for (const r of searchResult.results) {
      searchContext += `- ${r.title}\n  ${r.content?.slice(0, 350)}\n  URL: ${r.url}\n\n`;
      sources.push({ title: r.title, url: r.url, snippet: r.content?.slice(0, 200) ?? "" });
    }

    // Optional image context
    if (imageUrl?.trim()) {
      const imgSearch = await tv.search(`fact check image original source: ${imageUrl}`, {
        maxResults: 3,
      });
      searchContext += "\nIMAGE CONTEXT:\n";
      for (const r of imgSearch.results) {
        searchContext += `- ${r.title}: ${r.content?.slice(0, 200)}\n`;
      }
    }
  } catch (e: unknown) {
    console.error("Tavily error:", e);
    searchContext = "Search unavailable. Analyse based on general knowledge.";
  }

  // ── 2. Groq reasoning ──────────────────────────────────────────────────
  const systemPrompt = `You are an elite fact-checking AI. Given a claim and live web research results, produce a verdict.
You MUST respond with ONLY a valid JSON object — no markdown, no preamble, no explanation outside the JSON.

Required format:
{
  "verdict": "<2-4 sentence summary of findings>",
  "label": "<one of: TRUE | MOSTLY TRUE | MIXED | MOSTLY FALSE | FALSE | UNVERIFIABLE>",
  "confidence": <integer 0-100>,
  "key_findings": ["<finding 1>", "<finding 2>", "<finding 3>"]
}`;

  const userPrompt = `CLAIM: "${claim}"

LIVE RESEARCH DATA:
${searchContext}

Produce the JSON verdict now.`;

  let parsed: {
    verdict: string;
    label: string;
    confidence: number;
    key_findings: string[];
  } | null = null;

  try {
    const chat = await groq.chat.completions.create({
      model: "llama-3.3-70b-versatile",
      messages: [
        { role: "system", content: systemPrompt },
        { role: "user", content: userPrompt },
      ],
      temperature: 0.3,
      max_tokens: 800,
      response_format: { type: "json_object" },
    });

    const raw = chat.choices[0]?.message?.content ?? "{}";
    parsed = JSON.parse(raw);
  } catch (e) {
    console.error("Groq error:", e);
    return NextResponse.json({ error: "Analysis failed. Please try again." }, { status: 500 });
  }

  return NextResponse.json({
    verdict: parsed?.verdict ?? "Could not determine.",
    label: (parsed?.label ?? "UNVERIFIABLE").toUpperCase(),
    confidence: Math.max(0, Math.min(100, parsed?.confidence ?? 50)),
    key_findings: parsed?.key_findings ?? [],
    sources,
  });
}
