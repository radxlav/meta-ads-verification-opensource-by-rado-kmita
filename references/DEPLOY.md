# DEPLOY — ship the dashboard for any client / any team

Works for **any Meta ad account, any period, any market, any agency** (brand tokens). TM/LM months and all month labels **derive from the data** — nothing to configure. You change 5 placeholders + inject data.

## Steps

0. **Preflight with the user** (SKILL.md Step 0) — model, data access (Meta MCP required; per-window tool optional), manual data. Don't build blind.

1. **Copy the skeleton** into the client project:
   `cp references/dashboard-skeleton.html <project>/dashboards/meta-ads/simple-dash.html`

2. **Pull data** (SKILL.md Workflow):
   - **Required (Meta Ads MCP only):** ad-level × day for the period, full funnel fields → write a CSV with exactly these 18 headers (order free, matched by name):
     `Date, Campaign name, AdSet name, Ad name, Year-Month, Year-Week (Starting on Monday), Total Cost, Reach, Impressions, Link clicks, Outbound clicks, Landing page views, Website content views, Website adds to cart, Website checkouts initiated, Website purchases, Website purchases conversion value, Website adds of payment info`
     File name: `meta-adlevel-7dc1dv.csv` (single window = account default; on most accounts that IS 7d click + 1d view). `Year-Month`/`Year-Week` may be left blank — derived from `Date`.
   - **Optional (per-window tool):** `meta-adlevel-1dc.csv`, `meta-adlevel-7dc.csv`, `meta-3windows-7dc1dv.csv` → enables the attribution switcher. Missing windows = "—" columns + disabled buttons (by design).
   - **Optional (breakdowns):** `meta-breakdown-placement-daily.csv`, `meta-breakdown-age-daily.csv` (columns: `Date, <segment>, cost, impr, reach, clicks, pur, roas`) + account-level `frequency`. Skipped → those tabs show a friendly placeholder.
   - **Always verify the currency at the source first** (spend prefix from the account-level pull). Different client = different data; never copy numbers between clients.

3. **Encode:** `python3 references/build-data.py` (run from the raw-CSV directory) → `/tmp/DATA.json`, `/tmp/BRK.json`. CUR/PREV months auto-detected. If the year is truncated in source dates → fix the fallback in `iso()`.

4. **Inject** into the skeleton markers (5 blocks):
   - `const DATA=/*__INJECT_DATA__*/{}` → `const DATA=<DATA.json>;` (single window goes under the `'7dc1dv'` key)
   - `const BRK=/*__INJECT_BRK__*/{}` → `const BRK=<BRK.json>;` (or leave `{}` if breakdowns skipped)
   - `const BREAKDOWNS=/*…*/{...}` → `{freq:{frequency,reach,impr,cost},placement:[…],age:[…]}` from the account-level pull (or leave the default)
   - `const CHECK=/*__INJECT_CHECK__*/[]` → the checklist from `checklist-starter.md`: **33 rules + 34–39 diagnostics + 40–45 MANUAL** + items from your team's meetings. MANUAL rows use `mtg='MANUAL'`, status `todo`, and the "where to get it" path in the how-to field — the 🖐 panel in TOTAL reads them.
   - `const CMAP=/*__INJECT_CMAP__*/{}` → cell deep-links (`{checklistIdx:{s,r,c,note}}`) once you know the client's numbers. Notes must contain THIS client's numbers (anti-contamination).

5. **Swap 5 placeholders** (find-replace):
   | placeholder | value |
   |---|---|
   | `__AGENCY__` | your agency/team name |
   | `__CLIENT__` | client name |
   | `__META_ACCOUNT_ID__` | numeric account id (without `act_`) |
   | `__CURRENCY__` | account currency (PLN / EUR / USD / CZK…) |
   | `__PERIOD__` | header period label (e.g. "Jul–Aug 2026") |

   > Note: the file also contains `act___META_ACCOUNT_ID__` — that's `act_` + the placeholder (looks like 3 underscores). The find-replace above resolves it to `act_<id>` correctly; don't "fix" it manually.

6. **Currency ≠ PLN?** The formatting symbol is `' zł'` (functions `fZ`/`fmtMetric` + the 🔍 diagnostics panel). Replace `' zł'` → `' €'` / `' $'` / `' Kč'` (a few spots). Numbers stay in the account currency from the pull.

7. **Language:** the UI ships in Polish. For non-PL teams, translate the *visible* strings (tab labels, card titles, table headers, notes) in the OUTPUT file — never identifiers, code, or formulas.

8. **Brand:** swap the palette in `:root` (`--coral/--cream/--dark`) and the font to your agency tokens.

9. **Verify** (browser or Playwright): 0 console errors; reconciliation raw == TOTAL == TM+LM == rollups; 0 `#` errors in the Sheet; fx bar shows formulas; TM/LM = correct months (auto); ROAS/CPA overlay on stacked charts works; **TOTAL shows the 3 diagnostics panels (🔍 d/d step-scan, 🪜 funnel, 🖐 manual-check)**; clicking "↗ checklist #N" in 🖐 jumps to the item; in single-window mode the two missing window columns show "—" and their buttons are disabled.

10. **Close the manual checks** (SKILL.md final step): guide the user through items 40–45 — where to click in Events Manager / Ads Manager / GTM / Ads Library, what to grab (CSV/screenshot), where to drop it (`./raw/<YYYY-MM>/manual/`). Update CHECK statuses + evidence as materials arrive → 100% checklist.

## What needs NO changes (automatic / fixed)
- TM/LM months + every month label (`ymPL()` from data — RAW TM/LM, attribution block, TM vs LM).
- Diagnostics in TOTAL: `totalDiag()` — step-scan, funnel TM vs LM, manual-check panel — computed from `D.tm`/`D.lm`/`CHECK`.
- All code: charts (bars/trend/stacked + ROAS/CPA overlay), naming parser, SUMIF sheet + fx bar, checklist deep-links, explanation toggles, polish. It's in the skeleton — do NOT rewrite it.

## Porting to other channels
The pattern (18-col RAW → SUMIF TOTAL, windows, breakdowns, checklist + diagnostics, fx) ports to Google Ads / TikTok — change the pull and the funnel columns, keep the tab layout and the Sheet.
