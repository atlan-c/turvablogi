# Turvablogi autoblog runbook

Goal: keep https://atlan-c.github.io/turvablogi/ alive with one practical Finnish post per day. The blog now alternates between two topic families: (A) local LLMs / AI hardware and (B) OpenClaw practical usage, tuning, automation patterns, and self-hosted operating practices.

## Topic boundaries
Write about things like:
- local LLMs
- Ollama, llama.cpp, GGUF, quantization, context windows, RAG in practical use
- GPUs, VRAM, RAM, SSDs, power, thermals, used hardware, upgrade tradeoffs
- home-lab AI security when directly relevant to local models or hardware
- practical workflows for hobbyists and small self-hosters
- OpenClaw practical use: heartbeat vs cron, sessions, delegation, topic/thread isolation, safe automation boundaries, tuning, maintenance, troubleshooting, and workflow design

Avoid:
- generic AI hype with no practical angle
- pure cloud-SaaS posts unless comparing against local setups
- copying the same structure/title shape as recent posts

## Daily workflow
1. Check the latest recent posts in `content/posts/` so the new one is not repetitive.
2. Determine which topic family is next and alternate strictly day by day:
   - prefer `data/editorial_state.json` and its `last_topic_family` field as the source of truth
   - if `last_topic_family` is `llm-hardware`, the next post must be `openclaw`
   - if `last_topic_family` is `openclaw`, the next post must be `llm-hardware`
   - only if the field is missing, fall back to conservative inference from the latest post's title, slug, body, and sources
3. Do lightweight web research for one narrow topic that is timely *or* evergreen-useful within the required family.
4. Write one complete Finnish post as markdown in `content/posts/`.
4. Requirements:
   - frontmatter must include `title`, `date`, `draft: false`, `topic_family`
   - `topic_family` must be exactly `openclaw` or `llm-hardware`
   - body length should clearly exceed the repo minimum
   - include `## Lähteet`
   - include at least 2 source URLs
   - make it practical and readable, not hypey
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
Avoid repeating the same topic family two days in a row.

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
- Never mass-produce multiple posts in one run.
- One good post beats five thin ones.
