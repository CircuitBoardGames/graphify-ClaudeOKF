# Fork Changelog

Changes specific to the [`CircuitBoardGames/graphify-ClaudeOKF`](https://github.com/CircuitBoardGames/graphify-ClaudeOKF) fork, layered on top of upstream [`Graphify-Labs/graphify`](https://github.com/Graphify-Labs/graphify). Upstream's own release notes live in `CHANGELOG.md`, kept **verbatim** so upstream syncs never conflict here — record fork-only changes in this file instead.

## Unreleased
- Feature: the Obsidian export (`to_obsidian()`) is now an [Open Knowledge Format](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)-conformant bundle. Every node note and `_COMMUNITY_*.md` overview note carries a non-empty `type` in its YAML frontmatter (spec §9) plus the recommended `title`, `resource`, and `timestamp` fields; `type` falls back to `"concept"` when a node has no `file_type`, matching `build.py`'s own normalization, so the guarantee holds even for a hand-built or legacy `graph.json`. See `tests/test_obsidian_okf.py`.
