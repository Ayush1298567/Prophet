# Secret History Review

Date: 2026-05-11

This note records the current `make secrets-archaeology` result without printing matched secret-like values.

## Current Result

Current tracked and untracked non-ignored files pass the current-only scan:

```bash
./scripts/check-secrets-archaeology.sh --current-only
```

Full git-history archaeology currently fails on historical
`LOG4SHELL_INSTRUCTIONS.md` password-like content in these commits:

| Commit | Date | Subject |
|---|---:|---|
| `4cb04a1f003a62876dfe15d0ff11f31635bde945` | 2026-05-02 | Refactor docs to unified Prophet language; remove stale pre-event artifacts |
| `e025907c723645b2d725d424243e6f35b7100deb` | 2026-05-02 | Merge prophet-console-ui: console UI, lab setup, updated world-side |
| `c2a5082c34d85491f93c23bb98c09f82d15148e1` | 2026-05-02 | Hackathon work: console UI updates, lab setup, world-side forecaster |

The scanner reports only commit IDs and paths. Do not paste the matched line or value into issues, PR comments, docs, or agent prompts.

## Release Decision Needed

Before any public release, the owner must choose one of these paths:

- If the value was real or could have been reused, rotate or revoke it first,
  then remove the historical commit content with an explicit history-rewrite or
  new-clean-repo release plan.
- If the value was a non-secret demo/test value, record an explicit
  false-positive exception in the release review, including who reviewed it and
  why it is not sensitive.
- If ownership cannot be confirmed, treat it as sensitive and do not publish
  the current git history as clean.

## Safe Local Review

Review locally only:

```bash
make secrets-archaeology
git show <commit>:LOG4SHELL_INSTRUCTIONS.md
```

Do not use `git reset --hard`, `git filter-repo`, BFG, force-push, or branch
deletion unless the repo owner explicitly approves that release cleanup.

## Current Working Release Boundary

`make release-hygiene` intentionally runs only the current-worktree secret scan
so normal local pilot verification remains usable while this history issue is
pending. A public release still requires resolving the full history finding.
