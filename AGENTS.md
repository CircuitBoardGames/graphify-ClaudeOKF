## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- After modifying code files in this session, run `graphify update .` to keep the graph current (AST-only, no API cost)

## GitHub release asset attachment (cross-repo convention)

The GitHub MCP tools available to agent sessions can't create a release, create a tag, or upload a
release asset, and tag pushes are rejected by this environment's git proxy even though branch
pushes work. Attach files to an existing release via a GitHub Actions workflow instead — the
Actions-native `GITHUB_TOKEN` has `contents: write` there. Canonical example:
`.github/workflows/vault-viewer-release-asset.yml` in
[`CircuitBoardGames/webobsidian-GitPusher`](https://github.com/CircuitBoardGames/webobsidian-GitPusher)
— `workflow_dispatch` + `softprops/action-gh-release` with `tag_name`/`files`, triggered via the
`actions_run_trigger` MCP tool and verified with `actions_list`/`get_release_by_tag`. The
release/tag itself still needs to exist first (created manually, outside these tools' reach). Apply
this pattern in any repo needing a release asset attached from an agent session.
