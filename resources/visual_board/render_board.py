# SPDX-License-Identifier: Apache-2.0
"""Render an EGM board page from the template and a board JSON file.

Usage: python3 render_board.py <board.json> <out.html> [--template <board.html>]

The template's <script id="egm-board-data"> block is replaced with the JSON.
Claude keeps board.json as the board's state and runs this before each publish,
so the HTML never has to be rewritten by hand.
"""

import argparse
import html as html_lib
import json
from pathlib import Path
import re
import sys

BLOCK = re.compile(
    r'(<script id="egm-board-data" type="application/json">)(.*?)(</script>)',
    re.DOTALL,
)
SEVERITIES = {"blocker", "major", "nit"}
TURNS = {"you", "claude", "reviewers", "done"}


MERMAID = re.compile(
    r"^\s*(flowchart|graph|sequenceDiagram|stateDiagram|classDiagram|erDiagram|"
    r"gantt|pie|mindmap|journey)\b", re.MULTILINE)
TAG = re.compile(r"<(style|script)\b.*?</\1>|<[^>]+>", re.DOTALL | re.IGNORECASE)
ID_ATTR = re.compile(r'\bid="([^"]+)"')
TITLE = re.compile(r"<title>.*?</title>", re.DOTALL)


def page_title(data: dict) -> str:
  """The artifact's name in the gallery and the browser tab."""
  name = str(data.get("session", {}).get("title") or "").strip()
  return "EGM Board" + (f" - {name}" if name else "")


def visible_words(html: str) -> int:
  return len(TAG.sub(" ", html or "").split())


def warnings(data: dict) -> list[str]:
  """Facts about the board for the agent to weigh; never blocks a render."""
  out = []
  if not str(data.get("session", {}).get("title") or "").strip():
    out.append("session.title is empty: the artifact is named only 'EGM Board'")
  if data.get("turn") not in TURNS:
    out.append(f"turn should be one of {sorted(TURNS)}")
  if data.get("session", {}).get("example"):
    out.append("session.example is true: Send to Claude stays off. Remove it.")
  if data.get("turn") == "you" and not data.get("gate"):
    out.append("turn is 'you' but there is no gate: the viewer has no button.")
  pictures = [(f"section {s.get('id')}", s.get("html", ""))
              for s in data.get("sections", [])]
  pictures += [(f"finding {f.get('id')}", f.get("visual", ""))
               for f in data.get("findings", []) if f.get("visual")]
  seen_ids: dict[str, str] = {}
  for name, html in pictures:
    if not isinstance(html, str):
      out.append(f"{name}: html/visual must be a string of SVG or HTML")
      continue
    if MERMAID.search(html):
      out.append(f"{name}: looks like Mermaid text; nothing renders it here")
    if "<script" in html.lower():
      out.append(f"{name}: <script> inside html does not run")
    for i in ID_ATTR.findall(html):
      if i in seen_ids and seen_ids[i] != name:
        out.append(f"{name}: id {i!r} also used in {seen_ids[i]}; "
                   "url(#...) references will point at the first one")
      seen_ids.setdefault(i, name)
  for s in data.get("sections", []):
    if not s.get("html") and not s.get("questions"):
      out.append(f"section {s.get('id')}: empty (no html, no questions)")
  for f in data.get("findings", []):
    if f.get("severity") not in SEVERITIES:
      out.append(f"finding {f.get('id')}: severity {f.get('severity')!r}")
  ids = [f.get("id") for f in data.get("findings", [])]
  if len(ids) != len(set(ids)):
    out.append("finding ids repeat; decisions would collide")
  counts = ", ".join(f"{n.split()[1]} {visible_words(h)}"
                     for n, h in pictures if isinstance(h, str))
  if counts:
    out.append(f"visible words per picture: {counts}")
  return out


def main() -> int:
  parser = argparse.ArgumentParser()
  parser.add_argument("data")
  parser.add_argument("out")
  parser.add_argument(
      "--template", default=str(Path(__file__).with_name("board.html")))
  args = parser.parse_args()
  data = json.loads(Path(args.data).read_text(encoding="utf-8"))
  template = Path(args.template).read_text(encoding="utf-8")
  payload = json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")
  html, count = BLOCK.subn(lambda m: m.group(1) + "\n" + payload + "\n" + m.group(3),
                           template, count=1)
  if count != 1:
    print("template has no egm-board-data block", file=sys.stderr)
    return 1
  title = html_lib.escape(page_title(data), quote=False)
  html = TITLE.sub(lambda m: f"<title>{title}</title>", html, count=1)
  Path(args.out).write_text(html, encoding="utf-8")
  print(f"wrote {args.out}")
  for w in warnings(data):
    print(f"note: {w}")
  return 0


if __name__ == "__main__":
  sys.exit(main())
