# STEMHUB AMC Project State

- Updated: 2026-07-16 (America/Vancouver)
- Repository: `D:\STEMHUB_AMC`
- Branch: `main`
- Audit commit before remediation: `fb80b504` (`Audit 2021 Fall AMC 12 data integrity`)
- Published site: <https://yiyangd.github.io/STEMHUB_AMC/>

## Current baseline

- AMC10 source rows: 1,150
- AMC12 source rows: 1,200
- Total source rows: 2,350
- Generated detail-page manifest entries: 2,086
- Missing/triage rows: 264
- Bilingual Chinese/English interface remains enabled for shared UI.

The historical root-level manifest, progress, report, and resume files remain useful evidence. This document is the current high-level state entry point.

## 2021 Fall remediation status

**The 2021 Fall AMC 12 base data and overview are repaired. Teaching pages have intentionally not yet been regenerated.**

- The mislabeled combined Fall PDF was quarantined because it is byte-for-byte identical to Spring.
- Independent Fall A and Fall B source booklets are now used and guarded by SHA-256, title, date, and page-count checks.
- All 50 Fall rows were rebuilt: 25 AMC 12A and 25 AMC 12B.
- All 50 rows contain complete A-E choices and a unique major/minor category.
- All 50 answer letters match the verified Fall Answer Keys.
- Normalized Fall/Spring statement duplicates: 0.
- Explicit diagram rows are A6, A14, A21, B2, and B15.
- All 31 stale Fall detail pages and manifest entries were removed.
- All 50 corrected Fall rows re-entered triage: 29 `ready_to_generate`, 5 `needs_diagram`, and 16 `solution_high_risk`.

Evidence:

- [`docs/audits/2021_fall_data_audit.md`](audits/2021_fall_data_audit.md)
- [`docs/audits/2021_fall_data_audit.csv`](audits/2021_fall_data_audit.csv)
- [`docs/audits/2021_fall_source_manifest.json`](audits/2021_fall_source_manifest.json)
- [`docs/audits/2021_fall_sync_result.json`](audits/2021_fall_sync_result.json)
- [`docs/audits/2021_fall_repair_validation.md`](audits/2021_fall_repair_validation.md)

## Immediate next entry point

Regenerate 2021 Fall teaching pages from the corrected CSV only:

1. Start with 5-10 `ready_to_generate` rows from `missing_problem_triage.csv`.
2. Verify each statement and answer against the corrected source and AoPS Answer Key.
3. Write original English teaching solutions with 4-6 explanatory steps.
4. Keep diagram and high-risk rows in their review queues until separately approved.
5. Validate MathJax, bilingual assets, detail links, manifest, and GitHub Pages after each batch.

## Scope guard

- Do not restore any deleted 2021 Fall page from Git history.
- Do not use `D:\AMC12_Codex\input\quarantine\2021AMC_FALL_is_Spring.pdf`.
- Do not treat historical Fall batch scripts or progress text as authoritative content.
- Keep 2021 Spring unchanged unless a separate audit finds an independent defect.
- Generate future Fall pages only from `D:\STEMHUB_AMC\amc12\all_problems.csv` after the repair commit.

## Repository-document note

`AGENTS.md` and `docs/DEFINITION_OF_DONE.md` were requested as prerequisites but remain absent from the local checkout. The audit and repair therefore use this state document and the dedicated validation report as the release criteria.
