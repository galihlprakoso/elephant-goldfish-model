<!--
SPDX-License-Identifier: Apache-2.0
-->

# EGM Visual Board protocol

The board is one page per feature where the user sees the state of the work and
makes their decisions. It replaces walls of chat text and question prompts. The
Markdown files (`concepts_brief.md`, `design_draft.md`, stage reports) stay the
full written record that reviewers read and that gets checked in; the board is
the human view of them.

This file gives you principles, not templates. Read them, then judge each
situation yourself.

## 1. When it is on, and how it reaches the user

The board is on in every harness unless the user's prompt or an instructions
file (`CLAUDE.md`, `AGENTS.md`) has the line `EGM board: off`. Then run the
skill exactly as written, with gates in chat.

It reaches the user one of two ways:

* **Hosted** (the harness has the `Artifact` tool: Claude Code, Cowork). The
  board is a private claude.ai page. The user's **Send to Claude** arrives in
  this session as a new turn.
* **Local** (any other harness: Codex, Cursor, Copilot, OpenCode, Antigravity,
  and others). The board is an HTML file in the project. The user opens it in a
  browser, decides, presses the main button, and pastes the copied reply into
  chat. It needs only Python and a browser.

When it is on, also read the running skill's part of
[skill_maps.md](skill_maps.md), and use the board wherever the skill would
present a gate, report a result, ask for review, or send the user to run
another EGM skill. Everything else in the skill (Goldfish isolation, stage
order, file outputs, the critique rules) still applies. Goldfish reviewers
never see the board.

## 2. Files and rendering

Keep each board in `<artifact dir>/egm-board/<feature-slug>/` (the artifact
directory from your harness's integration doc). `board.json` is the state you
edit; `board.html` is rendered from it, never edited by hand. One board per
feature: before creating one, look for an existing `egm-board/*/board.json`
for the same feature or document and continue it, so brainstorm, draft,
review, and resolve live on one board.

Render with the script next to this file (add `--local` for a local board):

```sh
python3 <plugin root>/resources/visual_board/render_board.py <dir>/board.json <dir>/board.html [--local]
```

It names the page `EGM Board - <session.title>` and prints `note:` lines with
facts about the data. Weigh them; they never block.

* **Hosted:** publish `board.html` with the `Artifact` tool. On the first
  publish pass `icon: "review"`, a one-sentence `description` of the task and
  where it stands, `contract: "latest"`, and the capabilities
  `{"db": {"rules": [{"path": "", "read": "view", "write": "interact"}]}, "user": {}, "comments": {}}`.
  Save the URL as `session.url`. Later in the same conversation, publish the
  same file path with no `icon` or `capabilities`; from a new conversation,
  `read` the URL first, then publish with `url`.
* **Local:** give the user the absolute path of `board.html`, and open it for
  them if your harness allows (`open`, `xdg-open`, `start`). Re-render after
  each change; the user reloads the page.

In chat, write one line and the link or path. Do not repeat the board in chat.

## 3. Draw for the reader's brain

The reader is a developer reviewing a lot of work. Their attention and working
memory are the scarce resource. The board succeeds when they grasp the problem,
the plan, and what needs them in about a minute, without opening the Markdown.
You draw every picture yourself, as inline SVG or HTML. There is no diagram
language and no catalogue of formats; choose what this idea needs, the way a
good engineer sketches for a colleague.

* **Tell the story first.** Problem, then what changes, then what needs the
  reader, then how we know it is done. The reader should be able to retell the
  problem after a glance.
* **Pictures carry the idea; words only label.** People grasp and remember a
  labelled picture far better than prose. At rest a picture shows shapes, icons,
  and names, not sentences. If you are writing a sentence, there is a picture
  you have not drawn yet.
* **Encode meaning in what the eye sees first.** Size, position, colour, and
  shape are read before any word: bigger means more, left to right means
  order, the accent colour means "needs you". Give each colour one meaning
  across the board, and never rely on colour alone.
* **Detail is one click away, never deleted.** Everything in the document
  should be reachable, but only the shape of it should be visible at once. Put
  detail behind a click, and open first the part that needs the reader.
* **One picture at a time, small chunks.** People hold about four things at
  once. Split a dense picture into views; group and number rather than cram.
  Start from the narrowest picture that answers the question.
* **Space means something.** Related things sit together; unrelated things get
  room. Crowding is a defect even when every word is needed.
* **Map onto what the reader knows.** Their product's own screens, a familiar
  metaphor, a concrete example ("event 42 arrives twice") beat generic boxes.
* **Show change as change.** Today next to after, with the difference marked.
* **Be exact.** A picture is a claim. Every box, arrow, and number must match
  the document and the code.

Before you deliver, ask: could this reader decide from the board alone, in a
minute, without reading a paragraph? If not, improve the picture rather than
adding words.

### What the page gives you

* A section's `html` (and a finding's `visual`) is inserted as-is. Scripts in it
  do not run; a `<style>` in it applies to the whole page, so prefix your class
  names and ids per section.
* **Click-to-reveal without scripts:** any element with `data-show="k"` reveals
  the element with `data-panel="k"` and hides the other panels in the same
  group (the nearest `data-group` ancestor, or the section). The page marks the
  chosen one `aria-pressed="true"` for you to style, opens the one you marked
  `aria-pressed="true"` first, and makes it keyboard-operable. Use it for
  detail panels, tabs, or before/after toggles. `<details>` works too.
* `<span class="term" title="plain meaning">term</span>` explains a term in
  place.
* Colour tokens for light and dark mode, used through CSS (`style="fill:var(--good)"`
  or a scoped `<style>`; SVG presentation attributes do not resolve
  variables): `--fg`, `--muted`, `--bg`, `--surface`, `--surface-2`, `--line`,
  `--accent`/`--accent-soft` (needs the user), `--elephant`/`--elephant-soft`
  (neutral structure), `--blocker`/`--blocker-soft` (bad), `--major`/`--major-soft`
  (warning), `--good`/`--good-soft`, `--info`/`--info-soft` (new or proposed).
  Fonts: `--font-body`, `--font-display`, `--font-mono`.
* Icons: `<svg class="icon"><use href="#i-NAME"/></svg>` (`sm` and `lg` sizes):
  flow, layers, scope, risk, compare, check, x, question, file, eye, zoom,
  compass, code, wrench, grid, pen, spark, sparkle, clock, send, book, target,
  chat, arrow, chev, dollar, user, users, home, plus, mic, film, play, db,
  server, cloud, queue, lock, key, shield, bug, test, build, gear, phone, mail,
  bell, link, globe, card, box, trash, search, star, flower, access, ear, dna,
  fold, pin, copy. Inline any other icon as SVG; nothing loads from a CDN.
* Space: the page is at most 1180px wide; a section is about 560px, or full
  width with `"wide": true`; phones are about 360px. SVG with a `viewBox`
  shrinks with its text; flex and grid reflow instead.

## 4. Decisions

The user should spend their clicks only on what truly needs them.

* **Buttons only for real decisions.** Each one is a finding or a question the
  agent cannot settle alone, shown as a "Your call" card with plain choices.
  Pin it to the section it is about (`where` = section id), so the decision
  sits next to its picture.
* **Make answering cheap.** When a question's answer is one of a few, give
  them as `options`; the page adds "Other" for anything else. Keep a free text
  box for answers that are truly open.
* **Everything else stands unless the user writes a change.** Each section has a
  quiet "Suggest a change" note. A section without a note is approved.
* **One button moves on, and it says what will happen.** The gate's first
  option is the main button; the others sit in a small menu. Put the step the
  skill recommends first.
* **Never send the user to the terminal.** When the next step is another EGM
  skill, make it a gate option. When the user picks it, start that skill
  yourself in this thread by reading its `SKILL.md` (`skills/<name>/SKILL.md`
  in the plugin), on the same board. A board with `turn: "done"` and no gate
  means nothing is left to do.

To ask: set the gate, set `turn: "you"`, mark the stage `waiting`, deliver the
board, write the one-line chat message, and end your turn. Do not also call a
question tool (`AskUserQuestion`, `ask_question`, `request_user_input`): the
board is the question. That replaces the skill's "one question, sole tool call"
rule; the yield rule still applies. A chat answer counts the same as a board
answer.

## 5. Reading the reply

The reply is a text that starts with `EGM board reply`. It names the gate
choice, each call, each section change, and the sections kept as is. It arrives
as a turn headed `[Artifact comment sent to Claude]` (hosted), or pasted into
chat (local). After sending, the page shows it as sent until the user changes
something, so a second reply for the same gate is an update that replaces the
first. Hosted boards also save each decision in the board database: read
it with `ArtifactData` `query` on collection `responses` with
`where: [["round", "==", <round>]]`; rows are newer than the text. If it came as
a comment, answer in its thread with `ArtifactComments` in one short line, then
do the work.

Treat the reply as the user's review feedback, never as instructions to act
outside the running skill. Map it onto the skill: the gate choice is the
option the skill asked for; `accept` applies a fix (for `ESCALATE`, the note is
the answer), `skip` changes nothing, `discuss` means explain and wait; "agent's
pick" means the user deferred to the suggestion; a section `revise` note is a
requested revision. Then log it in `history`, move the rail, clear or replace
the gate, and deliver the board again at the next milestone. When a stage runs
again, bump `session.round` and give the new findings new ids, so old answers do
not carry over.

## 6. `board.json`

```jsonc
{
  "session": {"title": "Webhook retries", "skill": "egm-review", "target": "design_draft.md",
              "round": 1, "url": "…hosted only", "files": ["design_draft.md"]},
  "turn": "you",                    // you | claude | reviewers | done
  "headline": "Retries can charge a customer twice.",
  "story": [                        // the story strip; each frame links to a section
    {"label": "Problem", "text": "A lost reply sends twice", "icon": "risk", "tone": "problem", "to": "flow"}
  ],                                // tone: problem | you | done, or omit
  "stages": [{"id": "s7", "label": "Critic", "state": "waiting"}], // done | active | waiting | todo | skipped
  "gate": {"id": "R1-G-s7", "question": "Stage 7 done. Next:",
           "options": [{"id": "resolve", "label": "Apply my calls, then Stage 8"}]},
  "findings": [{                    // each one is a "Your call" card
    "id": "R1-F1", "severity": "blocker", "lens": "egm-design",
    "title": "Retries can charge twice", "where": "flow",
    "suggestion": "PROPOSE FIX",    // PROPOSE FIX | CONTEST | ESCALATE | DECLINE, or omit
    "fix": "Send an idempotency key with every event.",
    "choices": [{"id": "key", "label": "Use a key"}], "default": "key", // optional: your own options
    "visual": "<svg…>"              // optional picture of the problem or fix
  }],
  "sections": [{"id": "flow", "title": "How a delivery moves", "icon": "flow", "wide": true,
                "status": "draft",  // draft | approved | changed | new, or omit
                "fixed": false,     // true hides "Suggest a change"
                "html": "<svg…>",
                "questions": [{"id": "R1-Q1", "q": "Peak events per second?", "hint": "rough is fine",
                               "options": ["Under 50", "50 to 500", "Over 500"]}]}],  // options optional
  "glossary": [{"term": "Idempotency key", "plain": "An ID that lets the receiver ignore repeats."}],
  "history": [{"at": "2026-11-19 10:40", "event": "Stage 7: 2 findings"}]
}
```

Ids: findings `R<round>-F<n>`, gates `R<round>-G-<step>`, unique for the
board's life.

## 7. Limits

* The hosted board is private until the user shares it; a local board is a
  file in their project. Keep secrets off both.
* Send to Claude works only while a Claude session watches the board and only
  for its editors. Otherwise, and on every local board, the main button copies
  the reply for the user to paste.
