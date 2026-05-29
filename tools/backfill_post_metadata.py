from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "content" / "posts"
FRONT_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.S)


def parse_frontmatter(text: str) -> tuple[list[str], dict[str, object], str]:
    m = FRONT_RE.match(text)
    if not m:
        raise ValueError("Invalid front matter")
    raw, body = m.group(1), m.group(2)
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
            items = []
            i += 1
            while i < len(lines) and lines[i].startswith("  - "):
                items.append(lines[i][4:].strip().strip('"'))
                i += 1
            fm[key] = items
            continue
        fm[key] = value.strip('"')
        i += 1
    return lines, fm, body


def slug(text: str) -> str:
    text = text.lower()
    text = text.replace("ä", "a").replace("ö", "o").replace("å", "a")
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")


def normalized_text(*parts: str) -> str:
    return " ".join(part.lower() for part in parts if part)


def title_and_intro(body: str, max_chars: int = 1800) -> str:
    return body[:max_chars]


def has_any(text: str, markers: list[str]) -> bool:
    return any(marker in text for marker in markers)


def infer_topic_family(path: Path, title: str, body: str, current: str) -> str:
    if current in {"openclaw", "llm-hardware"}:
        return current
    text = normalized_text(path.name, title, title_and_intro(body))
    openclaw_markers = [
        "openclaw", "heartbeat", "cron", "session", "sessions_", "subagent",
        "taskflow", "task flow", "memory.md", "models status", "agentturn",
    ]
    if has_any(text, openclaw_markers):
        return "openclaw"
    return "llm-hardware"


def infer_series(title: str, body: str, topic_family: str) -> list[str]:
    title_text = normalized_text(title)
    text = normalized_text(title, title_and_intro(body))
    if topic_family == "openclaw" or "openclaw" in text:
        return ["OpenClaw käytännössä"]
    if has_any(text, ["powershell", "helpdesk", "intune", "entra", "activedirectory", "active directory", "ryhmäkäytäntö", "group policy"]):
        return ["Windows IT ja AI"]
    if has_any(text, ["staattinen blogi", "tietoturva", "oauth", "ssh", "hallintapinta", "hyökkäyspinta", "kovennus", "privacy", "cisa"]) and not has_any(title_text, ["gpu", "vram", "ram", "ssd", "nvme", "pcie", "rtx", "arc a770", "ecc", "ai-rauta"]):
        return ["Tietoturvan minimikäytännöt"]
    if has_any(title_text, ["ai-rauta", "ai-raudan", "laitteisto", "gpu", "vram", "ram", "ssd", "nvme", "pcie", "rtx", "arc a770", "intel arc", "virtalähde", "jäähdytys", "jaahdytys", "ecc", "muistikaista", "kotilabra", "workstation", "prosessori", "cpu"]):
        return ["AI-kotilabra"]
    if has_any(text, ["paikallinen malli", "paikallinen llm", "llama.cpp", "ollama", "rag", "konteksti", "kv-cache", "kvantisointi", "pilvi-api", "pilvimalli"]):
        return ["Paikalliset LLM:t"]
    if has_any(text, ["ai-rauta", "ai-raudan", "laitteisto", "gpu", "vram", "ram", "ssd", "nvme", "pcie", "rtx", "arc a770", "intel arc", "virtalähde", "jäähdytys", "jaahdytys", "ecc", "muistikaista", "kotilabra", "workstation", "prosessori", "cpu"]):
        return ["AI-kotilabra"]
    return ["Paikalliset LLM:t"]


def infer_tags(title: str, body: str, topic_family: str, series: list[str]) -> list[str]:
    text = normalized_text(title, title_and_intro(body, max_chars=2600))
    tags: list[str] = []

    def add(tag: str):
        if tag not in tags:
            tags.append(tag)

    if topic_family == "openclaw" or "openclaw" in text:
        add("OpenClaw")
        add("Agents")
    if has_any(text, ["paikallinen", "llm", "ollama", "llama.cpp", "gguf", "rag", "kv-cache", "kvantisointi", "konteksti"]):
        add("Local LLM")
    if has_any(text, ["gpu", "vram", "rtx", "arc a770", "nvidia", "amd", "pcie x", "pcie-kaista"]):
        add("GPU")
    if has_any(text, ["ai-rauta", "rauta", "ram", "ssd", "nvme", "cpu", "prosessori", "muistikanava", "virtalahde", "jaahdytys", "jäähdytys", "apple silicon", "ecc", "pcie"]):
        add("Hardware")
    if has_any(text, ["windows", "powershell", "helpdesk", "intune", "entra", "activedirectory", "active directory"]):
        add("Windows")
    if has_any(text, ["powershell", "pwsh"]):
        add("PowerShell")
    if has_any(text, ["linux", "ubuntu", "debian", "fedora", "bash", "systemd"]):
        add("Linux")
    if has_any(text, ["tietoturva", "turvamalli", "hyökkäyspinta", "ssh", "oauth", "auth", "hallintapinta", "salasana", "cisa", "secure", "rajatut oikeudet"]):
        add("Security")
    if has_any(text, ["kotilabra", "kotipalvelin", "homelab", "itsehost", "self-host"]):
        add("Homelab")
    if has_any(text, ["automaatio", "automation", "cron", "heartbeat", "workflow", "task flow", "publish", "runbook"]):
        add("Automation")
    if has_any(text, ["vianrajaus", "troubleshoot", "hidas", "pullonkaula", "miksi", "mitä teet", "ongelma", "vika", "virhe", "status", "health"]):
        add("Troubleshooting")
    if has_any(text, ["signage", "näyttöseinä", "digital signage"]):
        add("Signage")

    if "AI-kotilabra" in series:
        add("Homelab")
    if "Paikalliset LLM:t" in series and "Local LLM" not in tags:
        add("Local LLM")
    if "Tietoturvan minimikäytännöt" in series and "Security" not in tags:
        add("Security")
    if "Windows IT ja AI" in series and "Windows" not in tags:
        add("Windows")

    if topic_family == "openclaw" and "Automation" not in tags:
        add("Automation")
    if topic_family == "llm-hardware" and "Hardware" not in tags:
        add("Hardware")

    if len(tags) < 2:
        if topic_family == "openclaw":
            add("OpenClaw")
            add("Agents")
        else:
            add("Local LLM")
            add("Hardware")

    return tags[:5]


def render_frontmatter(fm: dict[str, object]) -> str:
    ordered_keys = ["title", "date", "draft", "topic_family", "series", "tags"]
    lines: list[str] = []
    for key in ordered_keys:
        if key not in fm:
            continue
        value = fm[key]
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - \"{item}\"")
        elif isinstance(value, str) and value in {"true", "false"}:
            lines.append(f"{key}: {value}")
        else:
            lines.append(f"{key}: \"{value}\"")
    for key, value in fm.items():
        if key in ordered_keys:
            continue
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - \"{item}\"")
        elif isinstance(value, str) and value in {"true", "false"}:
            lines.append(f"{key}: {value}")
        else:
            lines.append(f"{key}: \"{value}\"")
    return "---\n" + "\n".join(lines) + "\n---\n"


def update_post(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    lines, fm, body = parse_frontmatter(text)
    title = str(fm.get("title", ""))
    topic_family = infer_topic_family(path, title, body, str(fm.get("topic_family", "")))
    series = infer_series(title, body, topic_family)
    tags = infer_tags(title, body, topic_family, series)

    changed = False
    if fm.get("topic_family") != topic_family:
        fm["topic_family"] = topic_family
        changed = True
    if fm.get("series") != series:
        fm["series"] = series
        changed = True
    if fm.get("tags") != tags:
        fm["tags"] = tags
        changed = True

    if changed:
        rendered = render_frontmatter(fm) + body.lstrip("\n")
        path.write_text(rendered, encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    changed = 0
    seen = 0
    for path in sorted(POSTS_DIR.glob("*.md")):
        if args.limit and seen >= args.limit:
            break
        seen += 1
        if args.dry_run:
            text = path.read_text(encoding="utf-8")
            _, fm, body = parse_frontmatter(text)
            title = str(fm.get("title", ""))
            topic_family = infer_topic_family(path, title, body, str(fm.get("topic_family", "")))
            series = infer_series(title, body, topic_family)
            tags = infer_tags(title, body, topic_family, series)
            needs_change = fm.get("topic_family") != topic_family or fm.get("series") != series or fm.get("tags") != tags
            if needs_change:
                changed += 1
                print(f"{path.name}: {topic_family} | {series[0]} | {', '.join(tags)}")
            continue
        if update_post(path):
            changed += 1
    print(f"updated {changed} posts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
