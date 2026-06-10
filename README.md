# Meta Ads Checklist — a Claude Code skill for Paid Social teams

**One self-contained HTML dashboard for a Meta Ads account: a 45-item Paid Social checklist, an editable spreadsheet where every number is a live formula, anti-anchoring diagnostics, and human instructions for everything the API can't see.**

![downloads](https://img.shields.io/github/downloads/radxlav/meta-ads-verification-opensource-by-rado-kmita/total) ![stars](https://img.shields.io/github/stars/radxlav/meta-ads-verification-opensource-by-rado-kmita)

**[⬇ Download the ZIP (latest release)](https://github.com/radxlav/meta-ads-verification-opensource-by-rado-kmita/releases/latest)**

Free, MIT-licensed. Built by [Radosław Kmita](https://www.linkedin.com/in/radoslawkmita/) + Hubert (Paid Social) at MTA Digital.

![what you get](#) <!-- optional: drop a screenshot here -->

## Why

- **I hate black-box AI dashboards.** Here the TOTAL tab is a real spreadsheet (Handsontable + HyperFormula) where monthly numbers are `SUMIF` formulas over raw ad-level rows. Click a cell → the fx bar shows exactly how it was calculated. Zero hand-typed numbers.
- **Meta Ads MCP first.** The primary (and sufficient) data source is your Meta Ads MCP, read-only. No draining of BigQuery / Supermetrics / Dataslayer quotas — those are only an optional add-on for the 3-attribution-window comparison.
- **Human instructions included.** Every checklist item that can't be proven from the export tells you where to click in Ads Manager / Events Manager (with links), what to screenshot, and deep-links to the exact spreadsheet cell with the evidence.
- **Anti-anchoring diagnostics.** When ROAS tanks, the dashboard doesn't jump to "creative fatigue". A day-over-day step-scan, a funnel-break detector, and a fatigue-refutation rule (frequency↑ AND CTR↓ per creative, or the theory dies) keep you from killing a winning creative.

## What's inside

```
meta-ads-verification-opensource-by-rado-kmita/
├── SKILL.md                       ← the Claude Code skill (workflow, rules, quality gates)
├── README.md                      ← you are here
├── LICENSE                        ← MIT
└── references/
    ├── dashboard-skeleton.html    ← full dashboard code, no data, 5 injection markers
    ├── build-data.py              ← CSV → compact JSON encoder
    ├── checklist-starter.md       ← the 45 starter checklist items
    └── DEPLOY.md                  ← step-by-step deployment for any client
```

## Requirements

- **Claude Code** (any recent version). Works great with frontier models (Fable 5 / Opus 4.8).
- **A Meta Ads MCP** connected to your ad account (read-only access is enough — the skill never writes).
- Optional: Dataslayer / Supermetrics / any insights-export tool **only if** you want the side-by-side 1d-click / 7d-click / 7d-click+1d-view attribution comparison. Without it the dashboard runs in single-window mode (account default) — fully supported.

No Meta MCP / no Claude yet? Ping me on LinkedIn — happy to talk you through wiring Claude into your MarTech stack.

## Install (2 minutes)

```bash
# 1. Put the skill where Claude Code looks for skills:
cp -R meta-ads-verification-opensource-by-rado-kmita ~/.claude/skills/meta-ads-verification-opensource-by-rado-kmita

# 2. In your project, start Claude Code and run:
#    /meta-ads-verification-opensource-by-rado-kmita
#    (or just say: "build the Meta Ads checklist dashboard for act_XXXX")
```

Claude will first ask you 3 preflight questions (model, data access, manual data), then pull the data, build the dashboard, verify it in a browser, and finally walk you through the 6 manual checks (EMQ, budget change history, learning phase, LP changes, competitor promos, consent) so the checklist reaches 100%.

## The 8 tabs

| Tab | What it shows |
|---|---|
| 📑 Index & sources | navigation + where every number comes from (provenance) |
| Rollup Campaigns / AdSets | full funnel per entity + audit flags linking into the checklist |
| TOTAL ⭐ | 🔍 day-over-day step-scan · 🪜 funnel-break detector · 🖐 manual-check panel · attribution windows side-by-side · TM vs LM · MoM |
| TM / LM | day-by-day for current/previous month (auto-derived from data) |
| RAW | the actual ad-level rows (18 columns) — the ground truth |
| 📊 Sheet | editable spreadsheet, TOTAL = live SUMIF formulas, fx bar shows every formula |
| 🔬 Placement / Age | breakdowns (optional pull) |
| ✔ Checklist | 45 items: 33 Paid Social rules + 6 diagnostics + 6 manual checks, each with evidence and deep-links |

## FAQ

**Does it send my data anywhere?** No. The output is one local HTML file with the data embedded. It loads chart/spreadsheet libraries from a CDN on first open, then works offline.

**My team doesn't speak Polish.** The dashboard UI ships in Polish (built for PL teams); the skill instructs Claude to translate visible labels into your team's language during deployment.

**Can it modify my campaigns?** No. The skill is read-only by design and explicitly forbids write calls.

**Other channels?** The pattern (RAW → SUMIF TOTAL, checklist with deep-links, diagnostics) ports to Google Ads / TikTok — change the pull and the funnel columns, keep the structure.

## Thanks

If you downloaded it — leave a comment on the LinkedIn post ("thanks bro" works) and tell me what broke or what you'd add. That's the whole price.

MIT © Radosław Kmita
