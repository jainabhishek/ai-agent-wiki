# Log

Append-only, chronological record of activity. Newest at the bottom. Each entry
starts with `## [YYYY-MM-DD] <type> | <title>` so the log is greppable:

```
grep "^## \[" log.md | tail -5
```

Event types: `ingest`, `query`, `lint`, `schema`.

---

## [2026-06-21] schema | wiki initialized
- Scaffolded the research-wiki structure per the LLM Wiki pattern.
- Created: CLAUDE.md (schema), index.md, log.md, templates/, tools/search.py.
- Ready to ingest the first source.
