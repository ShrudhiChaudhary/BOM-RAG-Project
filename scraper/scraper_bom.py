"""
Scrape Bank of Maharashtra loan pages.
Usage:
  1. Create a urls.txt with one Bank of Maharashtra loan page URL per line (only BOM domain).
  2. python scrape_bom.py --urls urls.txt --out_dir ../data/raw
"""
import os
import argparse
import time
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Selenium fallback for JS-heavy pages
USE_SELENIUM = True
SELENIUM_TIMEOUT = 15

def domain_allowed(url):
    p = urlparse(url)
    return (
        "bankofmaharashtra.in" in p.netloc or
        "bankofmaharashtra.co.in" in p.netloc or
        "bankofmaharashtra.bank.in" in p.netloc
    )


def fetch_requests(url):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; Bot/1.0)"}
    # resp = requests.get(url, headers=headers, timeout=20)
    resp = requests.get(url, headers=headers, timeout=20, allow_redirects=True)
    resp.raise_for_status()
    return resp.text

def fetch_with_selenium(url):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager

    opts = Options()
    opts.headless = True
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
    driver.set_page_load_timeout(SELENIUM_TIMEOUT)
    try:
        driver.get(url)
        time.sleep(2)  # let JS load
        html = driver.page_source
    finally:
        driver.quit()
    return html

def extract_relevant_text(html):
    soup = BeautifulSoup(html, "lxml")
    # remove nav, scripts, style
    for tag in soup(["script", "style", "header", "footer", "nav", "aside", "form"]):
        tag.decompose()
    # Attempt to find main content containers
    main_text = []
    # gather text from <main> if present
    main = soup.find("main")
    if main:
        main_text.append(main.get_text(separator="\n"))
    # fallback: use article or large section tags
    for t in soup.find_all(["article", "section", "div"]):
        txt = t.get_text(separator="\n").strip()
        if len(txt) > 200:  # heuristic
            main_text.append(txt)
    # fallback: whole page
    if not main_text:
        main_text = [soup.get_text(separator="\n")]
    content = "\n\n".join(main_text)
    return content

def save_output(out_dir, url, content):
    os.makedirs(out_dir, exist_ok=True)
    safe_name = url.replace("https://", "").replace("http://", "").replace("/", "_").replace("?", "_")
    fn = os.path.join(out_dir, f"{safe_name}.txt")
    with open(fn, "w", encoding="utf-8") as f:
        f.write(content)
    return fn

def scrape(urls, out_dir, use_selenium=False):
    outputs = []
    for url in tqdm(urls):
        url = url.strip()
        if not url:
            continue
        if not domain_allowed(url):
            print(f"Skipping non-BOM domain: {url}")
            continue
        try:
            html = fetch_requests(url)
        except Exception as e:
            print(f"requests failed for {url}: {e}")
            if use_selenium:
                try:
                    html = fetch_with_selenium(url)
                except Exception as e2:
                    print(f"selenium failed for {url}: {e2}")
                    continue
            else:
                continue
        content = extract_relevant_text(html)
        out_path = save_output(out_dir, url, content)
        outputs.append(out_path)
    return outputs

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--urls", required=True, help="file with urls (one per line)")
    parser.add_argument("--out_dir", default="../data/raw", help="where to write raw files")
    parser.add_argument("--selenium", action="store_true", help="use selenium fallback")
    args = parser.parse_args()
    with open(args.urls, "r", encoding="utf-8") as f:
        urls = f.readlines()
    scraped = scrape(urls, args.out_dir, use_selenium=args.selenium)
    print("Scraped files:", scraped)
