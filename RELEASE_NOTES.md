JC-Agent release notes (draft)

Release candidate: improvements to secrets, testing, and CI

Highlights (2026-01-11):
- Centralized safe secrets helper (`jc/secrets.py`) that prefers `OPENAI_API_KEY` and safely loads `.env` files.
- `.env.example` and documentation to prevent accidental secret commits.
- Focused unit tests for JC internals and GUI helpers to improve reliability.
- GitHub Actions CI workflow to run `pytest -q` and collect coverage artifacts.

Notes for reviewers:
- No secrets are stored in this branch. Please review `README.md` and `.env.example` before merging.
- Consider squashing related testing commits into a single test-suite commit for clarity.
