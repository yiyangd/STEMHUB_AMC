# STEMHUB AMC Project State

- Updated: 2026-07-16 (America/Vancouver)
- Repository: `D:\STEMHUB_AMC`
- Branch: `main`
- Baseline commit before this audit: `813144af` (`Polish bilingual navigation and UI`)
- Published site: <https://yiyangd.github.io/STEMHUB_AMC/>

## Current baseline

- AMC10 source rows: 1,150
- AMC12 source rows: 1,200
- Total source rows: 2,350
- Generated detail-page manifest entries: 2,117
- Missing/triage rows: 233
- Bilingual Chinese/English interface is deployed for shared UI.

The historical root-level manifest, progress, report, and resume files remain useful evidence, but this document is the current high-level state entry point.

## Active release blocker

**2021 Fall AMC 12 data is invalid and must not be extended or regenerated from the current CSV.**

The independent audit found:

- `2021AMC_FALL.pdf` is byte-for-byte identical to `2021AMC_Spring.pdf`.
- All 50 Fall rows duplicate Spring content; only the year/source labels differ.
- 0 of 50 Fall statements match the actual Fall competition.
- 31 Fall detail pages exist and all 31 use the wrong statement/solution.
- 23 existing pages display an answer letter that conflicts with the Fall AoPS Answer Key.
- All 50 Fall CSV answer fields are blank.

Full evidence and the repair sequence are in:

- [`docs/audits/2021_fall_data_audit.md`](audits/2021_fall_data_audit.md)
- [`docs/audits/2021_fall_data_audit.csv`](audits/2021_fall_data_audit.csv)

## Immediate next entry point

Run a dedicated 2021 Fall repair task in this order:

1. Replace or split the invalid Fall source PDF using verified Fall A/B booklets.
2. Remove the pipeline exception that permits identical Spring/Fall PDF hashes.
3. Re-extract and reclassify all 50 Fall rows, then populate verified answers.
4. Regenerate upstream annual and aggregate products.
5. Replace published Fall data and invalidate all 31 stale detail pages/manifest entries.
6. Regenerate and validate Fall pages before deployment.

## Scope guard

Until the repair is complete:

- Do not generate additional 2021 Fall teaching pages from the current data.
- Do not treat `aops_verified: true` in existing Fall manifest entries as reliable.
- Do not edit stale Fall pages in place; remove/regenerate them from corrected source rows.
- Keep 2021 Spring unchanged unless a separate audit finds an independent defect.

## Repository-document note

`AGENTS.md` and `docs/DEFINITION_OF_DONE.md` were requested as prerequisites but were absent from both the local checkout and `origin/main` when this audit began. They were not created in this audit because the authorized write scope is limited to audit artifacts and this state document.
