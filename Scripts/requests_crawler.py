"""
@file: requests_crawler.py
@desc: Basic web crawler using requests and BeautifulSoup. Crawls from a base URL,
       follows internal links, and classifies each page by access level.
@usage: Run the script and input a base URL when prompted.
@requires: requests, beautifulsoup4, pandas, openpyxl
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import pandas as pd
from collections import deque

def detect_access_level(response, url):
    """
    @desc: Determines the access level of a URL based on HTTP status code and content.
    @param response: Response object from requests.get()
    @param url: The URL being accessed
    @return: A string - 'no login required', 'requires login', or 'not accessible to regular use'
    """
    if response.status_code == 200:
        text = response.text.lower()
        if any(token in text for token in ['login', 'password', 'signin']):
            return 'requires login'
        return 'no login required'
    elif response.status_code in [401, 403, 404]:
        return 'not accessible to regular use'
    else:
        return f'unknown ({response.status_code})'

def crawl(base_url, max_pages=100):
    """
    @desc: Crawls internal pages starting from base_url and classifies them by access level.
    @param base_url: The URL to start crawling from
    @param max_pages: Maximum number of pages to crawl
    """
    visited = set()
    domain = urlparse(base_url).netloc
    queue = deque([base_url])
    results = []

    while queue and len(visited) < max_pages:
        url = queue.popleft()
        if url in visited:
            continue

        try:
            response = requests.get(url, timeout=5)
            visited.add(url)
            access_level = detect_access_level(response, url)
            print(f"[+] {url} → {access_level}")
            results.append((url, access_level))

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for tag in soup.find_all('a', href=True):
                    href = tag['href']
                    full_url = urljoin(url, href)
                    if urlparse(full_url).netloc == domain and full_url not in visited:
                        queue.append(full_url)
        except Exception as e:
            print(f"[!] Error on {url}: {e}")

    df = pd.DataFrame(results, columns=["url", "access level"])
    df.to_excel("requests_crawled_urls.xlsx", index=False)
    print("\n✅ Saved to requests_crawled_urls.xlsx")

if __name__ == "__main__":
    base_url = input("Enter base URL (e.g. https://example.com): ").strip()
    crawl(base_url)
