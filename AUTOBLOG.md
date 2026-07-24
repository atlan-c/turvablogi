# Turvablogi autoblog runbook

Goal: keep https://atlan-c.github.io/turvablogi/ alive with one practical Finnish post per day. The current phase focuses on AI models and agent work. Earlier local-LLM, AI hardware, OpenClaw, and homelab posts remain available in the archive.

## Topic boundaries
Write about things like:
- new AI models when the angle is practical instead of hype-driven
- model evaluation for coding, tool use, structured output, RAG, and agent work
- agent architecture, model routing, tool schemas, MCP, and provider abstraction
- practical workflows for hobbyists and small self-hosters who want useful agent systems
- local LLMs, AI hardware, and OpenClaw only when they support the new model-and-agent angle directly

Avoid:
- generic AI hype with no practical angle
- pure cloud-SaaS posts unless comparing against local setups
- copying the same structure/title shape as recent posts

## Daily workflow
1. Check the latest recent posts in `content/posts/` so the new one is not repetitive.
2. Stay inside the current phase:
   - new phase posts must include `phase: "new-era"`
   - prefer `topic_family: "ai-models"` for the normal daily flow
   - use `data/editorial_state.json` as the recent-style memory, not as an old two-family alternation lock
   - older `openclaw` or `llm-hardware` families belong to the archive unless a human explicitly asks for a special exception
3. Do lightweight web research for one narrow topic that is timely *or* evergreen-useful within the current phase.
4. Write one complete Finnish post as markdown in `content/posts/`.
4. Requirements:
   - frontmatter must include `title`, `date`, `draft: false`, `topic_family`
   - new phase posts must also include `phase: "new-era"`
   - `topic_family` should normally be `ai-models` in the new phase
   - body length should clearly exceed the repo minimum
   - include `## Lähteet`
   - include at least 2 source URLs
   - make it practical and readable, not hypey
   - do not publish two different posts on the same calendar day unless a human explicitly asks for a one-off exception
   - if a human explicitly asks to seed the phase with multiple same-day posts, mark each seeded post with `allow_same_day: true`
5. Run the repo checks:
   - `python3 tools/pre_publish_check.py --staged` after staging the post
   - if needed, run `hugo --minify` if Hugo exists
6. If checks pass, commit and push to `main`.
7. GitHub Actions will publish automatically.

## Title/style rules
Prefer concrete titles such as:
- `Paikallinen LLM käytännössä: ...`
- `AI-rauta kotilabrassa: ...`
- `OpenClaw käytännössä: ...`
- `Mitä X tarkoittaa harrastajalle?`
- `Kannattaako Y juuri nyt?`

Avoid repeating the same title skeleton two days in a row.
Avoid writing three posts in a row that answer the exact same question from slightly different angles.

## Quality bar
The post should answer one practical question clearly.
Good angles:
- what matters in real use
- what beginners often misunderstand
- what is worth buying / not buying
- what bottleneck matters first
- what setup gives the best value for a hobbyist

## Publish commands
From repo root:

```bash
git status -sb
```

Create/edit the post, then:

```bash
git add content/posts/*.md
python3 tools/pre_publish_check.py --staged
```

If checks pass, also update editorial state and publish:

```bash
git add data/editorial_state.json || true
git commit -m "Add Finnish AI blog update post"
git pull --rebase origin main
git push origin main
python3 tools/pre_publish_check.py --update-state || true
```

If `git push` fails because credentials are missing, stop and report the failure in the session instead of looping.

## Fallback behavior
- If research quality is weak that day, write an evergreen practical explainer instead of forcing "news".
- If sources are too thin, skip publishing and report why.
- Never mass-produce multiple posts in one run unless a human explicitly asks to seed the current phase.
- Never publish two separate posts for the same calendar day unless the human explicitly requests an exception.
- One good post beats five thin ones.
