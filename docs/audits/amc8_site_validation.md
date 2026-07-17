# AMC 8 Site Validation

- Result: **PASS**
- Checks passed: **33/33**
- Publication subtree: `amc8/`
- Validated source: `AMC8_Codex/output`

| # | Check | Result | Detail |
|---:|---|:---:|---|
| 1 | AMC 8 publication directory exists | PASS | amc8 |
| 2 | Aggregate CSV is readable | PASS | UTF-8 CSV parsed successfully |
| 3 | Aggregate CSV has the exact 12-column schema | PASS | ['year', 'contest', 'form', 'problem_no', 'source', 'statement', 'answer', 'major_category', 'minor_category', 'tags', 'key_idea', 'notes'] |
| 4 | Aggregate CSV contains exactly 250 rows | PASS | 250 |
| 5 | Years and problem numbers are exactly the real 10 × 1-25 set | PASS | years=['2015', '2016', '2017', '2018', '2019', '2020', '2022', '2023', '2024', '2025']; unique keys=250 |
| 6 | No 2021 data exists in the aggregate CSV | PASS | 2021 rows=0 |
| 7 | contest is AMC 8 and form is empty for every row | PASS | contest values=['AMC 8']; non-empty forms=0 |
| 8 | Source labels are exact and unique | PASS | unique source labels=250 |
| 9 | No difficulty field was introduced | PASS | ['year', 'contest', 'form', 'problem_no', 'source', 'statement', 'answer', 'major_category', 'minor_category', 'tags', 'key_idea', 'notes'] |
| 10 | Root files match the public allowlist | PASS | ['all_problems.csv', 'all_years_index.html', 'common_errors.md', 'index.html', 'method_index.md', 'prerequisite_map.md', 'site_manifest.json', 'taxonomy.md', 'textbook_index.html'] |
| 11 | Root directories match the public allowlist | PASS | ['2015', '2016', '2017', '2018', '2019', '2020', '2022', '2023', '2024', '2025', 'assets', 'problems'] |
| 12 | Ten annual directories contain only HTML/Markdown/CSV and exact 25-row slices | PASS | all 10 years match |
| 13 | Exactly 250 expected detail-page directories exist | PASS | slugs=250; detail pages=250; unexpected files=[] |
| 14 | Exactly 76 local PNG diagram images are published | PASS | images=76; extensions={'.png': 76} |
| 15 | amc8/index.html is an exact copy of all_years_index.html | PASS | identical publication entrypoints |
| 16 | Overview and annual pages embed the expected problem counts | PASS | overview=250 and every year=25 |
| 17 | All 263 public HTML pages have STEMHUB/AMC10/AMC12 navigation | PASS | pages=263; missing nav=[] |
| 18 | All static local HTML links and resources resolve | PASS | no broken references |
| 19 | No external images or CSS image hotlinks exist | PASS | external img=[]; external CSS=[] |
| 20 | Every embedded image has non-empty alt text | PASS | all image alt text present |
| 21 | Every published diagram image is referenced by a page | PASS | referenced=76; published=76 |
| 22 | No detail page links to an unpublished local input PDF | PASS | residual pages=[] |
| 23 | AMC 8 HTML contains no A/B form or difficulty controls | PASS | pages=[] |
| 24 | All local Markdown links resolve | PASS | no broken Markdown links |
| 25 | Markdown contains no external image hotlinks | PASS | [] |
| 26 | No absolute local paths, file URLs, or localhost URLs leak into publication files | PASS | [] |
| 27 | No temporary, cache, backup, or internal audit artifacts are published | PASS | [] |
| 28 | site_manifest.json covers every managed file with current SHA-256 and counts | PASS | manifest current |
| 29 | Protected CSV/taxonomy/textbook Markdown is byte-identical to AMC8_Codex | PASS | 25 copied data/document files match |
| 30 | STEMHUB home exposes AMC 8 with current aggregate counts and honest form wording | PASS | home integration current |
| 31 | The site 404 page links to AMC 8 | PASS | AMC 8 fallback link present |
| 32 | Home-page Chinese/English dictionary covers the AMC 8 integration | PASS | AMC 8 keys present in both languages |
| 33 | All local links and assets on the STEMHUB home page resolve | PASS | home links resolve |

## Publication contract

The publication contains only the AMC 8 overview/textbook entry points, ten annual datasets/pages, 250 problem-detail pages, 76 locally hosted diagram PNGs, and the public taxonomy/method documents. Original PDFs, local audit artifacts, screenshots, temporary files, and local filesystem paths are intentionally excluded.
