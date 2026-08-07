# NIRIKSHAN — single-page fraud-check tool

Goal: one screen, three view-states (idle → loading → results), styled to look dense and deliberate — bordered panels, strong navy hierarchy, orange used only as a signal. No sidebar, no invented nav, no dead space.

## Fixing "bland + too much whitespace"

- Every panel gets a visible 1px blue-grey border, a tinted section header strip, and tight internal padding — structure comes from borders, not empty gaps.
- Two-column desktop grid (input / verdict on the left, status and metrics on the right) so the page fills its width instead of a narrow centered column floating in space.
- A subtle navy hairline texture on the page background plus a thin orange rule under the header — quiet institutional character, no decorative animation.
- Content-height page: sections stack directly against each other with small gaps; no full-viewport stretching, no half-empty screen.
- Type does the work: IBM Plex Sans, uppercase micro-labels with letter-spacing, tabular numerals, an oversized trust score as the visual anchor.

## Layout

Header: NIRIKSHAN wordmark, dark-mode toggle, EN/HI toggle (both icon buttons with aria-labels). Nothing else — no sidebar, no persona framing, no fake nav items.

Idle: mode tabs (Text / Audio / Video, active tab marked by an orange underline) → auto-resizing textarea or file dropzone → 3 example chips → Analyze button (orange, disabled until input exists).

Loading: input panel dims and locks; a status panel cycles 3 plain-language strings every ~700ms; inline spinner in the button.

Results (identical structure for every band, only content and color differ):
1. Verdict banner — color + icon + text label together.
2. Trust score gauge, analysis breakdown bars (Phishing Language Risk, Authenticity Match) and the Claims SEBI Origin Yes/No badge, grouped as one bordered block.
3. Matched Official Circulars table — always present; when empty it renders "No matching circular found" in the same slot. Below ~600px it becomes stacked cards.
4. Recommended next steps, varying by band.
5. Helpline notice — only on High Risk.
6. Check Another resets to idle with cleared input.

## Data model (exact, nothing invented)

`text_risk`, `auth_trust`, `claims_sebi_origin`, `trust_score`, `band`, `matches[{title, date, distance, source_url}]`. No "Syntax Match", "Source Verity", "Domain Trust" or "Urgency Level" anywhere.

## Behavior

- Empty submit → inline validation message, never a browser alert.
- Wrong format or file over 25 MB → inline error naming the actual constraint.
- Backend unreachable → labeled demo-mode result with a note that live analysis needs the local backend (deliberate, preserved from the HTML version).
- Enter in the textarea analyzes; Shift + Enter is a newline.
- Example chip fills the textarea, pauses ~350ms, then auto-analyzes.

## Technical notes

- Tailwind v4 tokens in `src/styles.css`; light and dark as two complete themes (navy #122850 / #2C4570, backgrounds #F7F9FC / #0B1220, accent #F7941D in both). Orange restricted to the primary button, the active tab underline and focus rings.
- Reusable components under `src/components/nirikshan/`: Header, ModeTabs, InputPanel, ExampleChip, AnalyzeButton, LoadingStatus, VerdictBanner, ScoreGauge, RiskBar, MatchTable, GuidanceBlock, HelplineNotice, EmptyState, InlineError.
- All state in memory in `src/routes/index.tsx` — no routing, no storage, no auth, no backend added.
- Motion limited to 150–200ms hover transitions and a single 250ms fade/slide-up on results reveal.
- WCAG AA contrast checked in dark mode; risk bands always combine color + icon + text.

Already in place from the current session: the design tokens and the data/copy module. The plan continues from there.