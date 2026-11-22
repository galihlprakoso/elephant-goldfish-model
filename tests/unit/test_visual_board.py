# SPDX-License-Identifier: Apache-2.0

"""Render the visual board template and check the facts the agent relies on."""

import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
BOARD = ROOT / "resources" / "visual_board"
DATA = re.compile(r'<script id="egm-board-data" type="application/json">(.*?)</script>', re.S)


def example() -> dict:
  html = (BOARD / "board.html").read_text(encoding="utf-8")
  return json.loads(DATA.search(html).group(1).replace("<\\/", "</"))


def render(tmp_path: Path, data: dict, *flags: str) -> tuple[str, str]:
  src = tmp_path / "board.json"
  out = tmp_path / "board.html"
  src.write_text(json.dumps(data), encoding="utf-8")
  run = subprocess.run([sys.executable, str(BOARD / "render_board.py"), str(src), str(out), *flags],
                       capture_output=True, text=True, check=True)
  return out.read_text(encoding="utf-8"), run.stdout


def test_example_findings_point_at_sections() -> None:
  data = example()
  sections = {s["id"] for s in data["sections"]}
  assert all(f["where"] in sections for f in data["findings"])


def test_render_names_page_and_embeds_data(tmp_path: Path) -> None:
  data = example()
  data["session"]["title"] = "Webhook </script> retries"
  html, _ = render(tmp_path, data)
  assert "<title>EGM Board - Webhook &lt;/script&gt; retries</title>" in html
  assert json.loads(DATA.search(html).group(1).replace("<\\/", "</")) == data
  assert not html.lstrip().lower().startswith("<!doctype")


def test_local_render_is_a_standalone_page(tmp_path: Path) -> None:
  html, _ = render(tmp_path, example(), "--local")
  assert html.lower().startswith("<!doctype html>")
  assert html.rstrip().endswith("</html>")


def test_notes_report_unpinned_findings(tmp_path: Path) -> None:
  data = example()
  data["findings"][0]["where"] = "nowhere"
  _, notes = render(tmp_path, data)
  assert "names no section" in notes
  assert "session.example is true" in notes
