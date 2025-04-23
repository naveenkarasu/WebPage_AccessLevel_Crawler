"""
@file: playwright_crawler.py
@desc: Asynchronous web crawler using Playwright to detect access levels of pages from a base URL.
       Handles JavaScript-heavy pages and runs multiple browser tasks concurrently.
@usage: Run the script, choose a browser (chromium/firefox/webkit), and enter a base URL.
@requires: playwright, pandas, openpyxl
"""

import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urljoin, urlparse
import pandas as pd

visited = set()
results = []
domain = ""

async def get_access_level(page, requested_url):
    """
    @desc: Determines access level based on current URL and page content.
    @param page: Playwright page object
    @param requested_url: Original URL to compare against
    @return: Access level string
    """
    cur = page.url.lower()
    src = await page.content()
    src_l = src.lower()

    if any(err in src_l for err in ["404", "not found", "403", "forbidden"]):
        return "not accessible to regular use"
    if cur != requested_url.lower() and any(tok in cur for tok in ["login", "signin", "auth"]):
        return "requires login"
    if 'type="password"' in src_l or ("password" in src_l and "<input" in src_l):
        return "requires login"
    return "no login required"

async def worker(name, queue, browser, sem, max_pages):
    """
    @desc: Individual browser worker that processes one URL at a time and adds discovered links.
    @param name: Worker name
    @param queue: Shared queue of URLs to visit
    @param browser: Playwright browser instance
    @param sem: Async semaphore for concurrency control
    @param max_pages: Maximum number of pages to visit
    """
    global visited, results
    while not queue.empty() and len(visited) < max_pages:
        url = await queue.get()
        async with sem:
            if url in visited:
                queue.task_done()
                continue
            try:
                context = await browser.new_context()
                page = await context.new_page()
                await page.goto(url, wait_until="networkidle")

                level = await get_access_level(page, url)
                visited.add(url)
                results.append((url, level))
                print(f"[{name}] {url} → {level}")

                hrefs = await page.eval_on_selector_all("a[href]", "els => els.map(e => e.href)")
                for href in hrefs:
                    full = urljoin(url, href)
                    if urlparse(full).netloc == domain and full not in visited:
                        await queue.put(full)

                await context.close()
            except Exception as e:
                print(f"[{name}] Error on {url}: {e}")
            finally:
                queue.task_done()

async def crawl(base_url, browser_choice, max_pages=100, concurrency=5):
    """
    @desc: Orchestrates all crawling tasks and saves final results to Excel.
    @param base_url: Starting URL
    @param browser_choice: 'chromium', 'firefox', or 'webkit'
    @param max_pages: Total number of pages to crawl
    @param concurrency: Number of concurrent browser workers
    """
    global domain
    domain = urlparse(base_url).netloc
    queue = asyncio.Queue()
    await queue.put(base_url)

    async with async_playwright() as p:
        browser = await getattr(p, browser_choice).launch(headless=True)
        sem = asyncio.Semaphore(concurrency)

        workers = [
            asyncio.create_task(worker(f"W{i+1}", queue, browser, sem, max_pages))
            for i in range(concurrency)
        ]
        await queue.join()
        for w in workers:
            w.cancel()
        await browser.close()

    df = pd.DataFrame(results, columns=["url", "access level"])
    df.to_excel("playwright_crawled_urls.xlsx", index=False)
    print("\n✅ Saved to playwright_crawled_urls.xlsx")

if __name__ == "__main__":
    choice = input("Choose browser (chromium/firefox/webkit): ").strip().lower()
    if choice not in ("chromium", "firefox", "webkit"):
        raise SystemExit("Invalid choice—must be one of chromium, firefox, or webkit.")
    start = input("Enter base URL (e.g. https://example.com): ").strip()
    asyncio.run(crawl(start, choice))
