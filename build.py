"""Build the static site into _site/.

Each tool lives in src/tools/<slug>.html. The file starts with a JSON
metadata block inside an HTML comment, followed by the tool's body HTML:

<!--meta
{"title": "...", "description": "...", "category": "...", "order": 10}
-->
<section>...</section>
"""
import json
import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "_site"
BASE_URL = "https://ash2700.github.io/tools-site"
SITE_NAME = "生活小工具"

META_RE = re.compile(r"^\s*<!--meta\s*(\{.*?\})\s*-->\s*", re.S)


def load_tools():
    tools = []
    for path in sorted((SRC / "tools").glob("*.html")):
        text = path.read_text(encoding="utf-8")
        m = META_RE.match(text)
        if not m:
            raise SystemExit(f"missing meta block: {path}")
        meta = json.loads(m.group(1))
        meta["slug"] = path.stem
        meta["body"] = text[m.end():]
        tools.append(meta)
    tools.sort(key=lambda t: (t.get("order", 100), t["slug"]))
    return tools


def render(layout, *, title, description, canonical, body, extra_head=""):
    return (
        layout.replace("{{title}}", title)
        .replace("{{description}}", description)
        .replace("{{canonical}}", canonical)
        .replace("{{site_name}}", SITE_NAME)
        .replace("{{extra_head}}", extra_head)
        .replace("{{body}}", body)
        .replace("{{year}}", str(date.today().year))
    )


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SRC / "static", OUT)
    layout = (SRC / "layout.html").read_text(encoding="utf-8")
    tools = load_tools()
    urls = [f"{BASE_URL}/"]

    for t in tools:
        url = f"{BASE_URL}/{t['slug']}/"
        urls.append(url)
        ld = {
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": t["title"],
            "description": t["description"],
            "url": url,
            "applicationCategory": "UtilityApplication",
            "operatingSystem": "Any",
            "inLanguage": "zh-TW",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "TWD"},
        }
        extra = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>'
        body = (
            f'<nav class="crumb"><a href="../">← 所有工具</a></nav>'
            f"<h1>{t['title']}</h1><p class=\"lead\">{t['description']}</p>{t['body']}"
        )
        page = render(layout, title=f"{t['title']}｜{SITE_NAME}", description=t["description"],
                      canonical=url, body=body, extra_head=extra)
        (OUT / t["slug"]).mkdir()
        (OUT / t["slug"] / "index.html").write_text(page, encoding="utf-8")

    groups = {}
    for t in tools:
        groups.setdefault(t.get("category", "其他"), []).append(t)
    cards = []
    for cat, items in groups.items():
        links = "".join(
            f'<a class="card" href="{t["slug"]}/"><strong>{t["title"]}</strong><span>{t["description"]}</span></a>'
            for t in items
        )
        cards.append(f"<h2>{cat}</h2><div class=\"grid\">{links}</div>")
    home = render(layout, title=f"{SITE_NAME}｜免費線上計算機與換算工具",
                  description="免費、免註冊的線上計算工具：房貸試算、複利、坪數換算、民國年換算、日期天數、折扣百分比等，手機也好用。",
                  canonical=f"{BASE_URL}/",
                  body=f"<h1>{SITE_NAME}</h1><p class=\"lead\">免費、免註冊、資料不上傳，在瀏覽器裡直接算。</p>{''.join(cards)}")
    (OUT / "index.html").write_text(home, encoding="utf-8")

    today = date.today().isoformat()
    sitemap = "".join(f"<url><loc>{u}</loc><lastmod>{today}</lastmod></url>" for u in urls)
    (OUT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sitemap}</urlset>',
        encoding="utf-8")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n", encoding="utf-8")
    print(f"built {len(tools)} tools -> {OUT}")


if __name__ == "__main__":
    main()
