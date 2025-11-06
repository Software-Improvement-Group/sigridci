from pathlib import Path
import re

DOC_PATH = Path("docs/integrations/integration-sigrid-mcp.md")

def test_file_exists():
    assert DOC_PATH.exists(), f"{DOC_PATH} not found"

def test_title_is_expected():
    text = DOC_PATH.read_text(encoding="utf-8")
    # first non-empty line should be the H1 title
    for line in text.splitlines():
        line = line.strip()
        if line:
            assert line.startswith("# Sigrid MCP Integrations"), f"Unexpected title: {line!r}"
            return
    assert False, "Document is empty"

def test_contains_guardrails_heading():
    text = DOC_PATH.read_text(encoding="utf-8")
    # allow either "## Sigrid Guardrails MCP" or "### Sigrid Guardrails MCP" just in case,
    # but prefer the exact heading used in the doc.
    assert re.search(r"^#{2,3}\s+Sigrid Guardrails MCP", text, flags=re.MULTILINE), \
        "Missing expected 'Sigrid Guardrails MCP' heading"

def test_no_merge_conflict_markers():
    text = DOC_PATH.read_text(encoding="utf-8")
    for marker in ("<<<<<<<", "=======", ">>>>>>"):
        assert marker not in text, f"Found merge conflict marker {marker}"

def test_links_use_https():
    text = DOC_PATH.read_text(encoding="utf-8")
    urls = re.findall(r'\((https?://[^\)]+)\)', text)
    non_https = [u for u in urls if not u.startswith("https://")]
    assert not non_https, f"Found non-https links: {non_https}"