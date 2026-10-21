# tools-site

Free Traditional Chinese (zh-TW) calculator/converter site for Taiwan users, monetized later by ads.
Live at https://ash2700.github.io/tools-site/ — deployed by `.github/workflows/deploy.yml` on every push to `main`.

## Adding a tool
1. Create `src/tools/<slug>.html`: a `<!--meta {...} -->` JSON block (title, description, category, order), then body HTML + inline `<script>`.
   Copy an existing tool (e.g. `discount.html`) for structure and CSS classes: `.panel`, `.row`, `.result`, `.big`, `.explain`.
2. Helpers from `src/static/common.js`: `fmt(n, digits)`, `num(id)`, `bindAll(fn)`.
3. Every tool needs an `.explain` section with the formula/basis — this is what makes pages rank and pass ad review.
4. `python3 build.py` → outputs `_site/` with index, sitemap.xml, robots.txt. Never commit `_site/`.

## Rules
- All text in Traditional Chinese, Taiwan usage (坪、台斤、民國年、元).
- Pure client-side; no external requests, no tracking, no user data leaves the browser.
- Prefer tools whose rules are stable. Avoid tools that depend on rates or laws that change yearly (tax brackets, electricity prices,
  labor insurance) unless you verify current official numbers with a web search and cite the source year on the page.
- No duplicate tools: check `src/tools/` first. Don't change existing slugs (URLs are indexed by Google).
- Before pushing: build, then load every new page in Playwright at 390px width, confirm results render and there are no page errors.
- Do not touch `src/static/google*.html` (Search Console verification).

## Tool backlog (pick from the top, remove when done)
- 油耗與油錢計算
- 薪資時薪換算（月薪↔時薪↔年薪）
- 進位制換算（二/八/十/十六進位）
- 溫度換算（攝氏/華氏）
- 長度換算（公分/台尺/吋/英尺）
- 倒數計時天數（距離某節日還有幾天）
- 預產期計算
- 利率換算（年利率↔月利率↔日利率）
- 隨機抽籤／分組工具
- 字數計算（中英文字數、字元數）
- 單價比較（不同容量哪個划算）
- 貸款提前還款試算
