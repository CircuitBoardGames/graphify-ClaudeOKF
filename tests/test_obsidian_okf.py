"""Open Knowledge Format (OKF) conformance for the Obsidian export.

OKF spec §9: every non-reserved markdown file in a bundle must contain
parseable YAML frontmatter with a non-empty `type` field. graphify's Obsidian
vault (one .md per node, one _COMMUNITY_*.md per community) is written as a
conformant OKF bundle - this test asserts that directly rather than trusting
it by inspection, including the legacy/hand-built-graph case where a node
carries no `file_type` attribute at all.
"""
import re

import networkx as nx

from graphify.export import to_obsidian

_FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def _frontmatter(text: str) -> dict:
    m = _FRONTMATTER_RE.match(text)
    assert m, "note has no parseable YAML frontmatter block"
    fields = {}
    for line in m.group(1).splitlines():
        if not line.strip() or line.startswith("  ") or line.strip() == "---":
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip().strip('"')
    return fields


def test_every_note_has_nonempty_type_including_nodes_missing_file_type(tmp_path):
    G = nx.Graph()
    # n0 has no file_type at all - the legacy/hand-built-graph case build.py's
    # own normalization would otherwise be relied on to prevent.
    G.add_node("n0", label="Untyped", source_file="a.py", community=0)
    G.add_node("n1", label="Typed", file_type="code", source_file="b.py", community=0)
    G.add_edge("n0", "n1", relation="calls", confidence="EXTRACTED")
    communities = {0: ["n0", "n1"]}

    to_obsidian(G, communities, str(tmp_path))

    md_files = list(tmp_path.glob("*.md"))
    assert md_files, "no notes were written"
    for path in md_files:
        fields = _frontmatter(path.read_text(encoding="utf-8"))
        assert fields.get("type"), f"{path.name} has empty or missing `type`"
        assert fields.get("title"), f"{path.name} has empty or missing `title`"
        assert fields.get("timestamp"), f"{path.name} has empty or missing `timestamp`"


def test_node_note_maps_file_type_to_okf_type_and_resource(tmp_path):
    G = nx.Graph()
    G.add_node("n0", label="Widget", file_type="code", source_file="widget.py", community=0)
    to_obsidian(G, {0: ["n0"]}, str(tmp_path))

    fields = _frontmatter((tmp_path / "Widget.md").read_text(encoding="utf-8"))
    assert fields["type"] == "code"
    assert fields["title"] == "Widget"
    assert fields["resource"] == "widget.py"


def test_community_note_type_is_always_community(tmp_path):
    G = nx.Graph()
    G.add_node("n0", label="Alpha", file_type="code", source_file="a.py")
    to_obsidian(G, {0: ["n0"]}, str(tmp_path))

    comm_notes = list(tmp_path.glob("_COMMUNITY_*.md"))
    assert len(comm_notes) == 1
    fields = _frontmatter(comm_notes[0].read_text(encoding="utf-8"))
    assert fields["type"] == "community"
    assert fields.get("title")
