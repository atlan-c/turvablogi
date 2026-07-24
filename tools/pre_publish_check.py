from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "content" / "posts"
STATE_PATH = ROOT / "data" / "editorial_state.json"

URL_RE = re.compile(r"https?://[^\s)]+")
FRONT_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.S)
ALLOWED_TOPIC_FAMILIES = {"openclaw", "llm-hardware", "ai-models"}


@dataclass
class ParsedPost:
    path: Path
    frontmatter: dict
    body: str


def run_git(args: list[str]) -> str:
    p = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    return p.stdout.strip()


def staged_post_files() -> list[Path]:
    out = run_git(["diff", "--cached", "--name-only"])
    files = []
    for line in out.splitlines():
        if line.startswith("content/posts/") and line.endswith(".md"):
            files.append(ROOT / line)
    return files


def parse_frontmatter(text: str) -> tuple[dict, str]:
    m = FRONT_RE.match(text)
    if not m:
        raise ValueError("Frontmatter puuttuu tai on virheellinen (--- ... ---)")
    raw, body = m.group(1), m.group(2).strip()
    lines = raw.splitlines()
    fm: dict[str, object] = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or ":" not in line:
            i += 1
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "":
            items: list[str] = []
            i += 1
            while i < len(lines) and lines[i].startswith("  - "):
                items.append(lines[i][4:].strip().strip('"'))
                i += 1
            fm[key] = items
            continue
        fm[key] = value.strip().strip('"')
        i += 1
    return fm, body


def parse_post(path: Path) -> ParsedPost:
    txt = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(txt)
    return ParsedPost(path=path, frontmatter=fm, body=body)


def first_paragraph(body: str) -> str:
    parts = [p.strip() for p in body.split("\n\n") if p.strip()]
    return parts[0] if parts else ""


def title_shape(title: str) -> str:
    t = re.sub(r"\d+", "", title.lower())
    t = re.sub(r"[^a-zåäö\s-]", "", t)
    words = [w for w in t.split() if w not in {"ja", "tai", "on", "the", "ai"}]
    return " ".join(words[:4]).strip()


def recent_posts(limit: int = 8) -> list[Path]:
    arr = sorted(POSTS_DIR.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    return arr[:limit]


def post_date_day(post: ParsedPost) -> str:
    raw = str(post.frontmatter.get("date", "")).strip()
    if not raw:
        return ""
    return raw.split("T", 1)[0].split(" ", 1)[0]


def validate_sources(body: str) -> tuple[bool, str]:
    if "## Lähteet" not in body and "### Lähteet" not in body:
        return False, "Osio 'Lähteet' puuttuu"
    urls = URL_RE.findall(body)
    if len(urls) < 2:
        return False, "Lähteitä pitää olla vähintään 2 URLia"
    return True, ""


def is_draft(post: ParsedPost) -> bool:
    return str(post.frontmatter.get("draft", "")).lower() in {"true", "1", "yes"}


def post_phase(post: ParsedPost) -> str:
    return str(post.frontmatter.get("phase", "")).strip()


def validate_post(post: ParsedPost) -> list[str]:
    errors: list[str] = []
    fm = post.frontmatter
    for key in ["title", "date", "draft", "topic_family"]:
        if key not in fm:
            errors.append(f"Frontmatter-kenttä puuttuu: {key}")

    draft_value = str(fm.get("draft", "")).lower()
    if draft_value not in {"true", "false", "0", "1", "no", "yes"}:
        errors.append("draft pitää olla true tai false")

    if str(fm.get("topic_family", "")) not in ALLOWED_TOPIC_FAMILIES:
        allowed = ", ".join(sorted(ALLOWED_TOPIC_FAMILIES))
        errors.append(f"topic_family pitää olla yksi seuraavista: {allowed}")

    tags = fm.get("tags")
    if tags:
        if not isinstance(tags, list):
            errors.append("tags pitää olla YAML-lista")
        elif not (2 <= len(tags) <= 5):
            errors.append("tageja pitää olla 2-5")

    series = fm.get("series")
    if series and not isinstance(series, list):
        errors.append("series pitää olla YAML-lista")

    if is_draft(post):
        return errors

    if len(post.body) < 450:
        errors.append("Sisältö on liian lyhyt (min 450 merkkiä)")

    ok, msg = validate_sources(post.body)
    if not ok:
        errors.append(msg)

    state = load_state()
    cur_family = infer_topic_family(post)
    last_family = state.get("last_topic_family")
    last_post = state.get("last_post")
    cur_relpath = str(post.path.relative_to(ROOT))
    same_family_allowed = post_phase(post) == "new-era"
    if last_family and cur_family == last_family and last_post != cur_relpath and not same_family_allowed:
        errors.append("Aiheperhe toistaa edellisen postauksen; vuorottelun pitää vaihtua")

    cur_day = post_date_day(post)
    if cur_day:
        for old_path in POSTS_DIR.glob("*.md"):
            if old_path.resolve() == post.path.resolve():
                continue
            try:
                old_post = parse_post(old_path)
            except Exception:
                continue
            if post_date_day(old_post) == cur_day and not is_draft(old_post):
                same_day_allowed = str(post.frontmatter.get("allow_same_day", "")).lower() in {"true", "1", "yes"}
                if same_day_allowed:
                    break
                errors.append(
                    f"Kalenteripäivälle {cur_day} on jo olemassa postaus ({old_path.name}); toinen saman päivän julkaisu vaatii erillisen poikkeuksen"
                )
                break

    cur_title_shape = title_shape(str(fm.get("title", "")))
    cur_intro = first_paragraph(post.body)
    for old in recent_posts(limit=6):
        if old.resolve() == post.path.resolve():
            continue
        try:
            op = parse_post(old)
        except Exception:
            continue
        if is_draft(op):
            continue
        if title_shape(str(op.frontmatter.get("title", ""))) == cur_title_shape and cur_title_shape:
            errors.append("Otsikkorakenne toistaa liian tarkasti viimeaikaisen postauksen")
            break
        old_intro = first_paragraph(op.body)
        if cur_intro and old_intro:
            sim = SequenceMatcher(None, cur_intro[:280], old_intro[:280]).ratio()
            if sim > 0.86:
                errors.append("Aloituskappale muistuttaa liikaa viimeaikaista postausta")
                break

    return errors


def extract_sources_domains(body: str) -> list[str]:
    domains = []
    for u in URL_RE.findall(body):
        m = re.match(r"https?://([^/]+)/?", u)
        if m:
            domains.append(m.group(1).lower())
    return sorted(set(domains))


def infer_topic_family(post: ParsedPost) -> str:
    explicit = str(post.frontmatter.get("topic_family", "")).strip()
    if explicit in ALLOWED_TOPIC_FAMILIES:
        return explicit

    text = " ".join(
        [
            post.path.name.lower(),
            str(post.frontmatter.get("title", "")).lower(),
            post.body.lower(),
            " ".join(extract_sources_domains(post.body)),
        ]
    )
    openclaw_markers = [
        "openclaw",
        "heartbeat",
        "cron",
        "session",
        "topic/thread",
        "docs.openclaw.ai",
    ]
    if any(marker in text for marker in openclaw_markers):
        return "openclaw"
    ai_models_markers = [
        "agenttiarkkitehtuuri",
        "structured output",
        "tool calling",
        "function calling",
        "mcp",
        "tekoälymalli",
        "tekoalymalli",
    ]
    if any(marker in text for marker in ai_models_markers):
        return "ai-models"
    return "llm-hardware"


def load_state() -> dict:
    if not STATE_PATH.exists():
        return {}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def update_state_from_post(post: ParsedPost):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    state = load_state()

    intro = first_paragraph(post.body)
    state.update(
        {
            "last_post": str(post.path.relative_to(ROOT)),
            "last_title": post.frontmatter.get("title", ""),
            "last_title_shape": title_shape(str(post.frontmatter.get("title", ""))),
            "last_topic_family": infer_topic_family(post),
            "last_intro_hash": hashlib.sha256(intro.encode("utf-8", errors="ignore")).hexdigest() if intro else "",
            "last_sources_domains": extract_sources_domains(post.body),
            "updated_at": run_git(["log", "-1", "--format=%cI"]) or "",
        }
    )
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def latest_post() -> Path | None:
    posts = recent_posts(limit=1)
    return posts[0] if posts else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--staged", action="store_true")
    ap.add_argument("--update-state", action="store_true")
    args = ap.parse_args()

    if args.staged:
        files = staged_post_files()
        if not files:
            print("No staged post files. OK")
            return 0
        all_errors: list[str] = []
        for f in files:
            p = parse_post(f)
            errs = validate_post(p)
            for e in errs:
                all_errors.append(f"{f.name}: {e}")
        if all_errors:
            print("PRE-PUBLISH CHECK FAILED")
            for e in all_errors:
                print("-", e)
            return 1
        print("PRE-PUBLISH CHECK OK")
        return 0

    if args.update_state:
        lp = latest_post()
        if not lp:
            print("No posts found")
            return 0
        p = parse_post(lp)
        update_state_from_post(p)
        print(f"State updated from {lp.name}")
        return 0

    print("No action")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
