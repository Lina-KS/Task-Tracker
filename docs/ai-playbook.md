# My AI playbook after the course

## When I reach for AI first

I use AI early for bounded, verifiable work: turning a rubric into a checklist, locating files, reviewing a small diff, suggesting tests from an existing contract, or checking CI and Docker configuration. Here it helped compare the brief with the repository, review the Dockerfile, and organize evidence after I ran the commands. Code and tests, not the suggestion, remain the source of truth.

## When I do not reach for AI first

I start by reading when I do not understand the code, story, or failure. I slow down for security changes, destructive commands, unfamiliar infrastructure, production data, and scope decisions. I do not use AI to skip learning. I reproduce failures before asking for theories.

## My non-negotiables

- Never paste secrets, `.env` values, tokens, personal data, or production logs.
- Submit only changes I read, understand, and can explain.
- Never weaken tests, validation, TLS, permissions, or CI failure behavior for a green result.
- Treat configuration and execution as different evidence.
- Keep scope explicit and prefer small, reversible changes.
- Record uncertainty honestly. "Pending" is better than invented evidence.

## My review rules

Before editing, I read the README, relevant docs, tests, and nearby code. Afterward, I inspect the diff for scope drift, accidental data, unexplained lines, and unsafe defaults, then run focused checks and the full relevant suite. I grade AI findings against file or command evidence. Here that meant correcting the final layout to root `app/`, recording local Docker as blocked, and requiring real CI evidence.

## What I am still figuring out

I am still learning when dependencies need exact pins versus compatible ranges, and who owns updates on a team. I want team norms for recording AI review without making pull requests noisy. I also need more practice deciding when local Docker proof is essential versus when a clean CI runner is better evidence.

## Decision Card

| Situation | My first move | Rule |
|---|---|---|
| New feature | Read the story and tests; define what is out of scope. | AI may suggest options, but it does not choose scope. |
| Code review | Inspect the diff, then ask AI for missed risks. | Grade material comments against evidence. |
| Debugging | Reproduce the failure and capture the exact error. | Test one hypothesis at a time. |
| Infrastructure | Run the real build, start, and health commands. | Configuration is not execution evidence. |
| Never-paste | Stop before sharing credentials, personal data, `.env`, tokens, or production logs. | Use fictional, minimal examples. |
| One rule | Ask: "Can I explain and verify this?" | If no, I do not submit it. |
