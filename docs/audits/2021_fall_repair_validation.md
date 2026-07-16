# 2021 Fall AMC 12 Repair Validation

- Validated: 2026-07-16T12:51:29-07:00
- Result: PASS
- AMC12 rows: 1,200
- Combined AMC10/AMC12 rows: 2,350
- 2021 Fall rows: 50 (A: 25, B: 25)
- Normalized Spring/Fall statement duplicates: 0
- Verified answer letters: 50/50
- Rows with complete A-E choice markers: 50/50
- Explicit diagram rows: A6, A14, A21, B2, B15
- Stale Fall detail pages remaining: 0
- Stale Fall manifest entries remaining: 0
- Current problem-page manifest entries: 2,086
- Current missing/triage rows: 264
- Repaired Fall triage: ready_to_generate=29, needs_diagram=5, solution_high_risk=16

## Source provenance

- AMC 12A: MAA American Mathematics Competitions 73rd Annual AMC 12 A FALL; 2021-11-10; 9 pages; SHA-256 `ABC5E98F5638C3CC66E61F58715CE71381A38AD6B67E3D5C9B4FEC86543252CC`; https://cda.sof.ws/ep/AMC/2021_AMC12A_Fall.pdf
- AMC 12B: 2021 AMC 12B (Fall Contest) Problems; 2021-11-16; 9 pages; SHA-256 `DCCE4DBF6DD331971564464B70FAA451E40BFA7A4DD2EB70C55790E291BA82CD`; https://fangmath.xyz/files/AMC%2012/2021-amc-12b-fall-contest-problems.pdf

## Release checks

- Published annual CSV equals the Fall slice of `amc12/all_problems.csv`.
- Published AMC12 aggregate equals the validated upstream aggregate.
- The overview embeds all 1,200 rows and the corrected 50-row Fall slice.
- The overview bilingual asset block remains present exactly once.
- The detail-link map contains no invalidated Fall link.
- No CSV schema contains a difficulty field.
- All 19 originally missing Fall rows are present in the new triage, along with the 31 invalidated rows.

## Local browser verification

- Served the published site over local HTTP and opened `/amc12/?lang=en`.
- Selecting `2021 Fall` showed 50 problems, one year label, 25 Form A problems, and 25 Form B problems.
- The first visible card was the corrected Fall A1 statement beginning with `((2112-2021)^2)/169`.
- Selecting Form A reduced the current result to 25 problems; clearing the filters restored 1,200 problems across 24 year labels.
- The filtered Fall card set contained zero links to the 31 invalidated detail-page paths.
- English navigation and filter labels remained active through the data refresh.

Teaching solutions were intentionally not regenerated in this repair round.
