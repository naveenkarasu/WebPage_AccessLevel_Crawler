# 🤝 Contributing Guide

Thank you for your interest in contributing to the Web Page Access Level Crawler!  
This project welcomes beginner and intermediate Python developers who want to learn and improve the tool.

---

## 📋 How to Contribute

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/web-access-crawler.git
cd web-access-crawler
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

For Playwright users, also run:

```bash
playwright install
```

### 3. Run a Crawler

Pick one of the scripts:
- `requests_crawler.py`
- `selenium_crawler.py`
- `playwright_crawler.py`

Follow on-screen prompts to crawl and generate results.

---

## ✨ Ways to Contribute

- Improve detection logic (e.g., smarter login/access detection)
- Add CLI arguments instead of input() prompts
- Support authentication tokens/cookies
- Improve multithreading (for requests or selenium)
- Submit bug reports or performance improvements
- Help improve README or documentation

---

## 🐛 Reporting Issues

Please use the GitHub Issues tab to report:
- Bugs
- Unexpected behavior
- Suggestions
- Questions

Include:
- OS and browser info (if using Selenium or Playwright)
- Python version
- Exact steps to reproduce

---

## ✅ Code Style

- Use clear variable names and comments
- Prefer docstrings for functions (we follow the @desc, @param, @return style)
- Keep code readable and beginner-friendly

---

## ⚠️ Ethical Use Reminder

Please only use this tool to crawl websites you own, control, or have permission to analyze.  
Never use it to scrape or audit websites without proper authorization.

---

Thank you again for helping improve this project! 💙
