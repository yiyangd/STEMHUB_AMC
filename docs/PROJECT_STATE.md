# STEMHUB AMC Project State

- Updated: 2026-07-17 (America/Vancouver)
- Repository: `D:\STEMHUB_AMC`
- Branch: `main`
- Audit commit before remediation: `fb80b504` (`Audit 2021 Fall AMC 12 data integrity`)
- Published site: <https://yiyangd.github.io/STEMHUB_AMC/>

## Current baseline

- AMC8 source rows: 250 across the ten real years 2015-2020 and 2022-2025
- AMC10 source rows: 1,150
- AMC12 source rows: 1,200
- Total source rows: 2,600
- Generated detail pages: 250 for AMC8 plus 2,086 AMC10/12 manifest entries (2,336 total)
- Missing/triage rows: 0 for AMC8; 264 in the existing AMC10/12 queue
- Bilingual Chinese/English interface remains enabled for the shared home, AMC10, and AMC12 UI. AMC8 keeps its validated self-contained interface and does not inherit the A/B-only localization path.

AMC8 is a single-form contest. Its retained `form` data is empty, and the published pages contain no A/B controls or generated 2021 dataset.

The historical root-level manifest, progress, report, and resume files remain useful evidence. This document is the current high-level state entry point.

## AMC 8 site integration

The validated AMC8 release is mirrored from `D:\AMC8_Codex\output` through a strict public-file allowlist into `amc8/`. The published payload includes:

- the 10-year, 250-problem overview and annual pages;
- 250 problem detail pages with independently written step-by-step solutions;
- 76 local diagram assets required by those pages;
- the textbook, method, common-error, and prerequisite indexes;
- the 12-column public CSV and AMC8 taxonomy;
- an independent AMC8 site manifest and validation report.

Run these commands from the repository root before any future AMC8 release:

```powershell
python scripts\sync_amc8_site.py
python scripts\validate_amc8_site.py
```

Current release validation: **33/33 PASS**. The sync verifies all 363 allowlisted upstream files against the AMC8 source manifest before publishing. Two consecutive full syncs produced the same `amc8/site_manifest.json` SHA-256: `853E200720DCFAA0F4966282EBF82773C72A8B133D8C55BE499EC0F1B8EAD3AC`.

Evidence: [`docs/audits/amc8_site_validation.md`](audits/amc8_site_validation.md)

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

## AMC 10/12 immediate next entry point

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
