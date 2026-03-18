# Turvablogi autoblog runbook

Goal: keep https://atlan-c.github.io/turvablogi/ alive with one practical Finnish post per day about local LLMs, home-lab AI hardware, and adjacent self-hosted workflows.

## Topic boundaries
Write about things like:
- local LLMs
- Ollama, llama.cpp, GGUF, quantization, context windows, RAG in practical use
- GPUs, VRAM, RAM, SSDs, power, thermals, used hardware, upgrade tradeoffs
- home-lab AI security when directly relevant to local models or hardware
- practical workflows for hobbyists and small self-hosters

Avoid:
- generic AI hype with no practical angle
- pure cloud-SaaS posts unless comparing against local setups
- copying the same structure/title shape as recent posts

## Daily workflow
1. Check the latest recent posts in `content/posts/` so the new one is not repetitive.
2. Do lightweight web research for one narrow topic that is timely *or* evergreen-useful.
3. Write one complete Finnish post as markdown in `content/posts/`.
4. Requirements:
   - frontmatter must include `title`, `date`, `draft: false`
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
- `Mitä X tarkoittaa harrastajalle?`
- `Kannattaako Y juuri nyt?`

Avoid repeating the same title skeleton two days in a row.

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
