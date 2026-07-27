import asyncio
import re
from playwright.async_api import async_playwright

SEEDS = range(60, 70)
URL_TMPL = "https://sanand0.github.io/tdsdata/js_table/?seed={seed}"

NUM_RE = re.compile(r"-?\d+(?:\.\d+)?")


async def sum_page(page, seed):
    url = URL_TMPL.format(seed=seed)
    await page.goto(url, wait_until="networkidle")
    await page.wait_for_selector("table")
    text = await page.inner_text("#table")
    total = sum(float(m) for m in NUM_RE.findall(text))
    print(f"seed={seed} sum={total}")
    return total


async def main():
    grand_total = 0.0
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        for seed in SEEDS:
            grand_total += await sum_page(page, seed)
        await browser.close()
    print(f"GRAND TOTAL: {grand_total}")


if __name__ == "__main__":
    asyncio.run(main())
