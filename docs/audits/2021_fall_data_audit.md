# 2021 Fall AMC 12 Data Integrity Audit

- Audit date: 2026-07-16 (America/Vancouver)
- Scope: 2021 Fall AMC 12A and AMC 12B, 50 problems total
- Mode: evidence collection and remediation design only
- Severity: release blocker
- Detailed row-level evidence: [`2021_fall_data_audit.csv`](2021_fall_data_audit.csv)

## Executive conclusion

The published 2021 Fall data is not a valid Fall data set. The file named `2021AMC_FALL.pdf` is byte-for-byte identical to `2021AMC_Spring.pdf`, and its extracted text is also byte-for-byte identical to the Spring extraction. The 50 Fall CSV rows copy the corresponding Spring rows in every content field; only `year` and `source` were relabeled.

As a result:

- 0 of 50 local Fall statements match the actual Fall test.
- 50 of 50 local Fall statements are duplicated from Spring.
- 31 Fall detail pages exist, and all 31 use the wrong problem statement.
- 23 of those 31 pages display an answer letter that conflicts with the Fall AoPS Answer Key.
- 8 pages happen to display the same answer letter as the Fall key, but the statement and solution are still for a Spring problem, so none of those pages is correct.
- All 50 Fall CSV `answer` fields are blank.
- All 50 problems must be re-sourced, re-extracted, reclassified, and reviewed before Fall can be considered publishable.

## Governing-document note

The requested files `AGENTS.md`, `docs/PROJECT_STATE.md`, and `docs/DEFINITION_OF_DONE.md` were not present in the local checkout or `origin/main` at the start of this audit. Therefore no repository-specific rules could be read from them. This audit creates `docs/PROJECT_STATE.md` only because the task explicitly requires updating that file; it does not invent `AGENTS.md` or `DEFINITION_OF_DONE.md`.

## Evidence sources

### Local and upstream files

- `D:\AMC12_Codex\input\2021AMC_Spring.pdf`
- `D:\AMC12_Codex\input\2021AMC_FALL.pdf`
- `D:\AMC12_Codex\output\tmp\extracted_text\2021_spring\2021AMC_Spring_text.txt`
- `D:\AMC12_Codex\output\tmp\extracted_text\2021_fall\2021AMC_FALL_text.txt`
- `D:\AMC12_Codex\output\2021_spring\2021_spring_problems.csv`
- `D:\AMC12_Codex\output\2021_fall\2021_fall_problems.csv`
- `D:\AMC12_Codex\output\all_problems.csv`
- `D:\STEMHUB_AMC\amc12\all_problems.csv`
- `D:\STEMHUB_AMC\amc12\years\2021_spring\2021_spring_problems.csv`
- `D:\STEMHUB_AMC\amc12\years\2021_fall\2021_fall_problems.csv`
- `D:\STEMHUB_AMC\problem_pages_manifest.json`
- Existing detail pages under `D:\STEMHUB_AMC\amc12\problems\2021-fall-*`

### Independent Fall references

- [MAA Fall 2021 AMC 12A problem booklet](https://cda.sof.ws/ep/AMC/2021_AMC12A_Fall.pdf)
- [Fall 2021 AMC 12B problem booklet](https://fangmath.xyz/files/AMC%2012/2021-amc-12b-fall-contest-problems.pdf)
- [Independent Fall 2021 AMC 12B problem/solution compilation](https://shsmathteam.com/wp-content/uploads/2021/11/fall_2021_amc_12_b_solutions.pdf)
- [AoPS Fall 2021 AMC 12A problems](https://artofproblemsolving.com/wiki/index.php/2021_Fall_AMC_12A_Problems)
- [AoPS Fall 2021 AMC 12A Answer Key](https://artofproblemsolving.com/wiki/index.php/2021_Fall_AMC_12A_Answer_Key)
- [AoPS Fall 2021 AMC 12B problems](https://artofproblemsolving.com/wiki/index.php/2021_Fall_AMC_12B_Problems)
- [AoPS Fall 2021 AMC 12B Answer Key](https://artofproblemsolving.com/wiki/index.php/2021_Fall_AMC_12B_Answer_Key)

At audit time, the AoPS community endpoint labeled as the Fall PDF (`https://artofproblemsolving.com/community/contest/download/c3415_amc_12/2021`) returned the 10-page Spring community packet. This likely explains how the mislabeled local input was acquired. It also means the repair must not reuse that endpoint without validating the downloaded title, date, and hash.

## Audit method

1. Compared SHA-256 hashes and page-rendered first pages of the two local source PDFs.
2. Compared SHA-256 hashes of the two extracted-text files.
3. Compared all 50 Spring/Fall annual CSV rows field by field.
4. Confirmed the same Fall rows propagate into upstream and published `all_problems.csv` files.
5. Parsed all 25 problems from independent Fall A and Fall B booklets and compared normalized statement fingerprints problem by problem.
6. Verified the 50 canonical answer letters against the AoPS Fall Answer Keys.
7. Audited all Fall manifest entries and every existing Fall detail page for identity, statement, answer, link, and page existence.

The `local_sha` and `canonical_fall_sha` values in the CSV are the first 12 hexadecimal characters of SHA-256 after lowercasing and removing non-alphanumeric characters. They are comparison fingerprints, not source-file hashes.

## Root-cause evidence

| Check | Result |
| --- | --- |
| Spring PDF SHA-256 | `E4F215D277EE20EB7B3A5C7208D2AF4E83529956CBCD4A4CAE8E479F562ED38C` |
| File labeled Fall PDF SHA-256 | `E4F215D277EE20EB7B3A5C7208D2AF4E83529956CBCD4A4CAE8E479F562ED38C` |
| Spring extracted-text SHA-256 | `3AE5EA591E164241C42ECD91DF84A2B1B0750113FF5BA561E5424D9BF344FE68` |
| Fall extracted-text SHA-256 | `3AE5EA591E164241C42ECD91DF84A2B1B0750113FF5BA561E5424D9BF344FE68` |
| Visual title of both local PDFs | `2021 AMC 12/AHSME Spring`, February 2021 |
| Correct Fall A booklet title | `AMC 12 A FALL`, November 10, 2021 |
| Correct Fall B booklet title | `2021 AMC 12B (Fall Contest) Problems` |
| Fall rows equal Spring content rows | 50 of 50 |
| Fields that differ between paired annual rows | `year`, `source` only |
| Upstream/published annual CSV hashes | Corresponding upstream and published files match exactly |

The pipeline also contains a dangerous exception in `D:\AMC12_Codex\scripts\build_all_years_summary.py`: duplicate-PDF detection explicitly ignores the pair `{2021AMC_FALL.pdf, 2021AMC_Spring.pdf}`. That exception allowed the duplicate source to be treated as acceptable and must be removed during remediation.

## Exact statistics

| Metric | Count | Interpretation |
| --- | ---: | --- |
| Correct Fall statement rows | 0 / 50 | No local Fall statement belongs to the actual Fall test |
| Spring/Fall duplicated statement rows | 50 / 50 | Every Fall content row copies its Spring counterpart |
| Correct identity fields | 50 / 50 | `year`, `source`, `form`, and `problem_no` labels are structurally correct |
| Local rows with five visible choice markers | 49 / 50 | B17 lacks A-E markers in the local text; all choices are for the wrong Spring test anyway |
| CSV answers present | 0 / 50 | All Fall CSV answers are blank |
| Existing detail pages | 31 / 50 | 17 A pages and 14 B pages |
| Correct existing detail pages | 0 / 31 | Every existing page uses a Spring statement/solution |
| Existing pages with wrong Fall answer letter | 23 / 31 | Displayed letter conflicts with AoPS Fall Answer Key |
| Existing pages with coincidentally matching letter | 8 / 31 | Letter matches, but statement/solution is still wrong |
| Missing detail pages | 19 / 50 | No page exists yet |
| Problems requiring re-extraction/review | 50 / 50 | Entire Fall set must be rebuilt |

For the requested “wrong answer” statistic, the actionable published count is **23 wrong detail-page answers**. The source CSV contains **0 explicit wrong values because all 50 values are missing**, not because they are verified.

## Detail-page findings

### Existing but incorrect pages

- A: Problems 1-9, 11-16, 22-23 (17 pages)
- B: Problems 1-10, 12, 16, 20, 23 (14 pages)

All 31 manifest entries have the right Fall slug/source identity and an AoPS Fall URL, but the page body is derived from Spring data. All 31 entries set `aops_verified: true`; that flag is therefore unreliable for these rows. Thirty of the 31 also set `needs_review: false`.

### Wrong displayed answer letters

- A: 1, 2, 3, 4, 5, 6, 8, 9, 11, 12, 13, 16, 23
- B: 1, 3, 4, 5, 6, 7, 8, 9, 12, 16

### Coincidentally matching answer letters, but still incorrect pages

- A: 7, 14, 15, 22
- B: 2, 10, 20, 23

### Missing pages

- A: 10, 17, 18, 19, 20, 21, 24, 25
- B: 11, 13, 14, 15, 17, 18, 19, 21, 22, 24, 25

### Choice completeness

Local B17 has no A-E choice markers because the copied Spring statement depends on a diagram and its choices were lost during extraction. The other 49 local rows contain five choice markers, but those choices belong to Spring and must not be retained.

## Repair order

1. **Freeze Fall publication.** Do not generate more 2021 Fall pages from the current CSV.
2. **Replace the source.** Replace `D:\AMC12_Codex\input\2021AMC_FALL.pdf` with a verified Fall A/B source, or update the extractor to accept separately verified A and B source files. Record source URL, title/date, page count, and SHA-256.
3. **Remove the duplicate exception.** Make identical Spring/Fall hashes a hard validation failure in `build_all_years_summary.py` and add the same guard before extraction/build.
4. **Re-extract 50 statements.** Confirm 25 A and 25 B rows, all five choices, and zero normalized statement equality with Spring.
5. **Reclassify every row.** Recompute major/minor category, tags, key idea, notes, and diagram flags from the actual Fall statements. Canonical figure-dependent problems needing explicit diagram review include at least A6, A14, A21, B2, and B15.
6. **Populate and verify answers.** Use the AoPS Fall Answer Keys for all 50 rows; retain answer-letter and answer-value evidence separately.
7. **Regenerate upstream products.** Rebuild the Fall annual CSV/Markdown/HTML and every aggregate/report through the normal pipeline.
8. **Sync the published data.** Replace the published Fall annual files, `amc12/all_problems.csv`, and `amc12/index.html`; then update copied taxonomy/manifest/progress/validation artifacts.
9. **Invalidate stale pages.** Remove all 31 current Fall manifest records and detail pages before regeneration so stale Spring solutions cannot survive. Regenerate only from corrected rows, then triage/generate the remaining 19 pages.
10. **Run release gates.** Verify hashes, 50 unique Fall rows, answer keys, classifications, card links, MathJax, bilingual UI, manifest consistency, missing triage, and GitHub Pages deployment.

## Affected files

### Upstream source and pipeline

- `D:\AMC12_Codex\input\2021AMC_FALL.pdf`
- `D:\AMC12_Codex\output\tmp\extracted_text\2021_fall\2021AMC_FALL_text.txt`
- `D:\AMC12_Codex\scripts\extract_input_pdfs.py`
- `D:\AMC12_Codex\scripts\build_years_from_extracted_text.py`
- `D:\AMC12_Codex\scripts\build_all_years_summary.py`
- `D:\AMC12_Codex\scripts\validate_outputs.py`
- `D:\AMC12_Codex\scripts\run_pipeline.py`

### Upstream generated products

- `D:\AMC12_Codex\output\2021_fall\2021_fall_problems.csv`
- `D:\AMC12_Codex\output\2021_fall\2021_fall_classified.md`
- `D:\AMC12_Codex\output\2021_fall\2021_fall.html`
- `D:\AMC12_Codex\output\all_problems.csv`
- `D:\AMC12_Codex\output\all_years_index.html`
- `D:\AMC12_Codex\output\taxonomy.md`
- `D:\AMC12_Codex\output\progress_report.md`
- `D:\AMC12_Codex\output\resume_prompt.md`
- `D:\AMC12_Codex\output\manifest.json`
- `D:\AMC12_Codex\output\validation_report.md`

### Published STEMHUB files

- `D:\STEMHUB_AMC\amc12\years\2021_fall\2021_fall_problems.csv`
- `D:\STEMHUB_AMC\amc12\years\2021_fall\2021_fall_classified.md`
- `D:\STEMHUB_AMC\amc12\years\2021_fall\2021_fall.html`
- `D:\STEMHUB_AMC\amc12\all_problems.csv`
- `D:\STEMHUB_AMC\amc12\index.html`
- `D:\STEMHUB_AMC\amc12\taxonomy.md`
- `D:\STEMHUB_AMC\amc12\manifest.json`
- `D:\STEMHUB_AMC\amc12\progress_report.md`
- `D:\STEMHUB_AMC\amc12\resume_prompt.md`
- `D:\STEMHUB_AMC\amc12\validation_report.md`
- `D:\STEMHUB_AMC\problem_pages_manifest.json`
- `D:\STEMHUB_AMC\problem_pages_progress.md`
- `D:\STEMHUB_AMC\problem_pages_report.md`
- `D:\STEMHUB_AMC\resume_prompt.md`
- `D:\STEMHUB_AMC\missing_problem_triage.csv`
- `D:\STEMHUB_AMC\missing_problem_triage.md`
- The 31 current directories under `D:\STEMHUB_AMC\amc12\problems\2021-fall-*`

### Published generator follow-up

- `D:\STEMHUB_AMC\scripts\build_problem_pages.py`
- `D:\STEMHUB_AMC\scripts\batch_generate_problem_pages.py`
- `D:\STEMHUB_AMC\scripts\generate_high_risk_review_batch.py`
- `D:\STEMHUB_AMC\scripts\build_missing_problem_triage.py`

The one-off high-risk batch scripts and historical progress records must not be treated as authoritative Fall content. They preserve useful evidence of the bad run, including Spring-specific problem descriptions under Fall labels.

## Repair acceptance criteria

- The verified Fall source hash differs from the Spring source hash.
- Source title/date checks identify November 2021 Fall A and Fall B.
- Exactly 50 Fall rows exist: A1-A25 and B1-B25.
- No corrected Fall statement equals the corresponding Spring statement after normalization.
- All 50 Fall choices are complete or a diagram-dependent exception is explicitly documented.
- All 50 answer letters match the AoPS Fall Answer Keys.
- All 50 classifications are reviewed against the corrected statements.
- No old Fall detail page or manifest record survives unchanged.
- Every regenerated Fall page has the corrected statement, choices, answer, teaching solution, AoPS links, MathJax, and bilingual UI.
- Aggregate counts remain stable at 1,200 AMC12 rows and 2,350 total AMC10/AMC12 rows.
- Validation, local browser checks, Git status scope checks, push, and GitHub Pages checks pass.

## Audit boundary

This audit did not modify any source PDF, extracted text, CSV data, HTML page, manifest, generation script, or deployed site. Only the audit artifacts and `docs/PROJECT_STATE.md` are in scope for this commit.
