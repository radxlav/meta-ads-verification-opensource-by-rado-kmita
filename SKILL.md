---
name: meta-ads-verification-opensource-by-rado-kmita
version: 2.1.0-public
status: active
license: MIT
author: Radosław Kmita (AI/strategy) + Hubert (Paid Social rules & sheet structure), MTA Digital
description: Builds a detailed, self-contained Meta Ads dashboard (1 HTML file) with a 45-item Paid Social checklist (rules + anti-anchoring diagnostics + manual-check), an editable open-source spreadsheet (RAW + TOTAL with live SUMIF formulas — every metric traceable), placement/age breakdowns, and a redesigned TOTAL section (day-over-day step-scan, funnel-break detection, manual-check panel). Pulls data primarily from Meta Ads MCP (read-only); attribution-window comparison is an optional add-on. Asks the user preflight questions and guides them to 100% checklist coverage with human instructions for the Meta Ads panel.
trigger-phrases:
  - meta ads checklist
  - meta ads dashboard with checklist
  - simple dash meta
  - meta-ads-verification-opensource-by-rado-kmita
inputs:
  - Meta ad account id (act_<id>) reachable through your Meta Ads MCP
  - period (default: last 2 months)
  - optional: per-window exports (1d_click / 7d_click / 7d_click+1d_view) if you have Dataslayer/Supermetrics or any insights export tool
  - manual data from the user (items 40–45 — EMQ, budget change history, learning phase, LP changelog, competitor promos, consent)
outputs:
  - ./dashboards/meta-ads/simple-dash.html (self-contained; works offline after first CDN load)
  - raw CSVs in ./raw/<YYYY-MM>/ (audit trail) + manual materials in ./raw/<YYYY-MM>/manual/
---

# meta-ads-verification-opensource-by-rado-kmita (public edition)

**Trigger:** `/meta-ads-verification-opensource-by-rado-kmita` or "build the Meta Ads checklist dashboard".

## Why this exists

Most AI-generated dashboards are black boxes — you can't backtrack how a metric was computed. This one fights that:

1. **Open-source spreadsheet inside the dashboard** — TOTAL rows are live `SUMIF` formulas over RAW ad-level rows (Handsontable + HyperFormula). Click any cell → the fx bar shows the exact formula. Zero hand-typed numbers.
2. **Meta Ads MCP first** — the primary pull is your Meta Ads MCP (read-only). No draining of BigQuery/Supermetrics/Dataslayer quotas. Those are only an *optional* add-on for the 3-attribution-window comparison.
3. **Human instructions everywhere** — every checklist item that can't be proven from API data tells you exactly where to click in the Meta Ads panel / Events Manager (with links), what to screenshot/export, and links to the exact spreadsheet cell that holds the evidence.

## Step 0 — PREFLIGHT (ask the user BEFORE doing anything)

Use **AskUserQuestion** (one call, max 3 questions). Don't assume — ask and note the answers:

1. **Model:** "Recommended model for this build is a frontier model — **Fable 5 / Opus 4.8** (`/model`). Big file, formulas, reconciliation. Are you on one (or knowingly staying on your current model)?" If they want to switch, let THEM switch and confirm — never assume they did.
2. **Data access:** "Is a Meta Ads MCP connected for this account? (Optional: do you also have Dataslayer/Supermetrics for per-attribution-window pulls?)" → adjust the pull plan. **No per-window tool = single-window mode** — fully supported, the two other window columns show "—" and their buttons are disabled.
3. **Manual data:** "After the build I'll guide you through 6 things the API can't see (EMQ, budget change history, learning phase, LP changes, competitor promos, consent). Provide now / later / skip?" → determines whether you finish at ~87% or 100% checklist coverage.

Apply the same pattern mid-flow: whenever you recommend an action outside your control (model switch, enabling a connector, a click in the client's ad account) — **ask whether it was done** before building the next step on it.

## Tabs (fixed structure — do NOT add new tabs)

1. **📑 Index & data sources** — navigation grid + provenance table (platform / client / synthesis tags). No monthly KPIs, no "top signals" — data lives in TOTAL/Sheet.
2. **Rollup CAMPAIGNS / ADSETS** — per entity: full funnel, ROAS, audit flags, "🔎 Signals → checklist" column (click = jump to the checklist item, highlighted).
3. **TOTAL** ⭐ (redesigned) — order:
   1. **🔍 Day-over-day step-scan**: days where |Δ d/d| > 30% on Cost/CPM/CTR/click→ATC; ≥2 metrics jumping the same day = delivery/budget change, NOT creative fatigue (fatigue decays per creative, gradually — it doesn't cliff the whole account overnight).
   2. **🪜 Where the funnel breaks — TM vs LM**: CTR → click→ATC → ATC→Checkout → Checkout→Purchase with Δ%; worst step highlighted 🔴 + a "when it drops → look at" column (traffic vs site vs tracking).
   3. **🖐 Manual checks**: CHECK items with `mtg='MANUAL'` — status, "where to get it" instruction, deep-link `↗ checklist #N`. Delivered/total counter.
   4. Conversions by attribution window (side-by-side; missing windows show "—").
   5. TM vs LM + day-by-day ROAS.
   6. Month-over-month totals.
4. **TM / LM** — day-by-day (current / previous month, auto-derived from data).
5. **RAW** (TM / LM / full) — raw ad-level rows (18 columns).
6. **📊 Sheet** (last tab, Sheets icon) — Handsontable 13 + HyperFormula 2.6; TOTAL = SUMIF over RAW; mandatory fx bar.
7. **🔬 Placement / 🔬 Age** — breakdowns in the RAW schema (optional pull; friendly placeholder if skipped).
8. **✔ Checklist** — 45 items (33 universal rules + 34–39 diagnostics + 40–45 MANUAL + items from your team's meetings), statuses ✅/⚠️/◷/⛔, "↗ cell" deep-links.

## 1:1 reproduction — CRITICAL (read first)

**Do NOT build the dashboard from scratch from this description — that yields a worse result.** All the code (charts, attribution engine, `totalDiag()`, spreadsheet, fx bar, checklist, polish) lives in the ready skeleton. Your job = pull data and inject it into the markers.

**Files in `references/` (source of truth):**
- **`DEPLOY.md`** — step-by-step deployment + placeholder swap-map + verification checklist.
- **`dashboard-skeleton.html`** — full working file (~67 KB), code only, NO data. 5 markers: `/*__INJECT_DATA__*/`, `/*__INJECT_BRK__*/`, `/*__INJECT_BREAKDOWNS__*/`, `/*__INJECT_CHECK__*/`, `/*__INJECT_CMAP__*/`. Tolerates single-window data and missing breakdowns.
- **`build-data.py`** — encoder: pull CSVs → `/tmp/DATA.json` + `/tmp/BRK.json` (exact `craw`/`lut`/`month`/`tm`/`lm`/`camp`/`adset` shape). Months auto-detected from data.
- **`checklist-starter.md`** — the 45 starter items + CHECK schema + FLAGMAP/auditSignals.

**Copy-and-inject procedure:**
1. `cp references/dashboard-skeleton.html <your-project>/dashboards/meta-ads/simple-dash.html`
2. Pull data (Workflow below) → CSVs into `./raw/<YYYY-MM>/` using the names from `build-data.py`.
3. `python3 references/build-data.py` (from the raw dir) → `/tmp/DATA.json`, `/tmp/BRK.json`.
4. Inject the 5 blocks (DATA / BRK / BREAKDOWNS / CHECK — remember the `MANUAL` rows, the 🖐 panel reads them / CMAP cell-links once you know the numbers).
5. Swap 5 placeholders: `__AGENCY__`, `__CLIENT__`, `__META_ACCOUNT_ID__`, `__CURRENCY__`, `__PERIOD__`.
6. **Localize:** the skeleton UI ships in Polish (built for PL teams). If the team language is different — translate the *visible* UI strings (tab labels, card titles, table headers, notes) in the OUTPUT file. Never touch identifiers, code, or formulas.
7. `node --check` on the `<script>` block; verify in a browser (Quality gates below).

## Workflow (data pull — Meta Ads MCP first)

1. **Currency + scope verification (anti-contamination)** — pull account-level insights from Meta Ads MCP → confirm the currency (the `amount_spent`/spend prefix) and the account name. NEVER assume the currency. If you copy a layout from another client — copy ONLY the layout, NEVER the data.
2. **PRIMARY pull — Meta Ads MCP** (read-only, e.g. `ads_get_ad_entities`): ad-level × day (`time_increment=1`) for the period; fields: spend, reach, impressions, link/outbound clicks, landing page views, content views, adds to cart, checkouts initiated, purchases, purchase value, add payment info (from `actions`/`action_values`). Write to CSV with the 18 headers expected by `build-data.py`, file name `meta-adlevel-7dc1dv.csv` (the account-default window — on most accounts that IS 7d click + 1d view). **This alone is enough for the full dashboard** (single-window mode).
3. **OPTIONAL — per-window pulls** (only if the user has Dataslayer/Supermetrics or similar): `1d_click`, `7d_click`, `7d_click+1d_view` → `meta-adlevel-1dc.csv`, `-7dc.csv`, `meta-3windows-7dc1dv.csv`. Enables the 3-window comparison + global attribution switcher. Mind the tool's quota — do not drain it if the user didn't ask for windows.
4. **OPTIONAL — breakdowns from Meta MCP**: `breakdowns=publisher_platform` and `age`, `time_increment=1` + account-level `frequency`. Skipped → those tabs show a friendly placeholder, everything else works.
5. **Encode** with `build-data.py`; **inject**; charts (sorted bars / trend / 100% stacked + ROAS/CPA overlay line), `[K:V]` naming-convention parser — all already in the skeleton.
6. **Spreadsheet**: TOTAL = SUMIF over RAW. The fx bar is mandatory (`showFx` reads `getSourceDataAtCell`); persistence uses `getSourceData()` (NOT `getData()` — that would bake formulas into values).
7. **Checklist (45 items)**: rules × numbers from the pull → statuses; 34–39 from the 🔍/🪜 panels; 40–45 stay `todo` until the user delivers materials.
8. **Verify** (browser/Playwright): 0 console errors; reconciliation raw == TOTAL == TM+LM == rollups; 0 `#` errors in the sheet; diagnostics panels render; 🖐 deep-links jump.

## Final step — CLOSE THE MANUAL CHECKS (guide the user to 100%)

Show the user items 40–45 with instructions. For each: **where to click → what to grab (CSV/screenshot) → where to drop it** (`./raw/<YYYY-MM>/manual/`):

| # | What | Where in the account | Material |
|---|---|---|---|
| 40 | EMQ / pixel + CAPI | Events Manager → Data sources → pixel → "Event Match Quality" (target ≥6.0 for Purchase) | screenshot |
| 41 | Budget/bid change history | Ads Manager → clock icon "Change history" → range = dashboard period → filter Budget/Bid | screenshot/export |
| 42 | Learning phase | Ads Manager → ad set list → "Delivery" column | screenshot |
| 43 | Landing page changes | GTM → Versions (publish dates) + site changelog from dev/client | dates + notes |
| 44 | Competitor promos | Meta Ads Library → competitor page → country → active ads in the drop window | screenshots |
| 45 | Consent / cookie banner | CMP panel + GTM Versions | change dates |

When the user delivers: update the CHECK status (`ok`/`warn`) + evidence (a concrete number/date + file name); the 🖐 panel shows progress automatically. Cross-reference items 41 & 43 **with the dates from the 🔍 panel** (a d/d step + a budget change on the same date = root cause found). If the user skips — leave `todo` and say plainly e.g. "checklist 39/45, here's what's missing and how to get it."

## Diagnostic rules (anti-anchoring — non-negotiable when interpreting)

- **Fatigue only with proof:** frequency↑ AND CTR↓ over 2–4 weeks *per creative*. Otherwise the theory is refuted — do not recommend killing the creative.
- **Multiple metrics jumping the same day** = delivery/budget (check #41), not creative.
- **Cause vs symptom:** fix the cause (e.g. budget rollback) and the symptom (CR↓) resolves itself.
- **Corroborate with ≥2 signals** before any kill/scale recommendation; a single signal = "watch".
- **What the data can't see — don't assert.** Pixel health, LP changes, competitor promos → MANUAL items, not invented theses.

## Gotchas (battle-tested)

- **HyperFormula SUMIF + `|`** — a criterion containing a pipe never matches → replace `|`→`?` (wildcard) in criteria.
- **Meta API dates** arrive as "May 1, 2026" (sometimes truncated) → normalize to ISO.
- **IFERROR** on derived metrics in breakdown TOTALs (denominators may be 0/absent).
- **Breakdowns ≠ windows** — account-default attribution, no mid-funnel; label that explicitly.
- **Frequency** — take account-level, never sum daily ad-level rows.
- **Empty 🖐 panel?** — CHECK has no `mtg='MANUAL'` rows; inject items 40–45.
- **Step-scan noisy on small accounts** — min-spend threshold (100/day) is one constant in `totalDiag()`; adjust to the account's scale.
- **Single-window data goes under the `'7dc1dv'` key** (it's Meta's default window); the other two buttons auto-disable.
- **Never call write endpoints** of any Meta Ads MCP from this skill. Read-only, always.

## Quality gates

- [ ] Preflight asked (model / data access / manual data) and answers noted
- [ ] Currency confirmed at the source (anti-contamination)
- [ ] Reconciliation: raw == TOTAL == TM+LM == rollups
- [ ] If windows pulled: 1dc ≤ 7dc ≤ 7dc1dv; if not: "—" columns + disabled buttons render correctly
- [ ] Sheet: 0 `#` errors; TOTAL = formulas; fx bar works
- [ ] TOTAL: 🔍/🪜/🖐 panels render; 🖐 deep-links jump to checklist items
- [ ] Checklist: 45 items; MANUAL rows carry "where to get it" paths; user knows what's missing for 100%
- [ ] No "kill creative" recommendation without fatigue refutation (#35) and corroboration (#38)
- [ ] 0 console errors; UI localized to the team's language; provenance table filled

## Credits & license

Built by **Radosław Kmita** (AI/strategy) with **Hubert** (Paid Social rules, sheet structure) at MTA Digital. Diagnostic pattern inspired by the SCALE AI "Meta Ads Diagnostic Playbook" (anti-anchoring: blind investigators → refutation → cause vs symptom → needs-manual-check). MIT — use it, fork it, ship it to your clients. If it saved you an afternoon, a comment or feedback on the LinkedIn post is the price. 🙂
