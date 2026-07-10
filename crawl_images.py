import json
import os
import re
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.jndhjyzx.com'
PAGES = [
    {'key': 'home', 'path': '/', 'title': '网站首页'},
    {'key': 'about', 'path': '/about/', 'title': '关于我们'},
    {'key': 'zanding', 'path': '/zanding/', 'title': '问题论坛'},
    {'key': 'zonghe', 'path': '/zonghe/', 'title': '综合施教'},
    {'key': 'xunlian', 'path': '/xunlian/', 'title': '拓展训练'},
    {'key': 'zixun', 'path': '/zixun/', 'title': '心理咨询'},
    {'key': 'fengcai', 'path': '/fengcai/', 'title': '学生风采'},
    {'key': 'contact', 'path': '/contact/', 'title': '联系我们'},
]

STATIC_PATTERNS = [
    r'/static/.*',
    r'.*web/img/.*',
]


def is_static_asset(url):
    for p in STATIC_PATTERNS:
        if re.match(p, url):
            return True
    return False


def sanitize_name(name):
    name = re.sub(r'[\\/:*?"<>|]+', '_', name).strip()
    name = re.sub(r'\s+', '_', name)
    return name[:80] or 'unnamed'


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


def download_image(url, dest_path):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        with open(dest_path, 'wb') as f:
            f.write(r.content)
        return len(r.content)
    except Exception as e:
        print(f"  [ERROR] download {url}: {e}")
        return None


def img_meta(img):
    return {'src': img.get('src'), 'alt': img.get('alt', '')}


def extract_home_modules(soup):
    modules = []
    top = soup.find('div', class_='top')
    if top:
        imgs = [img_meta(i) for i in top.find_all('img')]
        if imgs:
            modules.append({'name': '顶部导航', 'images': imgs})
    banner = soup.find('div', class_='banner')
    if banner:
        imgs = [img_meta(i) for i in banner.find_all('img')]
        if imgs:
            modules.append({'name': '首页Banner', 'images': imgs})
    abou = soup.find('div', class_='abou')
    if abou:
        heading = abou.find('div', class_='abou-b')
        name = heading.get_text(strip=True) if heading else '关于我们'
        imgs = [img_meta(i) for i in abou.find_all('img')]
        if imgs:
            modules.append({'name': name, 'images': imgs})
    lb = soup.find('div', class_='lb')
    if lb:
        # Each module is a titl-o heading followed by a lb-o container
        titl = lb.find('div', class_='titl')
        if titl:
            current_name = None
            for child in titl.children:
                if getattr(child, 'name', None) == 'div' and 'titl-o' in (child.get('class') or []):
                    current_name = child.get_text(strip=True)
                elif getattr(child, 'name', None) == 'div' and 'lb-o' in (child.get('class') or []) and current_name:
                    imgs = [img_meta(i) for i in child.find_all('img')]
                    if imgs:
                        modules.append({'name': current_name, 'images': imgs})
    ext = soup.find('div', class_='ext')
    if ext:
        heading = ext.find('div', class_='titl-o')
        name = heading.get_text(strip=True) if heading else '拓展训练'
        imgs = [img_meta(i) for i in ext.find_all('img')]
        if imgs:
            modules.append({'name': name, 'images': imgs})
    mind = soup.find('div', class_='mind')
    if mind:
        heading = mind.find('div', class_='titl-o')
        name = heading.get_text(strip=True) if heading else '心理咨询'
        imgs = [img_meta(i) for i in mind.find_all('img')]
        if imgs:
            modules.append({'name': name, 'images': imgs})
    stud = soup.find('div', class_='stud')
    if stud:
        heading = stud.find('div', class_='titl-o')
        name = heading.get_text(strip=True) if heading else '学生风采'
        imgs = [img_meta(i) for i in stud.find_all('img')]
        if imgs:
            modules.append({'name': name, 'images': imgs})
    foot = soup.find('div', class_='foot')
    if foot:
        imgs = [img_meta(i) for i in foot.find_all('img')]
        if imgs:
            modules.append({'name': '页脚联系', 'images': imgs})
    return modules


def extract_generic_modules(soup, page_title):
    modules = []
    headings = soup.find_all('div', class_='titl-o')
    if headings:
        for h in headings:
            title = h.get_text(strip=True) or page_title
            container = h.find_parent('div', class_='titl') or h.parent
            imgs = [img_meta(i) for i in (container.find_all('img') if container else [])]
            if imgs:
                modules.append({'name': title, 'images': imgs})
    if not modules:
        body = soup.find('body')
        imgs = [img_meta(i) for i in (body.find_all('img') if body else soup.find_all('img'))]
        imgs = [i for i in imgs if i.get('src') and not is_static_asset(i['src'])]
        if imgs:
            modules.append({'name': page_title, 'images': imgs})
    return modules


def extract_modules(soup, page):
    if page['key'] == 'home':
        return extract_home_modules(soup)
    return extract_generic_modules(soup, page['title'])


def main():
    os.makedirs('data', exist_ok=True)
    summary = []
    for page in PAGES:
        page_url = BASE_URL + page['path']
        print(f"Processing {page['title']} ({page_url})")
        r = requests.get(page_url, timeout=30)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        modules = extract_modules(soup, page)
        page_dir = os.path.join('data', page['key'])
        images_dir = os.path.join(page_dir, 'images')
        os.makedirs(images_dir, exist_ok=True)
        page_meta = {
            'title': page['title'],
            'url': page_url,
            'modules': []
        }
        for mod in modules:
            mod_name = mod['name']
            safe_mod = sanitize_name(mod_name)
            mod_dir = os.path.join(images_dir, safe_mod)
            os.makedirs(mod_dir, exist_ok=True)
            mod_meta = {
                'name': mod_name,
                'local_dir': f"images/{safe_mod}",
                'images': []
            }
            seen = set()
            for idx, img in enumerate(mod['images'], 1):
                src = img.get('src')
                if not src:
                    continue
                full_url = resolve_url(src, page_url)
                if not full_url or full_url in seen:
                    continue
                seen.add(full_url)
                filename = get_image_filename(full_url, idx)
                dest = os.path.join(mod_dir, filename)
                size = download_image(full_url, dest)
                mod_meta['images'].append({
                    'original_url': full_url,
                    'filename': filename,
                    'alt': img.get('alt', ''),
                    'size_bytes': size,
                    'downloaded': size is not None
                })
            page_meta['modules'].append(mod_meta)
        with open(os.path.join(page_dir, 'metadata.json'), 'w', encoding='utf-8') as f:
            json.dump(page_meta, f, ensure_ascii=False, indent=2)
        total_images = sum(len(m['images']) for m in page_meta['modules'])
        summary.append({
            'page': page['key'],
            'title': page['title'],
            'modules': len(page_meta['modules']),
            'images': total_images
        })
        print(f"  -> {len(page_meta['modules'])} modules, {total_images} images")
    with open(os.path.join('data', 'summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print("\nDone. Summary:")
    for s in summary:
        print(f"  {s['page']}: {s['modules']} modules, {s['images']} images")


if __name__ == '__main__':
    main()
