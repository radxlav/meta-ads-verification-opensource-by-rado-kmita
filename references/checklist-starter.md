# CHECK — schema + starter (universal Paid Social rules)

`const CHECK=[ [mtg, action, owner, status, evidence, howToCheck, link], ... ]`
- **status** ∈ `ok | warn | todo | no` (rendered as ✅/⚠️/◷/⛔)
- **evidence** = a concrete NUMBER from the data (e.g. "ROAS 11.87; 13/17 ad sets <25/wk")
- **link** = URL into Ads Manager (account section) or ''
- **CMAP[idx]** = `{s:'t'|'r'|..., r:rowIdx, c:colIdx, note:'…'}` → "↗ cell" deep-link to the evidence in the Sheet + a comment

## Universal items (always check, fill with a number from the pull)
1. MoM / WoW / day-to-day split — you have it in TOTAL + TM/LM
2. Reach + Impressions — sums from ad-level
3. Frequency (>4 anomaly = saturation) — **account-level** (never a daily sum)
4. CTR (drop → check Events Manager) — outbound/impressions
5. CPM (cost spike)
6. Spend / budget pacing
7. Link clicks vs Outbound clicks (Audience Network junk clicks)
8. Full funnel LPV→ContentView→ATC→Checkout→Purchase — is it tracked
9. ROAS + AOV + purchase value
10. Conversion rates (purchases vs Checkout/ATC/CV/LPV)
11. Placement breakdown — is Audience Network eating budget? (Placement tab)
12. Events Manager / pixel + CAPI health
13. Age cohorts + placements (Age/Placement tabs)
14. Click-to-purchase per creative
15. Conversion event = macro (Purchase), not micro
16. Event volume ≥50/wk/ad set (min 25) — the 50/25 rule
17. Dynamic conversion values
18. Pixel + CAPI + dedup + EMQ ≥6.0
19. Naming convention consistent/parsable [R:][C:][A:][B:]
20. Consolidation (campaign ≥50 conv/wk)
21. ASC / Advantage+ tested
22. Audiences: TOF ≥200K / rtrg ≥1000 / exclusions
23. Creatives: ≥4 variants / ad set
24. Frequency ≤4 (fatigue)
25. Budget: balanced split (not 90% in one)
26. Attribution: 7d click / 1d view window (+ compare 1dc/7dc/7dc1dv if pulled)
27. Tracking quality (conversions dropping while clicks stable?)
28. ROAS decline over 2–4 wks = creative fatigue *candidate* (see #35 before concluding)
29. Event volume per ad set (50/25)
30. Consolidation: 5+ Learning Limited → merge
31. Placement CPA / Audience Network exclusion
32. Budget scaling ≤20% / 3 days
33. Retargeting audience ≥1000

## DIAGNOSTICS — anti-anchoring (items 34–39; computed from data, 🔍 panel in TOTAL)
> Goal: when CPA↑ / ROAS↓, do NOT grab the first theory ("kill the creative"). Every theory must survive a refutation attempt.

34. **Day-over-day step-scan** — did spend/CPM/CTR/click→ATC jump THE SAME day? ≥2 metrics at once = delivery/budget change, NOT creative (fatigue decays per creative, gradually). Auto: 🔍 panel in TOTAL.
35. **Fatigue refutation** — accept creative fatigue ONLY if frequency↑ AND CTR↓ over 2–4 weeks per creative. Flat frequency or stable/rising CTR → theory REJECTED, look at delivery/budget.
36. **Funnel break** — which CR dropped: CTR / click→ATC (traffic quality) vs ATC→Checkout / Checkout→Purchase (site, cart, payments, tracking). Auto: 🪜 panel in TOTAL.
37. **Cause vs symptom** — e.g. budget×2 → broader delivery → CPM↓ → cheaper/worse traffic → click→ATC↓. Fix the cause (budget rollback); the symptom resolves. Don't optimize the symptom.
38. **Corroboration ≥2 signals** — every kill-creative / budget-shift decision needs ≥2 independent signals (e.g. step-scan + change history; CTR trend + frequency).
39. **Budget scaling events** — days with spend jumps >20% d/d (rule #32); cross-reference with learning resets and the date performance broke.

## MANUAL-CHECK — data the API can't see (items 40–45; `mtg='MANUAL'`, 🖐 panel in TOTAL)
> Row schema: `['MANUAL', action, owner, 'todo', '— (awaiting material)', '<where to get it — exact path>', '<link>']`
> Materials (screenshot .png / export .csv) → `./raw/<YYYY-MM>/manual/`. On receipt the agent updates status + evidence → 100% checklist.

40. **EMQ / pixel + CAPI health** — Events Manager → Data sources → select pixel → "Event Match Quality" (target ≥6.0 for Purchase) + browser/server dedup. Screenshot. Link: `https://business.facebook.com/events_manager2/list/dataset/`
41. **Budget/bid change history** — Ads Manager → clock icon "Change history" (top right) → range = dashboard period → filter Budget/Bid. Screenshot or export. Cross-reference dates with the 🔍 panel.
42. **Learning phase** — Ads Manager → ad set list → "Delivery" column (Learning / Learning limited). Screenshot. 5+ Learning Limited → consolidate (#30).
43. **Landing page changes / releases** — GTM → Versions (publish dates) + site changelog from dev/client. Cross-reference release dates with site-side CR drops (🪜 panel).
44. **Competitor promos** — Meta Ads Library (`facebook.com/ads/library`) → competitor page → country → active ads in the drop window. Screenshots with dates.
45. **Consent / cookie banner** — CMP panel (Cookiebot/OneTrust/other) → change history + GTM Versions. A consent change ≈ a drop in MEASURED conversions without a real sales drop (compare with the shop backend).

## Per project: ADD items from your team's meetings
Pull action items from your meeting notes/transcripts and append as `[mtg, action, owner, status, evidence, ...]` rows. Set the status only after verifying with a number from the pull.

## FLAGMAP (rollup flag → checklist item) + auditSignals
- `'<25/wk'` → #16 (idx 15), `'<4 creatives'` → #23 (idx 22)
- auditSignals(r): purwk<25→#16, nads<4→#23, spshare>0.40→#25(idx24), roas<3→#28(idx27)
- **Note:** the `roas<3` signal (#28 "fatigue") is NOT proof of fatigue — run #35 (refutation: frequency↑ + CTR↓ 2–4 wks) before concluding. MANUAL rows must be present in CHECK or the 🖐 panel in TOTAL stays empty.
