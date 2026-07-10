import json
import os
import re
import sys
import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.jndhjyzx.com'

SECTIONS = [
    {'key': 'zonghe', 'title': '综合施教'},
    {'key': 'xunlian', 'title': '拓展训练'},
    {'key': 'zixun', 'title': '心理咨询'},
    {'key': 'fengcai', 'title': '学生风采'},
]

REQUEST_TIMEOUT = 60
MAX_RETRIES = 3
RETRY_DELAY = 2


session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})


def fetch(url, timeout=REQUEST_TIMEOUT, retries=MAX_RETRIES):
    last_error = None
    for attempt in range(retries):
        try:
            r = session.get(url, timeout=timeout)
            r.encoding = 'utf-8'
            return BeautifulSoup(r.text, 'html.parser')
        except Exception as e:
            last_error = e
            print(f"    [WARN] fetch {url} attempt {attempt + 1}/{retries} failed: {e}")
            if attempt < retries - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
    raise last_error


def sanitize_filename(name):
    name = re.sub(r'[\\/:*?"<>|]+', '_', name).strip()
    name = re.sub(r'\s+', '_', name)
    return name[:100] or 'unnamed'


def resolve_url(src, base_url):
    if not src:
        return None
    src = src.strip()
    if src.startswith('//'):
        src = 'http:' + src
    return urljoin(base_url, src)


def get_image_filename(url, idx=0):
    parsed = urlparse(url)
    base = os.path.basename(parsed.path) or 'image'
    name, ext = os.path.splitext(base)
    if not ext or ext.lower() not in {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}:
        ext = '.jpg'
    safe_name = re.sub(r'[^\w\-]+', '_', name)[:60]
    return f"{idx:03d}_{safe_name}{ext}"


def download_image(url, dest_path, retries=MAX_RETRIES):
    try:
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        for attempt in range(retries):
            try:
                r = session.get(url, timeout=REQUEST_TIMEOUT)
                r.raise_for_status()
                with open(dest_path, 'wb') as f:
                    f.write(r.content)
                return len(r.content)
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(RETRY_DELAY * (attempt + 1))
                else:
                    raise e
    except Exception as e:
        print(f"    [ERROR] download {url}: {e}")
        return None


def extract_article_links(soup, list_url, section_key):
    pattern = re.compile(rf'/{section_key}/\d+\.html$')
    links = []
    for a in soup.find_all('a', href=pattern):
        href = a.get('href')
        if not href:
            continue
        full = resolve_url(href, list_url)
        m = re.search(rf'/{section_key}/(\d+)\.html', href)
        if not m:
            continue
        article_id = m.group(1)
        title = a.get_text(strip=True).split('\n')[0][:120]
        links.append({'id': article_id, 'url': full, 'title': title})

    seen = set()
    unique = []
    for link in links:
        if link['id'] not in seen:
            seen.add(link['id'])
            unique.append(link)
    return unique


def discover_pages(list_url, section_key):
    print(f"  Discovering list pages for {section_key}...")
    soup = fetch(list_url)
    pagination = soup.find('ul', class_='pagination')
    last_page = 1
    if pagination:
        pattern = re.compile(rf'/{section_key}/p(\d+)\.html')
        for a in pagination.find_all('a', href=True):
            m = pattern.search(a['href'])
            if m:
                last_page = max(last_page, int(m.group(1)))
    print(f"    Total list pages: {last_page}")
    return last_page


def crawl_list_page(page_num, section_key):
    if page_num == 1:
        url = f"{BASE_URL}/{section_key}/"
    else:
        url = f"{BASE_URL}/{section_key}/p{page_num}.html"
    print(f"  Crawling list page {page_num}: {url}")
    soup = fetch(url)
    articles = extract_article_links(soup, url, section_key)

    list_images = []
    for idx, img in enumerate(soup.find_all('img'), 1):
        src = img.get('src')
        if not src:
            continue
        full = resolve_url(src, url)
        if not full or '/uploadfile/' not in full:
            continue
        list_images.append({
            'src': full,
            'alt': img.get('alt', ''),
            'filename': get_image_filename(full, idx)
        })

    return {
        'page_num': page_num,
        'url': url,
        'articles': articles,
        'list_images': list_images
    }


def crawl_article(article, section_key):
    article_id = article['id']
    url = article['url']
    print(f"    Crawling article {article_id}: {url}")
    try:
        soup = fetch(url)
    except Exception as e:
        print(f"      [ERROR] fetch article {article_id}: {e}")
        return None

    title = article['title']
    h1 = soup.find('h1')
    if h1:
        title = h1.get_text(strip=True)
    else:
        for sel in ['.title', '.news-title', '.article-title', '.titl-o', '.content-title']:
            el = soup.select_one(sel)
            if el:
                title = el.get_text(strip=True)
                break

    content = None
    for sel in ['.content', '.article-content', '.news-content', '.ny-nr', '.lb-nr', '.main-content', '.detail']:
        content = soup.select_one(sel)
        if content:
            break
    if not content:
        body = soup.find('body')
        if body:
            content = body

    text = content.get_text('\n', strip=True) if content else ''

    images = []
    if content:
        for idx, img in enumerate(content.find_all('img'), 1):
            src = img.get('src')
            if not src:
                continue
            full = resolve_url(src, url)
            if not full:
                continue
            images.append({
                'src': full,
                'alt': img.get('alt', ''),
                'filename': get_image_filename(full, idx)
            })

    return {
        'id': article_id,
        'url': url,
        'title': title,
        'text': text,
        'images': images
    }


def save_list_page(page_data, base_dir):
    page_dir = os.path.join(base_dir, 'list', f"page_{page_data['page_num']:02d}")
    images_dir = os.path.join(page_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)

    saved_images = []
    for img in page_data['list_images']:
        dest = os.path.join(images_dir, img['filename'])
        size = download_image(img['src'], dest)
        saved_images.append({**img, 'size_bytes': size, 'downloaded': size is not None})

    meta = {
        'page_num': page_data['page_num'],
        'url': page_data['url'],
        'article_count': len(page_data['articles']),
        'articles': page_data['articles'],
        'images': saved_images
    }
    with open(os.path.join(page_dir, 'metadata.json'), 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    return meta


def save_article(article_data, base_dir):
    if not article_data:
        return None
    article_dir = os.path.join(base_dir, 'articles', article_data['id'])
    images_dir = os.path.join(article_dir, 'images')
    os.makedirs(images_dir, exist_ok=True)

    saved_images = []
    for img in article_data['images']:
        dest = os.path.join(images_dir, img['filename'])
        size = download_image(img['src'], dest)
        saved_images.append({**img, 'size_bytes': size, 'downloaded': size is not None})

    meta = {
        'id': article_data['id'],
        'url': article_data['url'],
        'title': article_data['title'],
        'images': saved_images
    }
    with open(os.path.join(article_dir, 'metadata.json'), 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    with open(os.path.join(article_dir, 'content.txt'), 'w', encoding='utf-8') as f:
        f.write(article_data['text'])
    return meta


def crawl_section(section):
    section_key = section['key']
    section_title = section['title']
    base_dir = os.path.join('data', section_key)
    os.makedirs(base_dir, exist_ok=True)

    list_url = f"{BASE_URL}/{section_key}/"
    print(f"\n{'='*60}")
    print(f"Section: {section_title} ({section_key})")
    print(f"{'='*60}")

    last_page = discover_pages(list_url, section_key)
    all_articles = []

    for page_num in range(1, last_page + 1):
        try:
            page_data = crawl_list_page(page_num, section_key)
            save_list_page(page_data, base_dir)
            all_articles.extend(page_data['articles'])
        except Exception as e:
            print(f"  [ERROR] Failed to crawl list page {page_num}: {e}")

    print(f"\n  Total articles to crawl: {len(all_articles)}")

    success = 0
    failed = []
    for article in all_articles:
        article_dir = os.path.join(base_dir, 'articles', article['id'])
        if os.path.exists(os.path.join(article_dir, 'metadata.json')):
            print(f"    Skipping already crawled article {article['id']}")
            success += 1
            continue
        article_data = crawl_article(article, section_key)
        if article_data:
            save_article(article_data, base_dir)
            success += 1
        else:
            failed.append(article['id'])

    # Retry failed articles once
    if failed:
        print(f"\n  Retrying {len(failed)} failed articles...")
        still_failed = []
        for article_id in failed:
            article = next((a for a in all_articles if a['id'] == article_id), None)
            if article:
                article_data = crawl_article(article, section_key)
                if article_data:
                    save_article(article_data, base_dir)
                    success += 1
                else:
                    still_failed.append(article_id)
        failed = still_failed

    summary = {
        'section': section_title,
        'list_pages': last_page,
        'total_articles': len(all_articles),
        'crawled_articles': success,
        'failed_articles': failed
    }
    with open(os.path.join(base_dir, 'summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\n  Done. Articles: {success}/{len(all_articles)} succeeded.")
    if failed:
        print(f"  Failed IDs: {failed}")
    return summary


def main():
    results = []
    for section in SECTIONS:
        try:
            summary = crawl_section(section)
            results.append(summary)
        except Exception as e:
            print(f"\n[ERROR] Section {section['key']} failed: {e}")

    print(f"\n{'='*60}")
    print("All sections summary:")
    for r in results:
        print(f"  {r['section']}: {r['list_pages']} list pages, {r['crawled_articles']}/{r['total_articles']} articles")


if __name__ == '__main__':
    main()
