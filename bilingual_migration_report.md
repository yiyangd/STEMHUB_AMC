# Bilingual Migration Report

- Mode: validation
- Detail pages inspected: 2117
- Detail pages updated: 0
- Pages with bilingual asset blocks: 2117
- Legacy taxonomy aliases recovered: 0
- Validation failures: 0

## Scope

- Added the shared bilingual CSS, dictionary, and language-switching script to each AMC10/AMC12 problem detail page.
- Preserved the existing problem statements, choices, answers, teaching solutions, MathJax markup, and AoPS links.
- The switcher defaults to Chinese, persists in localStorage, and accepts ?lang=zh or ?lang=en.

## Maintenance Note

The overview pages in this deployment repository are published HTML artifacts. The upstream AMC10/AMC12 overview builders are outside this repository, so rerunning those pipelines may replace the bilingual overview shell. Reapply the website migration or port the shared asset references and localization hooks into the upstream builders before publishing new overview files.
