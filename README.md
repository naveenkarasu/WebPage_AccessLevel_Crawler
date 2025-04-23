
# 🕸️ Web Page Access Level Crawler

This repository provides three beginner-friendly Python-based web crawlers that explore a website starting from a base URL, discover all accessible pages, and classify each page by access level:

- ✅ No login required  
- 🔐 Requires login  
- 🚫 Not accessible to regular users  

The output is saved to an Excel file for analysis.

---

## 📌 Use Cases

- Explore internal site structure for testing, documentation, or audits  
- Identify which pages are protected by authentication  
- Learn about web crawling using modern tools like Selenium and Playwright  

---

## 🚀 Features

- Supports three methods:
  1. Requests + BeautifulSoup (basic)
  2. Selenium (for JavaScript-heavy pages)
  3. Playwright (modern async & headless JS rendering)
- Access level detection using smart heuristics
- Saves results as an Excel file
- Cross-platform (Windows, macOS, Linux)
- Beginner-friendly and well-documented

---

## 📂 Repository Structure

| File | Description |
|------|-------------|
| requests_crawler.py | Basic crawler using requests + BeautifulSoup |
| selenium_crawler.py | Selenium-based crawler (handles JS, user input for browser) |
| playwright_crawler.py | Async Playwright crawler (fast, modern, JS rendering) |
| requirements.txt | Python dependencies |
| README.md | You’re reading it! |

---

## 🛠️ Prerequisites

Ensure Python 3.7+ is installed on your system.

Install required packages:

```bash
pip install -r requirements.txt
```

Then install Playwright browsers (for playwright_crawler.py):

```bash
playwright install
```

---

## 📥 How to Use

Each crawler will prompt you for:

- Base URL (e.g. https://example.com)
- Browser (for Selenium or Playwright)

🧪 Output: A file named selenium_crawled_urls.xlsx or playwright_crawled_urls.xlsx will be generated, with each URL and its access level.

---

## 💡 Three Ways to Crawl

### 1️⃣ requests_crawler.py  
- Lightest method (no JS support)  
- Use when site uses plain HTML or minimal JavaScript

### 2️⃣ selenium_crawler.py  
- Use Chrome or Firefox in headless mode  
- Ideal for login pages, dashboards, or JS-rendered content

### 3️⃣ playwright_crawler.py  
- Fastest and most robust for JS-heavy websites  
- Asynchronous crawler with concurrency support

---

## 📊 Output Format

Excel file with two columns:

| URL | Access Level |
|-----|---------------|
| https://example.com/home | no login required |
| https://example.com/dashboard | requires login |
| https://example.com/admin | not accessible to regular use |

---

## 🧪 How Access Levels Are Detected

We analyze:
- HTTP status codes (403, 404, etc.)
- Redirects to login or auth pages
- Presence of login fields or password inputs

---

## 🖥️ Verifying Drivers & Browsers

For Selenium and Playwright, browser drivers are required.

▶️ Check if drivers are available:

- Windows:  
  ```cmd
  where chromedriver
  where geckodriver
  ```

- macOS/Linux:  
  ```bash
  which chromedriver
  which geckodriver
  ```

▶️ Install drivers:

- ChromeDriver: https://sites.google.com/chromium.org/driver  
- GeckoDriver: https://github.com/mozilla/geckodriver/releases

▶️ Playwright:

```bash
pip install playwright
playwright install
```

---

## 📘 Learn More: Beginner’s Guide to Web Crawling & Automation

Want to understand the why behind this tool? Here’s a breakdown of everything covered in our companion blog post:

> 📝 [Why Learning to Crawl the Web is a Superpower: A Beginner’s Guide to Web Page Access Analysis](#) *(Link will be updated with the official blog post soon)*
<!-- TODO: Replace # with actual blog URL once published -->


This article explains:
- ✅ Why crawling matters (for security, audits, learning)
- 🔍 5 Why’s of web crawling — even for beginners
- 🛠️ Step-by-step setup instructions (Windows, macOS, Debian, Fedora)
- 🌐 Real-world use cases for Requests, Selenium, and Playwright
- 📊 How access levels are detected
- ⚠️ A reminder to crawl ethically (learning purposes only)

Perfect for:
- Tech hobbyists  
- QA testers  
- New devs  
- Bloggers building smarter workflows

> Use it to explore, test, and learn — one URL at a time.

## ⚠️ Disclaimer

This tool is intended only for learning and ethical exploration of websites you own or have permission to analyze.  
Do not use it for unauthorized scanning of third-party sites.

---
