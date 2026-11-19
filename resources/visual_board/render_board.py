# SPDX-License-Identifier: Apache-2.0
"""Render an EGM board page from the template and a board JSON file.

Usage: python3 render_board.py <board.json> <out.html> [--template <board.html>]

The template's <script id="egm-board-data"> block is replaced with the JSON.
Claude keeps board.json as the board's state and runs this before each publish,
so the HTML never has to be rewritten by hand.
"""

import argparse
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


def warnings(data: dict) -> list[str]:
  """Facts about the board worth showing to the agent; never blocks a render."""
  out = []
  if data.get("turn") not in TURNS:
    out.append(f"turn should be one of {sorted(TURNS)}")
  if data.get("session", {}).get("example"):
    out.append("session.example is true: Send to Claude stays off. Remove it.")
  if data.get("turn") == "you" and not data.get("gate"):
    out.append("turn is 'you' but there is no gate: the viewer has no button.")
  for f in data.get("findings", []):
    if f.get("severity") not in SEVERITIES:
      out.append(f"finding {f.get('id')}: severity {f.get('severity')!r}")
    if len(str(f.get("title", "")).split()) > 12:
      out.append(f"finding {f.get('id')}: title over 12 words")
    if len(str(f.get("fix", "")).split()) > 30:
      out.append(f"finding {f.get('id')}: fix over 30 words")
  for s in data.get("sections", []):
    visual = any(
        b.get("type") in {"diagram", "compare", "stats", "scope", "flow",
                          "risks", "beforeAfter", "questions"}
        for b in s.get("blocks", []))
    if not visual:
      out.append(f"section {s.get('id')}: no visual block")
  ids = [f.get("id") for f in data.get("findings", [])]
  if len(ids) != len(set(ids)):
    out.append("finding ids repeat; decisions would collide")
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
  Path(args.out).write_text(html, encoding="utf-8")
  print(f"wrote {args.out}")
  for w in warnings(data):
    print(f"note: {w}")
  return 0


if __name__ == "__main__":
  sys.exit(main())
