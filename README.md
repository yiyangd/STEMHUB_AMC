# STEMHUB AMC

Static AMC 8 / AMC 10 / AMC 12 problem-library site for GitHub Pages.

Published site: <https://yiyangd.github.io/STEMHUB_AMC/>

## Pages

- Home: `index.html`
- AMC 8: `amc8/index.html`
- AMC 10: `amc10/index.html`
- AMC 12: `amc12/index.html`

## Included data

- Interactive overview and per-year HTML pages
- Per-problem detail pages with step-by-step solutions where available
- `all_problems.csv` and `taxonomy.md` under each contest directory
- AMC 8 textbook and method indexes
- Public diagram assets required by problem pages
- Reproducible AMC 8 sync and site-validation scripts

## AMC 8 release source

Run `python scripts/sync_amc8_site.py` to copy the public, allowlisted release files from `D:\AMC8_Codex\output` into `amc8/`. Then run `python scripts/validate_amc8_site.py` before publishing.

AMC 8 contains the ten real contest years 2015-2020 and 2022-2025 (250 problems). There is no generated 2021 AMC 8 dataset. AMC 8 uses a single form; A/B controls remain specific to AMC 10 and AMC 12.

## Not included

Raw PDF files, extracted temporary text, cache folders, browser-test screenshots, internal audit artifacts, and local runtime files stay outside this repository.
