<!--
SPDX-License-Identifier: Apache-2.0
-->

# What each skill puts on the board

Read [PROTOCOL.md](PROTOCOL.md) first. Each part says what the reader needs to
grasp at that point and which decisions move to the board. How to draw it is
yours to decide. Keep the skill's gate options and their meaning; shorten the
labels and put the recommended step first.

## egm-brainstorm

* **Clarifying:** the idea as you understand it, and where the holes are. Open
  questions go in a section's `questions`; ask them briefly in chat too.
* **Readiness gate** `R<n>-G-ready`: `review`, `clarify`.
* **After the Goldfish review:** the concept, what it leaves out, the
  alternatives it beat, what could go wrong. Objections that need the user are
  calls.
* **Handoff gate** `R<n>-G-handoff`: `draft` first, then `publish`, `refine`,
  `stop`. On `draft`, start `egm-draft` yourself.

## egm-draft

* **Each drafted part** is a section the user can approve by leaving it alone or
  change with a note: what the design is, how it behaves, what it was chosen
  over, and what the work involves. The gate `R<n>-G-draft-<section>` moves on.
* **Option decisions** are calls whose `choices` are the candidates, with their
  trade-offs visible in the section.
* **Handoff** `R<n>-G-next`: `review` (Review with Goldfishes) first, then
  `revise`, `stop`. On `review`, start `egm-review` yourself.

## egm-review

* **Rail:** `s5` Zoom out, `s6` Comprehension, `s7` Critic, `s8` Zoom out 2, `s9`
  Readiness; stages a preset skips are `skipped`.
* **Preset gate** `R1-G-preset`: `interactive`, `consolidated`, `feature`,
  `implementation`.
* **Each stage:** which reviewers ran, and what they found, pinned to the part
  of the design it concerns. Stage 6 shows the gap between what the document
  means and what a fresh reader understood.
* **Stage gates** `R<n>-G-s5` … `R<n>-G-s9`: `proceed`, `resolve` (Stages 7 and
  9), `manual`, `pause`. On `resolve`, run `egm-resolve` with the board's calls
  already made; do not ask again.
* **End:** `R<n>-G-next` with what can follow (resolve what is left, check the
  code against the design, stop).

## egm-review-loop

One stage per reviewer group run. The aggregated hand-off goes on the board
with the skill's options; on "interactive", the calls are the walkthrough. Run
alone, it ends with `R<n>-G-next`.

## egm-resolve

Each finding is a call carrying the suggestion and the proposed edit in short
form (the full edit stays in `goldfish_review_report.md`); `ESCALATE` first.
When a fix changes structure or behaviour, its `visual` shows the change. Gate
`R<n>-G-resolve`: `apply`, `continue`, `chat`. After applying, mark the
affected sections `changed` and log counts in `history`.

## egm-lite

Progress through the checklist and the bottom line. The completion gate goes on
the board, offering `review` or `goldfish` where the user would type them.

## egm-drift-report

Per document, where the document and the code agree and where they part.
Divergences are calls with `where` set; options `update-doc`, `update-code`,
`decide-later`.

## egm-bootstrap

Which parts of the tree are documented and which are left. The skill's gates
go on the board.
