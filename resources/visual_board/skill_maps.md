<!--
SPDX-License-Identifier: Apache-2.0
-->

# What each skill puts on the board

Read [PROTOCOL.md](PROTOCOL.md) first. Each part below says what the reader needs
to grasp at that point of the skill, and which gates move to the board. How to
draw it is yours to decide, following the principles in PROTOCOL.md section 4.
Stage ids are the `stages[].id` values for the rail.

## egm-brainstorm

Rail: `brainstorm`, then `draft` and `review` as `todo`.

* **Clarifying:** the reader should see the idea as you currently understand it
  and where your understanding has holes. The open questions go in a section's
  `questions`; ask them briefly in chat too, so the user can answer either way.
* **Readiness gate:** `R<n>-G-ready` with `review` (Review with Goldfishes) and
  `clarify` (Keep clarifying).
* **After the Goldfish review:** the reader should grasp the concept, what it
  leaves out, the alternatives it beat and why, and what could go wrong. Each
  Goldfish objection is a finding card; the 2–3 the skill highlights lead the
  `headline`.
* **Handoff gate:** `R<n>-G-handoff` with `publish`, `draft`, `refine`, `stop`.

## egm-draft

Rail: `brainstorm` (done or skipped), `draft`, then the review stages as
`todo`.

* **Each section approval:** the drafted part becomes one board section with
  `approvable: true` and `status: "draft"`, plus the gate
  `R<n>-G-draft-<section>` with `approve` and `revise`. The reader should be
  able to approve the design decision itself from the picture: what the design
  is, how it behaves, what it was chosen over, and what the work involves.
* Approved sections keep `status: "approved"` and lose `approvable`. A section
  approve on the card and the gate choice mean the same thing; take either.
* **Option decisions:** when the skill asks the user to choose between design
  options, the gate's options are the candidates, and the section makes their
  trade-offs visible.

## egm-review

Rail: `s5` Zoom out, `s6` Comprehension, `s7` Critic, `s8` Zoom out 2, `s9`
Readiness. Mark stages a preset skips as `skipped`.

* **Preset gate:** `R1-G-preset` with `interactive`, `consolidated`, `feature`,
  `implementation`.
* **Each stage:** its findings become cards (`lens` = reviewer). The reader
  should also see which reviewers ran and which did not.
* **Stage 6 (Comprehension):** the reader should see the gap between what the
  document means and what a fresh reader understood. Gaps become findings.
* **Stage gates** (`R<n>-G-s5` … `R<n>-G-s9`): keep the skill's options:
  `proceed`, `resolve` (Stages 7 and 9), `manual`, `pause`. On `resolve`, run
  `egm-resolve` with the board decisions already given: do not ask again about
  items the user decided.
* **Uninterrupted preset:** publish once at the end with all stages `done` and
  the consolidated findings.

## egm-review-loop

Rail: one stage per reviewer group run, finding cards per reviewer. The
aggregated resolution hand-off gate goes on the board with the options the skill
lists (auto accept, continue, interactive). On "interactive", the cards are the
walkthrough.

## egm-resolve

* Each finding card carries the AI suggestion (`suggestion`) and the proposed
  edit in short form (`fix`); the full edit stays in
  `goldfish_review_report.md`. `ESCALATE` cards come first.
* When a fix changes structure or behaviour, the card's `visual` should let the
  reader see the change.
* **Resolution gate:** `R<n>-G-resolve` with `apply` (apply my decisions;
  undecided fixes follow the suggestion), `continue` (no changes), `chat` (walk
  me through it in chat).
* After applying, mark the affected sections `changed` and log counts in
  `history`.

## egm-lite

Rail: the lite phases you run. The reader should see progress through the
checklist and the bottom line (`headline`). The completion gate goes on the
board; when the user would type `review` or `goldfish`, offer those as options.

## egm-drift-report

The reader should see, per document, where the document and the code agree and
where they part. Divergences become findings with `where` = file path. Gate:
`update-doc`, `update-code`, `decide-later`.

## egm-bootstrap

The reader should see which parts of the tree are documented and which are
left. The skill's gates go on the board.
