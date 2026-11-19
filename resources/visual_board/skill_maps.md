<!--
SPDX-License-Identifier: Apache-2.0
-->

# What each skill puts on the board

Read [PROTOCOL.md](PROTOCOL.md) first. Each part below says what one skill shows
on the board and which of its gates move there. Stage ids are the `stages[].id`
values to use on the rail.

## egm-brainstorm

Rail: `brainstorm` (Clarify, Goldfish review, Brief), then `draft` and `review`
as `todo`.

* **Step 1 (clarify):** a section "Open questions" with a `questions` block
  (open text, no canned answers), plus a section "Working hypothesis" with a
  `diagram` or `flow` of the idea as you understand it and a `scope` block.
  Ask the same questions in chat too, briefly, so the user can answer either
  way.
* **Readiness gate:** `R<n>-G-ready` with options `review` (Review with
  Goldfishes) and `clarify` (Keep clarifying).
* **After the Goldfish review:** sections Overview (`diagram`), Goals vs
  Non-goals (`scope`), Alternatives Weighed (`compare`, rejected columns
  marked), Key decisions (`points`), Risks (`risks`). Each Goldfish objection
  becomes a finding card (lens = the brainstorm lens). The 2–3 key objections
  the skill highlights go in `headline` and the top cards.
* **Handoff gate:** `R<n>-G-handoff` with `publish`, `draft`, `refine`,
  `stop`.

## egm-draft

Rail: `brainstorm` (done or skipped), `draft`, then `review` stages as `todo`.
Add one rail stage per draft section if that helps: `d-overview`, `d-design`,
`d-alternatives`, `d-plan`.

* **Each section approval:** add or update one board section for the drafted
  part with `approvable: true` and `status: "draft"`, and set the gate
  `R<n>-G-draft-<section>` with `approve` and `revise`. Pick the visual from
  the content:
  * Overview & Goals: `scope` + a `diagram` of who uses what;
  * Design: architecture `diagram` (subgraphs), `sequenceDiagram` for the main
    path, `stateDiagram-v2` for lifecycles;
  * Alternatives: `compare` with the chosen option as `pick`;
  * Detailed Implementation: `flow` of the work steps, `files`, `stats`
    (files touched, steps, tests).
* Approved sections keep `status: "approved"` and lose `approvable`. A section
  approve on the card and the gate choice mean the same thing; take either.
* **Option decisions** (where the skill asks the user to choose between design
  options): a `compare` section plus a gate whose options are the candidates.

## egm-review

Rail: `s5` Zoom out, `s6` Comprehension, `s7` Critic, `s8` Zoom out 2, `s9`
Readiness. Mark stages a preset skips as `skipped`.

* **Preset gate:** `R1-G-preset` with `interactive`, `consolidated`,
  `feature`, `implementation`.
* **Each stage:** its report's findings become cards (`lens` = reviewer). Add a
  `stats` block of reviewer status (completed / not run) and a severity count.
* **Stage 6 (Comprehension):** show the reader's paraphrase as a
  `beforeAfter`: "What the doc means" vs "What a fresh reader understood", each
  a `points` block. Gaps become findings.
* **Stage gates** (`R<n>-G-s5` … `R<n>-G-s9`): keep the skill's options:
  `proceed`, `resolve` (Stages 7 and 9), `manual`, `pause`. On `resolve`, run
  `egm-resolve` with the board decisions already given: do not ask again for
  items the user decided.
* **Uninterrupted preset:** publish once at the end with all stages `done`, one
  section per stage, and the consolidated findings.

## egm-review-loop

Rail: one stage per reviewer group run. Findings cards per reviewer. The
aggregated resolution hand-off gate goes on the board with the options the skill
lists (auto accept, continue, interactive). On "interactive", the cards are the
walkthrough.

## egm-resolve

* Each finding card carries the AI suggestion (`suggestion`) and the proposed
  edit in `fix` (25 words max; the full edit stays in
  `goldfish_review_report.md`). `ESCALATE` cards come first in the list.
* For a fix that changes structure, add a `beforeAfter` visual on the card.
* **Resolution gate:** `R<n>-G-resolve` with `apply` (apply my decisions; undecided
  fixes follow the suggestion), `continue` (no changes), `chat` (walk me
  through it in chat).
* After applying, mark cards' sections `changed` and log counts in `history`.

## egm-lite

Rail: the lite phases you run (for example `l-plan`, `l-check`, `l-review`).
Show the checklist as a `flow` with each item's `state`, the BLUF as
`headline`, and the completion gate on the board. When the user would type
`review` or `goldfish`, offer those as gate options.

## egm-drift-report

One `compare` section per document: rows are the document's claims, columns
`Doc says`, `Code does`, `Match` (`yes` / `no` / `partial`). Divergences become
findings with `where` = file path. Gate: `update-doc`, `update-code`,
`decide-later`.

## egm-bootstrap

A `diagram` of the directory tree being documented (top two levels), `stats`
of folders done / to do, and the skill's gates on the board.
