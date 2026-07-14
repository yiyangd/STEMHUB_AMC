# Bilingual Migration Report

- Mode: migration
- Detail pages inspected: 2117
- Detail pages updated: 0
- Pages with bilingual asset blocks: 2117
- Legacy taxonomy aliases recovered: 0
- Validation failures: 0

## Scope

- Added the shared bilingual CSS, dictionary, and language-switching script to each AMC10/AMC12 problem detail page.
- Preserved the existing problem statements, choices, answers, teaching solutions, MathJax markup, and AoPS links.
- The switcher defaults to Chinese, persists in localStorage, and accepts ?lang=zh or ?lang=en.

## QA and UX Polish (2026-07-14)

### Improvements

- Fixed the language switcher so its `aria-pressed` state remains correct after the navigation links are grouped for responsive layout.
- Internal homepage, overview, and detail-page links now retain `?lang=zh` or `?lang=en`, including overview cards rendered after a filter update; localStorage remains the fallback for direct links without a language query.
- Added an explicit overview-render refresh hook. Dynamic year, form, major/minor category, keyword, empty-state, comparison, Part 1/2/3, summary, card, and detail-link text now localize again after every filter redraw.
- Localized the overview document titles and homepage accessibility region labels.
- In English mode, Chinese-only Key Idea and Notes text is labeled as `Key idea (Chinese)` or `Notes (Chinese)` rather than being machine-translated.
- Added keyboard focus visibility and tighter small-screen navigation rules for the language buttons and navigation links.
- Added a version query to the shared resources used by the site shell so the current bilingual overview fixes are fetched promptly after deployment.

### Local Verification

- Homepage: English and Chinese modes showed the expected navigation labels, selected-language state, query-preserving links, and no desktop overflow.
- AMC 10 overview: verified English direct links, year filtering to 2024 (50 results), major-category drill-down, Form A filtering, keyword filtering, clear filters, A/B comparison, Part labels, and card links.
- AMC 12 overview: verified English direct links, filtering to 2024 (50 results), dynamic A/B counts, Part labels, category statistics, and card links.
- Detail pages: checked two AMC 10 and two AMC 12 samples in both languages. Navigation and section labels switched; MathJax produced rendered containers; no raw double-escaped display delimiters were visible; no desktop overflow was detected.
- 404 page: verified English heading, document title, language-preserving internal navigation, and no desktop overflow.
- Detail-page asset migration completed successfully for all 2,117 pages with exactly one shared CSS file and two shared scripts per page.
- Responsive CSS now has dedicated 980px and 480px navigation layouts. A browser connection interruption prevented a final live 375px/768px screenshot pass in this round, so that visual spot-check remains a small follow-up rather than a claimed runtime result.

### Intentional Non-Translation

- Original AMC problem statements, choices, English teaching solutions, answer values, source strings, URLs, and AoPS content remain unchanged.
- Chinese key ideas and notes are retained as source material and labeled in English mode when present; they are not automatically translated.

## Maintenance Note

The overview pages in this deployment repository are published HTML artifacts. The upstream AMC10/AMC12 overview builders are outside this repository, so rerunning those pipelines may replace the bilingual overview shell. Reapply the website migration or port the shared asset references and localization hooks into the upstream builders before publishing new overview files.
