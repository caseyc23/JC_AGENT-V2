# Open Source License Compliance Checklist for JC-agent-

This checklist helps ensure compliance when integrating code or assets from the following repositories.

Confirmed licenses (found in workspace):

## 1. dyad — Apache-2.0
- License file path: `dyad/LICENSE` (Apache 2.0). Note: `dyad/src/pro/LICENSE` may apply to pro components; avoid using `src/pro/` without review.
- Actions:
	- [ ] Attribute original authors in documentation or a `NOTICE` file.
	- [ ] Include a copy of the Apache 2.0 license in any distribution that contains this code.

## 2. khoj — AGPL-3.0
- License file path: `khoj/LICENSE` (AGPL-3.0).
- Actions:
	- [ ] Attribute original authors in documentation.
	- [ ] Include a copy of the AGPL-3.0 license in distributions that include this code.
	- [ ] If used or modified in a networked service, ensure source availability and comply with AGPL obligations.

## 3. Promptgpt — Apache-2.0
- License file path: `Promptgpt/LICENSE` (Apache 2.0).
- Actions:
	- [ ] Attribute original authors and include Apache 2.0 license text.

## 4. SurfSense — Apache-2.0
- License file path: `SurfSense/LICENSE` (Apache 2.0).
- Actions:
	- [ ] Attribute original authors and include Apache 2.0 license text.

## 5. Local-NotebookLM — Apache-2.0
- License file path: `Local-NotebookLM/LICENSE` (Apache 2.0).
- Actions:
	- [ ] Attribute original authors and include Apache 2.0 license text.

## 6. notebooklm-mcp — MIT
- License file path: `notebooklm-mcp/LICENSE` (MIT).
- Actions:
	- [ ] Attribute original authors and include MIT license text.

Repos requiring manual license confirmation (no top-level LICENSE found):

## 7. local-deepthink (license not found)
- Actions:
	- [ ] Manually inspect `local-deepthink` for license or copyright notices (README, package manifests, or files).
	- [ ] Contact repository owner or avoid integrating until license is confirmed.

## 8. notebookllamadev-guide (license not found)
- Actions:
	- [ ] Manually inspect `notebookllamadev-guide` for license or copyright notices.

## 9. PageLM (license not found)
- Actions:
	- [ ] Manually inspect `PageLM` for license or copyright notices.

## 10. ai_hacking_study_prompts (license not found)
- Actions:
	- [ ] Manually inspect `ai_hacking_study_prompts` for license or copyright notices.

## 11. ai-in-the-terminal (license not found)
- Actions:
	- [ ] Manually inspect `ai-in-the-terminal` for license or copyright notices.

## 12. n8n-terry-guide (license not found)
- Actions:
	- [ ] Manually inspect `n8n-terry-guide` for license or copyright notices.

## 13. danielmiessler (license not found)
- Actions:
	- [ ] Manually inspect `danielmiessler` for license or copyright notices.

---

**General Best Practices:**
- Always retain original copyright and license notices.
- Create a `THIRD_PARTY_NOTICES.md` or `NOTICE` file listing all third-party components and their licenses.
- When packaging or redistributing, include the corresponding license texts.
- For copyleft (AGPL/GPL) components, review deployment and distribution implications before integrating into networked services.
- When in doubt, consult legal counsel before integrating code with unclear or restrictive licenses.
