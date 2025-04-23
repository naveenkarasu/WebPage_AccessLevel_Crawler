"""
@file: selenium_crawler.py
@desc: Web crawler using Selenium to detect page access levels from a base URL.
       Handles JavaScript-rendered content and login checks.
@usage: Run the script, choose a browser (chrome/firefox), and input a base URL.
@requires: selenium, pandas, openpyxl, chromedriver/geckodriver installed
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from urllib.parse import urljoin, urlparse
import pandas as pd
import time

visited = set()
paths_access = []   # list of (url, access_level)
domain = ""

def setup_driver(browser_choice):
    """
    @desc: Launches a headless browser based on user choice.
    @param browser_choice: 'chrome' or 'firefox'
    @return: Selenium WebDriver instance
    """
    if browser_choice.lower() == "chrome":
        opts = ChromeOptions()
        opts.headless = True
        return webdriver.Chrome(options=opts)
    elif browser_choice.lower() == "firefox":
        opts = FirefoxOptions()
        opts.headless = True
        return webdriver.Firefox(options=opts)
    else:
        raise ValueError("Unsupported browser. Choose 'chrome' or 'firefox'.")

def get_access_level(driver, requested_url):
    """
    @desc: Classifies the current page's access level using page URL and content heuristics.
    @param driver: Selenium WebDriver instance on the target page
    @param requested_url: Original URL requested
    @return: A string - 'no login required', 'requires login', or 'not accessible to regular use'
    """
    cur = driver.current_url.lower()
    src = driver.page_source.lower()

    if any(err in src for err in ["404", "not found", "403", "forbidden"]):
        return "not accessible to regular use"
    if cur != requested_url.lower() and any(tok in cur for tok in ["login", "signin", "auth"]):
        return "requires login"
    if 'type="password"' in src or ("password" in src and "<input" in src):
        return "requires login"
    return "no login required"

def crawl_with_selenium(base_url, browser_choice, max_pages=100):
    """
    @desc: Main crawler logic using Selenium to navigate and analyze internal site pages.
    @param base_url: Starting URL to begin crawling
    @param browser_choice: Browser to use (chrome/firefox)
    @param max_pages: Maximum number of pages to crawl
    """
    global domain
    domain = urlparse(base_url).netloc
    to_visit = [base_url]
    driver = setup_driver(browser_choice)

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue

        try:
            driver.get(url)
            time.sleep(1)  # allow JavaScript to render

            level = get_access_level(driver, url)
            visited.add(url)
            paths_access.append((url, level))
            print(f"[+] {url} → {level}")

            for link in driver.find_elements(By.TAG_NAME, "a"):
                href = link.get_attribute("href")
                if href:
                    full = urljoin(url, href)
                    if urlparse(full).netloc == domain and full not in visited:
                        to_visit.append(full)

        except Exception as e:
            print(f"[!] Error crawling {url}: {e}")

    driver.quit()

    df = pd.DataFrame(paths_access, columns=["url", "access level"])
    df.to_excel("selenium_crawled_urls.xlsx", index=False)
    print("\n✅ Saved to selenium_crawled_urls.xlsx")

if __name__ == "__main__":
    browser = input("Enter browser (chrome/firefox): ").strip()
    start_url = input("Enter base URL (e.g. https://example.com): ").strip()
    crawl_with_selenium(start_url, browser)
