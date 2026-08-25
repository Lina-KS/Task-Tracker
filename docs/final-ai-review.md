# Final AI review and ownership evidence

Reviewed on 2026-08-14 from branch `final-project`.

## AGENTS.md guardrails

- Repo-specific FastAPI, static frontend, JSON storage, and pytest commands included: **yes**
- Docs-first/read-first rule included: **yes**
- Unexpected `app/` and `frontend/` edits rule included: **yes**
- Duplicate-project and secret restrictions included: **yes**

## AI code review mini-log

| AI comment | Grade | Reason and decision |
|---|---|---|
| Run Docker as a dedicated non-root user. | **Useful** | Kept: `Dockerfile` creates and switches to `appuser`. |
| Install curl only for the image health check. | **Noise** | Rejected: Python's existing `urllib.request` performs the check without another package. |
| Keep `backend/app/` because it already works. | **Wrong after clarification** | Corrected when the final requirement explicitly specified root `app/`; configs and docs were updated together. |

## AI security mini-review

| Finding | File evidence | Grade | Decision |
|---|---|---|---|
| Dependencies have no version bounds. | `requirements.txt` | **Valid** | Recorded as dependency-drift risk; not expanded during layout cleanup. |
| Local `http://` URLs disable external TLS. | `frontend/index.html`, `Dockerfile`, CI | **False Positive** | URLs are localhost-only development and health checks; no `verify=False` exists. |
| `.env` text means a secret is copied. | `.gitignore`, `.dockerignore` | **Noise** | `.env` files are ignored and excluded from the image. |

## Manual security check

I checked the tracked source/docs for private-key, GitHub-token, OpenAI-key, and AWS-key patterns and found none. I also inspected Docker context exclusions and confirmed that no local environment file is required by the app.

## One AI output I rejected or corrected

I originally rejected moving `backend/app/` because the earlier repository worked from that path. The final submission requirement later made root `app/` explicit, so I corrected that decision: moved the same application without adding features, updated storage to `app/data/`, and changed CI, Docker, README, and guardrails consistently. This protected-code change is a documentation-supported layout correction.

The earlier Activity Log had also expanded into an unapproved restorable-deletion feature. That scope drift was corrected before this layout pass: deletion is permanent while the `deleted` activity event remains, and the restore endpoint/UI/tests were removed.

## Three AI usage rules

1. **Never paste:** credentials, `.env` values, tokens, production logs, or real personal/customer data.
2. **Always verify:** inspect the diff and run the relevant test, command, endpoint, or manual check.
3. **Record contributions:** grade material findings and document corrections or rejections with evidence.

## Ownership statement

I am comfortable submitting this repository because I reviewed the final paths, changed no product behavior during cleanup, and can explain every retained configuration choice. I verified claims against files and commands instead of treating AI output as proof. I recorded the root-layout correction and its protected-code impact explicitly. No secrets or real personal/customer data were provided or committed.
