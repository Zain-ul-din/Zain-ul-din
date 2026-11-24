"""Build the profile README and its SVG cards.

Edit CONTENT below, then run:  python3 scripts/build.py
It rewrites assets/*-light.svg and *-dark.svg and the block between the profile markers in readme.md.
Every card's text is also its alt text, so screen readers, search and AI screeners read it.
"""

from __future__ import annotations

import hashlib
import pathlib
import re
import textwrap
from html import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

CONTENT = {
    "name": "Zain Ul Din",
    "role": "FULLSTACK PRODUCT ENGINEER  ·  APPLIED AI",
    "pitch": "I take products from idea to shipped: frontend, backend, AI and deploy.",
    "meta": "REMOTE  ·  360+ ★ ON GITHUB",
    "links": [
        ("portfolio", "Portfolio", "https://zainuldin.dev"),
        ("linkedin", "LinkedIn", "https://www.linkedin.com/in/zain-ul-din/"),
        ("writing", "Writing", "https://zainuldin.dev/blog"),
        ("email", "Email", "mailto:zainuldin.dev@gmail.com"),
    ],
    "projects": [
        {
            "label": "OPEN SOURCE  ·  TYPESCRIPT  ·  PYTHON",
            "badge": ("star", "250 ★"),
            "title": "WhatsApp AI Bot",
            "text": "Self-hostable bot for 5 model providers, with a PII guard that keeps personal data away from the model.",
            "cta": "View code",
            "url": "https://github.com/Zain-ul-din/whatsapp-agents",
        },
        {
            "label": "OPEN SOURCE  ·  AI AGENT",
            "badge": ("plain", "TESTED IN CI"),
            "title": "Background Job Agent",
            "text": "Watches job channels, classifies postings and sends role-matched applications, on durable Inngest workflows.",
            "cta": "View code",
            "url": "https://github.com/Zain-ul-din/background-job-agent",
        },
        {
            "label": "OPEN SOURCE  ·  NEXT.JS  ·  AI",
            "badge": ("plain", "32 EVAL CASES"),
            "title": "Levaina",
            "text": "AI gut-care coach that logs meals and symptoms from chat, remembers what matters, and is tested like code.",
            "cta": "View code",
            "url": "https://github.com/Zain-ul-din/levaina",
        },
        {
            "label": "OPEN SOURCE  ·  REACT  ·  CHAKRA UI",
            "badge": ("plain", "ADMIN PANEL"),
            "title": "BAP Admin",
            "text": "Admin dashboard for a private ambulance service: organizations, admins, ambulance fleet and CSV imports.",
            "cta": "View code",
            "url": "https://github.com/Zain-ul-din/bap-admin",
        },
    ],
    "stack": [
        ("LANGUAGES", "TypeScript, JavaScript, Python, SQL, C#"),
        ("FRONTEND", "React, Next.js, Tailwind CSS"),
        ("BACKEND", "Node.js, Express, FastAPI, PostgreSQL, Supabase, MongoDB"),
        ("AI", "RAG, agents and tool calling, MCP, LangChain, LangGraph, evals, PII guardrails"),
        ("DEVOPS", "Docker, GitHub Actions, Linux (Ubuntu), Vercel"),
    ],
    "posts": [
        ("SEP 2026", "The True Cost of AI", "https://zainuldin.dev/blog/the-true-cost-of-ai"),
        ("JUL 2026", "AI gave me speed. Skills gave me consistency.", "https://zainuldin.dev/blog/ai-speed-skills-consistency"),
    ],
    "footer_title": "Got a project or role in mind?",
    "footer_text": "Say hi at zainuldin.dev or zainuldin.dev@gmail.com",
}

# Colors from GitHub's Primer themes, so the cards sit flush on the profile page in light and dark.
# Type from zainuldin.dev: a serif display face, mono labels, a plain sans for body text.
PALETTES = {
    "light": dict(bg="#ffffff", stroke="#d1d9e0", fg="#1f2328", muted="#59636e", rule="#d1d9e0",
                  live="#1a7f37", star="#9a6700", link="#0969da", pill="#f6f8fa", pill_stroke="#d1d9e0"),
    "dark": dict(bg="#0d1117", stroke="#3d444d", fg="#f0f6fc", muted="#9198a1", rule="#3d444d",
                 live="#3fb950", star="#d29922", link="#4493f8", pill="#212830", pill_stroke="#3d444d"),
}


def style(theme: str) -> str:
    c = PALETTES[theme]
    return f"""<style>
  .bg {{ fill: {c['bg']}; stroke: {c['stroke']}; }}
  .fg {{ fill: {c['fg']}; }}
  .muted {{ fill: {c['muted']}; }}
  .rule {{ stroke: {c['rule']}; }}
  .live {{ fill: {c['live']}; }}
  .star {{ fill: {c['star']}; }}
  .link {{ fill: {c['link']}; }}
  .pill {{ fill: {c['pill']}; stroke: {c['pill_stroke']}; }}
  .serif {{ font-family: 'Cooper Lt BT', 'Cooper Light', Georgia, 'Times New Roman', serif; }}
  .sans {{ font-family: 'Schibsted Grotesk', system-ui, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif; }}
  .mono {{ font-family: 'Geist Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; letter-spacing: .08em; }}
</style>"""


def svg(w: int, h: int, body: str, title: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>%%STYLE%%{body}</svg>\n')


def lines(x: int, y: int, text: str, width: int, size: float, cls: str, gap: float) -> tuple[str, float]:
    out = []
    for i, line in enumerate(textwrap.wrap(text, width, break_on_hyphens=False)):
        out.append(f'<text x="{x}" y="{y + i * gap:.1f}" font-size="{size}" class="{cls}">{escape(line)}</text>')
    return "".join(out), y + (len(out) - 1) * gap


def header(c) -> str:
    body = (
        '<rect x="6" y="6" width="818" height="208" rx="16" class="bg"/>'
        f'<text x="40" y="54" font-size="12" class="mono muted">{escape(c["role"])}</text>'
        f'<text x="38" y="112" font-size="50" class="serif fg">{escape(c["name"])}</text>'
        f'<text x="40" y="152" font-size="18" class="sans fg">{escape(c["pitch"])}</text>'
        '<line x1="40" y1="172" x2="790" y2="172" class="rule"/>'
        f'<text x="40" y="196" font-size="11" class="mono muted">{escape(c["meta"])}</text>'
    )
    return svg(830, 220, body, f'{c["name"]}, {c["role"]}. {c["pitch"]}')


def button(label: str) -> str:
    body = (
        '<rect x="6" y="4" width="195" height="46" rx="23" class="pill"/>'
        f'<text x="103" y="32" font-size="12" text-anchor="middle" class="mono fg">{escape(label.upper())}  ↗</text>'
    )
    return svg(207, 54, body, label)


def section(label: str) -> str:
    body = (f'<text x="8" y="30" font-size="12" class="mono muted">{escape(label)}</text>'
            '<line x1="120" y1="26" x2="822" y2="26" class="rule"/>')
    return svg(830, 44, body, label.title())


def project(p) -> str:
    kind, badge = p["badge"]
    if kind == "live":
        badge_svg = (f'<circle cx="{392 - 7.6 * len(badge) - 12}" cy="38" r="4" class="live"/>'
                     f'<text x="392" y="42" font-size="11" text-anchor="end" class="mono live">{escape(badge)}</text>')
    else:
        badge_svg = f'<text x="392" y="42" font-size="11" text-anchor="end" class="mono {"star" if kind == "star" else "muted"}">{escape(badge)}</text>'
    desc, last = lines(26, 110, p["text"], 50, 14, "sans muted", 20)
    body = (
        '<rect x="6" y="6" width="403" height="196" rx="14" class="bg"/>'
        f'<text x="26" y="42" font-size="10.5" class="mono muted">{escape(p["label"])}</text>{badge_svg}'
        f'<text x="25" y="82" font-size="25" class="serif fg">{escape(p["title"])}</text>{desc}'
        f'<text x="26" y="184" font-size="11" class="mono link">{escape(p["cta"].upper())}  →</text>'
    )
    return svg(415, 208, body, f'{p["title"]}: {p["text"]} ({p["label"].replace("  ·  ", ", ").lower()})')


def stack(rows) -> str:
    parts = ['<rect x="6" y="6" width="818" height="{h}" rx="16" class="bg"/>']
    y = 50
    for label, value in rows:
        parts.append(f'<text x="40" y="{y}" font-size="11" class="mono muted">{escape(label)}</text>')
        parts.append(f'<text x="170" y="{y}" font-size="15" class="sans fg">{escape(value)}</text>')
        y += 36
    h = y - 18
    body = "".join(parts).replace("{h}", str(h))
    return svg(830, h + 12, body, "Stack. " + "; ".join(f"{a.title()}: {b}" for a, b in rows))


def post(date: str, title: str) -> str:
    t, _ = lines(26, 76, title, 34, 20, "serif fg", 26)
    body = (
        '<rect x="6" y="6" width="403" height="146" rx="14" class="bg"/>'
        f'<text x="26" y="40" font-size="10.5" class="mono muted">{escape(date)}</text>{t}'
        '<text x="26" y="130" font-size="11" class="mono link">READ  →</text>'
    )
    return svg(415, 158, body, f"{title} ({date.title()})")


def footer(c) -> str:
    body = (
        '<rect x="6" y="6" width="818" height="128" rx="16" class="bg"/>'
        f'<text x="415" y="66" font-size="30" text-anchor="middle" class="serif fg">{escape(c["footer_title"])}</text>'
        f'<text x="415" y="102" font-size="15" text-anchor="middle" class="sans muted">{escape(c["footer_text"])}</text>'
    )
    return svg(830, 140, body, f'{c["footer_title"]} {c["footer_text"]}')


def img(src: str, alt: str, width: str) -> str:
    """Light and dark versions; GitHub picks the one that matches the viewer's GitHub theme."""
    stem = src.removesuffix(".svg")
    dark, light = f"{stem}-dark.svg", f"{stem}-light.svg"
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/{dark}?v={version(dark)}">'
            f'<img src="./assets/{light}?v={version(light)}" alt="{escape(alt)}" width="{width}" align="top"></picture>')


def version(name: str) -> str:
    """Short content hash, so a changed card gets a new URL and browsers skip their cached copy."""
    return hashlib.sha256((ASSETS / name).read_bytes()).hexdigest()[:8]


def build() -> None:
    c = CONTENT
    ASSETS.mkdir(exist_ok=True)
    files = {"header.svg": header(c), "section-shipped.svg": section("SHIPPED"),
             "section-stack.svg": section("STACK"), "section-writing.svg": section("WRITING"),
             "stack.svg": stack(c["stack"]), "footer.svg": footer(c)}
    for key, label, _ in c["links"]:
        files[f"link-{key}.svg"] = button(label)
    for i, p in enumerate(c["projects"], 1):
        files[f"project-{i}.svg"] = project(p)
    for i, (date, title, _) in enumerate(c["posts"], 1):
        files[f"post-{i}.svg"] = post(date, title)
    for old in ASSETS.glob("*.svg"):
        old.unlink()
    for name, text in files.items():
        for theme in PALETTES:
            (ASSETS / name.replace(".svg", f"-{theme}.svg")).write_text(text.replace("%%STYLE%%", style(theme)))

    alt = lambda name: re.search(r'aria-label="([^"]*)"', files[name]).group(1)  # noqa: E731
    pairs = lambda items: "\n".join("".join(items[i:i + 2]) for i in range(0, len(items), 2))  # noqa: E731
    projects = [f'<a href="{p["url"]}">{img(f"project-{i}.svg", alt(f"project-{i}.svg"), "50%")}</a>'
                for i, p in enumerate(c["projects"], 1)]
    posts = [f'<a href="{u}">{img(f"post-{i}.svg", alt(f"post-{i}.svg"), "50%")}</a>'
             for i, (_, _, u) in enumerate(c["posts"], 1)]
    links = "".join(f'<a href="{u}">{img(f"link-{k}.svg", label, "25%")}</a>' for k, label, u in c["links"])
    block = "\n".join([
        "<!-- profile:start -->",
        '<div align="center">',
        img("header.svg", alt("header.svg"), "100%"),
        links,
        img("section-shipped.svg", "Shipped", "100%"),
        pairs(projects),
        img("section-stack.svg", "Stack", "100%"),
        img("stack.svg", alt("stack.svg"), "100%"),
        img("section-writing.svg", "Writing", "100%"),
        pairs(posts),
        f'<a href="https://zainuldin.dev">{img("footer.svg", alt("footer.svg"), "100%")}</a>',
        "</div>",
        "<!-- profile:end -->",
    ])
    readme = ROOT / "readme.md"
    old = readme.read_text() if readme.exists() else ""
    if "<!-- profile:start -->" in old:
        new = re.sub(r"<!-- profile:start -->.*?<!-- profile:end -->", lambda _: block, old, flags=re.S)
    else:
        new = block + "\n\n" + TAIL
    readme.write_text(new)
    print(f"wrote {len(files) * len(PALETTES)} SVGs and readme.md")


TAIL = """<p align="center"><sub>
<a href="https://www.buymeacoffee.com/zainuldin">Buy me a coffee</a> · <a href="https://github.com/Safouene1/support-palestine-banner">#StandWithPalestine</a>
</sub></p>
"""

if __name__ == "__main__":
    build()
