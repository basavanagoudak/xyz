# 🛡️ RealityCheck AI

> **Multi-agent AI fact-checker** — verify any claim in seconds using live web search and LLM reasoning.

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/basavanagoudak/xyz)

---

## ✨ What It Does

RealityCheck AI takes any claim, news headline, or statement and:

1. **Searches the live web** via Tavily — pulling real sources, expert opinions, and fact-checks
2. **Reasons with Llama 3.3 70B** (via Groq) — weighs evidence and counter-evidence
3. **Returns a structured verdict** — label, confidence score, key findings, and cited sources

---

## 🧠 Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 15 (App Router), React, Vanilla CSS |
| AI Reasoning | Groq — Llama 3.3 70B Versatile |
| Live Search | Tavily Search API |
| Deployment | Vercel |

---

## 🚀 Deploy to Vercel

1. Click the **Deploy with Vercel** button above
2. Add these environment variables in the Vercel dashboard:

| Variable | Where to get it |
|---|---|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) |
| `TAVILY_API_KEY` | [tavily.com](https://tavily.com) |

3. Deploy ✅

---

## 🛠️ Local Development

```bash
# 1. Clone
git clone https://github.com/basavanagoudak/xyz.git
cd xyz

# 2. Install dependencies
npm install

# 3. Add API keys
cp .env.local.example .env.local
# Fill in GROQ_API_KEY and TAVILY_API_KEY

# 4. Run
npm run dev
# → http://localhost:3000
```

---

## 📁 Project Structure

```
├── app/
│   ├── api/analyze/route.ts   # API: Tavily search + Groq reasoning
│   ├── page.tsx               # Main UI
│   ├── layout.tsx             # Root layout + metadata
│   └── globals.css            # Premium dark theme
├── .env.local                 # API keys (not committed)
└── package.json
```

---

## 🏷️ Verdict Labels

| Label | Meaning |
|---|---|
| ✅ TRUE | Strongly supported by evidence |
| 🟢 MOSTLY TRUE | Largely accurate with minor caveats |
| ⚖️ MIXED | Disputed — evidence on both sides |
| 🟠 MOSTLY FALSE | Largely inaccurate |
| ❌ FALSE | Definitively debunked |
| ❓ UNVERIFIABLE | Insufficient public evidence |
