# JC Integration Plan for Third-Party Repos

Goal: Integrate selected open-source projects so `jc` can access relevant logic, documentation, and update streams while remaining license-compliant.

Phases:

1. Inventory & Compatibility
   - List third-party repos and confirmed licenses (see `OPEN_SOURCE_LICENSE_CHECKLIST.md`).
   - Mark any copyleft (AGPL/GPL) items and determine if they can be used as independent services or only as reference material.

2. Minimal Integration Layer
   - Provide a lightweight metadata registry `integrations/third_party.json` listing repo name, local path, license, and a short description.
   - Add a script `scripts/update_third_party.py` to fetch and refresh repos (git pull if exists, git clone otherwise).

3. Knowledge Access
   - Extract README and key docs into `integrations/docs/<repo>.md` for `jc` to index.
   - Create `jc/third_party.py` helpers to read `integrations/third_party.json` and provide queryable metadata.

4. Updater & Automation
   - Add scheduled updater (cron/task) to run `scripts/update_third_party.py` periodically.
   - Add a small CLI to refresh metadata and generate a `THIRD_PARTY_NOTICES.md` file.

5. Tests and Verification
   - Run unit tests validating `jc` can read the metadata and that updater exits cleanly.

Security & License Notes:
 - Keep AGPL components isolated; avoid embedding AGPL code inside jc runtime unless willing to accept AGPL obligations.
 - Prefer reading docs, extracting algorithms, or linking to permissively licensed implementations.

Files added/modified by this plan:
 - `integrations/third_party.json` (metadata registry)
 - `scripts/update_third_party.py` (updater script)
 - `scripts/generate_third_party_notices.py` (helper to produce NOTICE file)
 - `jc/third_party.py` (runtime helper)

Next step: implement the minimal updater and metadata files and run the updater once to populate `integrations/`.
