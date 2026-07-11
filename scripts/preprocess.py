import json
import os
import re
import shutil
import urllib.request
from pathlib import Path

ROOT = Path('C:/Users/86198/Desktop/web-edu')
DATA_DIR = ROOT / 'data'
OUT_DIR = ROOT / 'nuxt-app' / 'app' / 'public' / 'data'
IMG_OUT_DIR = ROOT / 'nuxt-app' / 'public' / 'images'

SECTIONS = [
    {'key': 'zanding', 'title': '问题论坛', 'subtitle': '找出问题 精准辅导'},
    {'key': 'zonghe', 'title': '综合施教', 'subtitle': '多管齐下 发掘学生潜力'},
    {'key': 'xunlian', 'title': '拓展训练', 'subtitle': '拓展人的价值观'},
    {'key': 'zixun', 'title': '心理咨询', 'subtitle': '个性化定制 心理辅导方案'},
    {'key': 'fengcai', 'title': '学生风采', 'subtitle': '用心奉献 成长在德泓'},
]

# Boilerplate images that appear on every page (top logo, banner, footer QR).
# They should be copied once to /images/common/ instead of every article/list folder.
BOILERPLATE_PATTERNS = ['96e14f88ddf0738', '90229136d5d440', 'nyban']


def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()


def parse_content_txt(text):
    """Parse article content.txt into structured fields."""
    lines = [ln.rstrip() for ln in text.splitlines()]
    result = {
        'title': '',
        'clicks': 0,
        'date': '',
        'author': '',
        'body': [],
        'prev_title': '',
        'next_title': '',
    }
    if len(lines) < 13:
        return result

    # Line 11 (0-indexed 10) is section subtitle, line 12 (0-indexed 11) is title
    result['title'] = clean_text(lines[11]) if len(lines) > 11 else ''

    body_start = None
    body_end = None
    for i, ln in enumerate(lines):
        if ln == '点击:':
            val = lines[i + 1] if i + 1 < len(lines) else ''
            try:
                result['clicks'] = int(clean_text(val))
            except ValueError:
                pass
        elif ln == '时间:':
            result['date'] = clean_text(lines[i + 1]) if i + 1 < len(lines) else ''
        elif ln == '作者:':
            result['author'] = clean_text(lines[i + 1]) if i + 1 < len(lines) else ''
            body_start = i + 2
        elif ln.startswith('上一篇：'):
            result['prev_title'] = clean_text(ln.replace('上一篇：', ''))
            body_end = i
        elif ln.startswith('下一篇：'):
            result['next_title'] = clean_text(ln.replace('下一篇：', ''))

    if body_start is None:
        for i, ln in enumerate(lines):
            if ln == '作者:':
                body_start = i + 2
                break
    if body_end is None:
        body_end = len(lines)
    if body_start is None:
        body_start = 14

    body_lines = lines[body_start:body_end]
    # Remove empty lines and join short lines into paragraphs
    paragraphs = []
    current = ''
    for ln in body_lines:
        ln = clean_text(ln)
        if not ln:
            if current:
                paragraphs.append(current)
                current = ''
        else:
            current = (current + ' ' + ln).strip() if current else ln
    if current:
        paragraphs.append(current)
    result['body'] = paragraphs
    return result


def is_boilerplate_image(filename: str) -> bool:
    return any(pattern in filename for pattern in BOILERPLATE_PATTERNS)


def copy_image(src: Path, dest: Path):
    if not src.exists():
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    return True


def copy_common_boilerplate_images():
    """Copy shared boilerplate images once to /images/common/."""
    copied = set()
    for sec in SECTIONS:
        sec_dir = DATA_DIR / sec['key']
        # Try to find boilerplate images from any article in this section
        art_base = sec_dir / 'articles'
        if not art_base.exists():
            continue
        for art_dir in art_base.iterdir():
            meta_path = art_dir / 'metadata.json'
            if not meta_path.exists():
                continue
            art_meta = json.loads(meta_path.read_text(encoding='utf-8'))
            for img in art_meta.get('images', []):
                fname = img['filename']
                if not is_boilerplate_image(fname):
                    continue
                if fname in copied:
                    continue
                src = art_dir / 'images' / fname
                dest = IMG_OUT_DIR / 'common' / fname
                if copy_image(src, dest):
                    copied.add(fname)
                    print(f'Copied common image: {fname}')
            if len(copied) >= len(BOILERPLATE_PATTERNS):
                break
        if len(copied) >= len(BOILERPLATE_PATTERNS):
            break

    # Also try to source boilerplate images from section metadata if article dirs are empty
    if len(copied) < len(BOILERPLATE_PATTERNS):
        for sec in SECTIONS:
            sec_meta_path = DATA_DIR / sec['key'] / 'metadata.json'
            if not sec_meta_path.exists():
                continue
            sec_meta = json.loads(sec_meta_path.read_text(encoding='utf-8'))
            for mod in sec_meta.get('modules', []):
                for img in mod.get('images', []):
                    fname = img['filename']
                    if not is_boilerplate_image(fname):
                        continue
                    if fname in copied:
                        continue
                    src = DATA_DIR / sec['key'] / mod['local_dir'] / fname
                    dest = IMG_OUT_DIR / 'common' / fname
                    if copy_image(src, dest):
                        copied.add(fname)
                        print(f'Copied common image from section metadata: {fname}')
                if len(copied) >= len(BOILERPLATE_PATTERNS):
                    break
            if len(copied) >= len(BOILERPLATE_PATTERNS):
                break

    # Fallback: use home metadata boilerplate images
    if len(copied) < len(BOILERPLATE_PATTERNS):
        home_meta_path = DATA_DIR / 'home' / 'metadata.json'
        if home_meta_path.exists():
            home_meta = json.loads(home_meta_path.read_text(encoding='utf-8'))
            for mod in home_meta.get('modules', []):
                for img in mod.get('images', []):
                    fname = img['filename']
                    if not is_boilerplate_image(fname):
                        continue
                    if fname in copied:
                        continue
                    src = DATA_DIR / 'home' / mod['local_dir'] / fname
                    dest = IMG_OUT_DIR / 'common' / fname
                    if copy_image(src, dest):
                        copied.add(fname)
                        print(f'Copied common image from home metadata: {fname}')
                if len(copied) >= len(BOILERPLATE_PATTERNS):
                    break
    return copied


def download_image(url: str, dest: Path):
    """Download an image from URL to dest, returning True on success."""
    if dest.exists():
        return True
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(url, dest)
        return True
    except Exception as e:
        print(f'Failed to download {url}: {e}')
        return False


def ensure_boilerplate_images():
    """Ensure common boilerplate images exist, downloading if necessary."""
    common_dir = IMG_OUT_DIR / 'common'
    common_dir.mkdir(parents=True, exist_ok=True)

    boilerplate = {
        '001_96e14f88ddf0738.png': 'https://www.jndhjyzx.com/uploadfile/202212/96e14f88ddf0738.png',
        '001_90229136d5d440.png': 'http://www.jndhjyzx.com/uploadfile/202212/90229136d5d440.png',
        '002_nyban.jpg': 'https://www.jndhjyzx.com/static/a/web/img/nyban.jpg',
    }

    for fname, url in boilerplate.items():
        dest = common_dir / fname
        if not dest.exists():
            if download_image(url, dest):
                print(f'Downloaded boilerplate image: {fname}')


def build_site_json():
    return {
        'title': '济南德泓教育咨询有限公司',
        'hotline': '13864188899、17615827726',
        'hotlineLabel': '24小时服务热线：',
        'icp': '鲁ICP备20032853号-1',
        'icpUrl': 'https://beian.miit.gov.cn/#/Integrated/index',
        'copyright': '版权所有：济南德泓教育咨询有限公司',
        'nav': [
            {'label': '网站首页', 'path': '/'},
            {'label': '关于我们', 'path': '/about'},
            {'label': '问题论坛', 'path': '/zanding'},
            {'label': '综合施教', 'path': '/zonghe'},
            {'label': '拓展训练', 'path': '/xunlian'},
            {'label': '心理咨询', 'path': '/zixun'},
            {'label': '学生风采', 'path': '/fengcai'},
            {'label': '联系我们', 'path': '/contact'},
        ],
    }


def build_sections_json():
    sections = {}
    for sec in SECTIONS:
        key = sec['key']
        summary_path = DATA_DIR / key / 'summary.json'
        total = 0
        pages = 1
        if summary_path.exists():
            summary = json.loads(summary_path.read_text(encoding='utf-8'))
            total = summary.get('total_articles', 0)
            pages = summary.get('list_pages', 1)
        sections[key] = {
            'key': key,
            'title': sec['title'],
            'subtitle': sec['subtitle'],
            'count': total,
            'pages': pages,
        }
    return sections


def module_images_from_home(module_name: str, dest_prefix: str):
    """Copy images from home metadata module and return public src array."""
    home_meta_path = DATA_DIR / 'home' / 'metadata.json'
    if not home_meta_path.exists():
        return []
    home_meta = json.loads(home_meta_path.read_text(encoding='utf-8'))
    module_map = {m['name']: m for m in home_meta.get('modules', [])}
    mod = module_map.get(module_name)
    if not mod:
        return []
    src_dir = DATA_DIR / 'home' / mod['local_dir']
    out = []
    for img in mod.get('images', []):
        src = src_dir / img['filename']
        dest = IMG_OUT_DIR / dest_prefix / img['filename']
        if copy_image(src, dest):
            out.append({'src': f'/images/{dest_prefix}/{img["filename"]}', 'alt': img.get('alt', '')})
    return out


def build_home_json(section_results: dict):
    # About intro text reused from original homepage
    about_intro = (
        '济南德泓教育咨询有限公司是由济南市工商局批准成立的正规专业咨询教育机构，'
        '主要针对青少年厌学逃课、叛逆、早恋、自控力差、啃老、不懂感恩、自卑自恋、离家出走、'
        '人格异常、强迫、抑郁、打架斗殴、暴力倾向、亲情淡漠等常见问题。我们坚持以孩子为中心、'
        '以家庭为基础、走进孩子心灵、塑造健全人格为理念，把孩子培养成“五会”（即学会自理自立，'
        '学会如何学习，学会团结互助，学会为人处事，学会理解关心父母）“三恩”（即知恩，感恩，报恩）'
        '的阳光青少年。'
    )

    about_images = module_images_from_home('关于我们', 'home/about')
    banner_images = module_images_from_home('首页Banner', 'home/banner')

    previews = {}
    for sec in SECTIONS:
        key = sec['key']
        sec_data = section_results.get(key, {})
        articles = sec_data.get('articles', [])

        if key == 'xunlian':
            # Gallery: up to 5 images (first large, rest small)
            gallery_images = []
            for art in articles[:5]:
                if art.get('image'):
                    gallery_images.append({
                        'src': art['image'],
                        'alt': art['title'],
                        'title': art['title'],
                        'path': art['path'],
                    })
            previews[key] = {
                'key': key,
                'title': sec['title'],
                'subtitle': sec['subtitle'],
                'images': gallery_images,
            }
        elif key == 'zixun':
            # News list: up to 3 items with formatted date
            items = []
            for art in articles[:3]:
                date = art.get('date', '')
                day = ''
                year = ''
                if date and len(date.split('-')) == 3:
                    parts = date.split('-')
                    day = f'{parts[1]}.{parts[2]}'
                    year = parts[0]
                items.append({
                    'id': art['id'],
                    'title': art['title'],
                    'date': date,
                    'day': day,
                    'year': year,
                    'excerpt': art.get('excerpt', ''),
                    'path': art['path'],
                })
            previews[key] = {
                'key': key,
                'title': sec['title'],
                'subtitle': sec['subtitle'],
                'items': items,
            }
        else:
            # Card grids: up to 6 articles
            previews[key] = {
                'key': key,
                'title': sec['title'],
                'subtitle': sec['subtitle'],
                'articles': articles[:6],
            }

    return {
        'banners': banner_images,
        'about': {
            'title': '关于我们',
            'text': about_intro,
            'image': about_images[0]['src'] if about_images else '',
            'link': '/about',
        },
        'previews': previews,
    }


def build_about_json():
    return {
        'title': '关于我们',
        'company': '济南德泓教育咨询有限公司',
        'paragraphs': [
            '济南德泓教育咨询有限公司是由济南市工商局批准成立的正规专业咨询教育机构，主要针对青少年厌学逃课、叛逆、早恋、自控力差、啃老、不懂感恩、自卑自恋、离家出走、人格异常、强迫、抑郁、打架斗殴、暴力倾向、亲情淡漠等常见问题。',
            '我们坚持以孩子为中心、以家庭为基础、走进孩子心灵、塑造健全人格为理念，把孩子培养成“五会”（即学会自理自立，学会如何学习，学会团结互助，学会为人处事，学会理解关心父母）“三恩”（即知恩，感恩，报恩）的阳光青少年。',
            '聘请国内及省内知名心理学、国学、书法家以及管理经验丰富的教务老师，根据孩子不同情况为每一位孩子制定不同的管理和解决方案，采取综合施教的方法，坚持一把钥匙开一把心锁。',
        ],
    }


def build_contact_json():
    return {
        'title': '联系我们',
        'company': '济南德泓教育咨询有限公司',
        'contacts': [
            {'label': '联系人', 'value': '林老师'},
            {'label': '手机', 'value': '13864188899、17615827726'},
            {'label': '微信', 'value': '17615827726'},
            {'label': '地址', 'value': '山东省济南市'},
        ],
        'form': {
            'title': 'ONLINE MESSAGE 在线留言',
            'fields': [
                {'label': '家长姓名', 'name': 'name'},
                {'label': '联系电话', 'name': 'phone'},
                {'label': '留言内容', 'name': 'message'},
            ],
        },
    }


def build_section_data(sec, sections_out_dir: Path):
    key = sec['key']
    sec_dir = DATA_DIR / key
    articles = []
    parsed_articles = {}

    list_dir = sec_dir / 'list'
    if list_dir.exists():
        for page_dir in sorted(list_dir.iterdir()):
            meta_path = page_dir / 'metadata.json'
            if not meta_path.exists():
                continue
            page_meta = json.loads(meta_path.read_text(encoding='utf-8'))
            # Copy list page images (skip boilerplate)
            page_num = page_meta.get('page_num', 1)
            for img in page_meta.get('images', []):
                if is_boilerplate_image(img['filename']):
                    continue
                src = page_dir / 'images' / img['filename']
                dest_prefix = f'sections/{key}/list/page_{page_num:02d}'
                dest = IMG_OUT_DIR / dest_prefix / img['filename']
                copy_image(src, dest)

            for art in page_meta.get('articles', []):
                article_id = art['id']
                content_path = sec_dir / 'articles' / article_id / 'content.txt'
                title = art['title']
                excerpt = ''
                date = ''
                parsed = None
                if content_path.exists():
                    parsed = parse_content_txt(content_path.read_text(encoding='utf-8'))
                    title = parsed['title'] or title
                    date = parsed['date']
                    excerpt = ' '.join(parsed['body'])[:160] if parsed['body'] else ''
                parsed_articles[article_id] = parsed

                # Find a representative image for the card from list page metadata
                # Prefer first non-boilerplate image whose alt matches the title.
                card_image = ''
                list_images = [
                    img for img in page_meta.get('images', [])
                    if not is_boilerplate_image(img['filename'])
                ]
                for img in list_images:
                    alt = img.get('alt', '').strip()
                    if alt and (alt == title or title.startswith(alt)):
                        card_image = f'/images/sections/{key}/list/page_{page_num:02d}/{img["filename"]}'
                        break
                if not card_image and list_images:
                    # Fallback to first non-boilerplate list image
                    img = list_images[0]
                    card_image = f'/images/sections/{key}/list/page_{page_num:02d}/{img["filename"]}'

                articles.append({
                    'id': article_id,
                    'title': title,
                    'date': date,
                    'excerpt': excerpt,
                    'image': card_image,
                    'path': f'/{key}/{article_id}',
                })

    # Build ordered article list for prev/next
    ordered_ids = [a['id'] for a in articles]

    # Copy article images (skip boilerplate) and write per-article JSON
    article_json_dir = sections_out_dir / key
    article_json_dir.mkdir(parents=True, exist_ok=True)
    art_base = sec_dir / 'articles'
    if art_base.exists():
        for art_dir in art_base.iterdir():
            article_id = art_dir.name
            meta_path = art_dir / 'metadata.json'
            if not meta_path.exists():
                continue
            art_meta = json.loads(meta_path.read_text(encoding='utf-8'))

            # Find the card image for this article to use as fallback
            card_image = ''
            for a in articles:
                if a['id'] == article_id:
                    card_image = a['image']
                    break

            # Copy non-boilerplate images
            article_images = []
            for img in art_meta.get('images', []):
                if is_boilerplate_image(img['filename']):
                    continue
                src = art_dir / 'images' / img['filename']
                dest_prefix = f'sections/{key}/articles/{article_id}'
                dest = IMG_OUT_DIR / dest_prefix / img['filename']
                if copy_image(src, dest):
                    article_images.append({
                        'src': f'/images/{dest_prefix}/{img["filename"]}',
                        'alt': img.get('alt', ''),
                    })

            # Fallback to card image if article has no inline images
            if not article_images and card_image:
                article_images.append({
                    'src': card_image,
                    'alt': '',
                })

            # Build detail JSON
            parsed = parsed_articles.get(article_id)
            if parsed:
                idx = ordered_ids.index(article_id) if article_id in ordered_ids else -1
                prev_id = ordered_ids[idx - 1] if idx > 0 else None
                next_id = ordered_ids[idx + 1] if idx >= 0 and idx < len(ordered_ids) - 1 else None
                detail = {
                    'id': article_id,
                    'title': parsed['title'],
                    'date': parsed['date'],
                    'clicks': parsed['clicks'],
                    'author': parsed['author'],
                    'section': key,
                    'sectionTitle': sec['title'],
                    'body': parsed['body'],
                    'images': article_images,
                    'prev': {'id': prev_id, 'title': articles[idx - 1]['title']} if prev_id else None,
                    'next': {'id': next_id, 'title': articles[idx + 1]['title']} if next_id else None,
                }
                (article_json_dir / f'{article_id}.json').write_text(
                    json.dumps(detail, ensure_ascii=False, indent=2), encoding='utf-8'
                )

    return {
        'key': key,
        'title': sec['title'],
        'subtitle': sec['subtitle'],
        'articles': articles,
    }


def main():
    # Clean previous generated data/images to avoid stale boilerplate duplicates
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    if IMG_OUT_DIR.exists():
        shutil.rmtree(IMG_OUT_DIR)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    IMG_OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Copy shared boilerplate images once, downloading any that are missing
    copy_common_boilerplate_images()
    ensure_boilerplate_images()

    site = build_site_json()
    (OUT_DIR / 'site.json').write_text(json.dumps(site, ensure_ascii=False, indent=2), encoding='utf-8')

    sections = build_sections_json()
    (OUT_DIR / 'sections.json').write_text(json.dumps(sections, ensure_ascii=False, indent=2), encoding='utf-8')

    about = build_about_json()
    (OUT_DIR / 'about.json').write_text(json.dumps(about, ensure_ascii=False, indent=2), encoding='utf-8')

    contact = build_contact_json()
    (OUT_DIR / 'contact.json').write_text(json.dumps(contact, ensure_ascii=False, indent=2), encoding='utf-8')

    # Build sections first so home.json can reference section previews
    sections_out_dir = OUT_DIR / 'sections'
    sections_out_dir.mkdir(parents=True, exist_ok=True)
    section_results = {}
    for sec in SECTIONS:
        data = build_section_data(sec, sections_out_dir)
        section_results[sec['key']] = data
        (sections_out_dir / f"{sec['key']}.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8'
        )
        print(f"Built section {sec['title']}: {len(data['articles'])} articles")

    # Build home.json after sections are ready
    home = build_home_json(section_results)
    (OUT_DIR / 'home.json').write_text(json.dumps(home, ensure_ascii=False, indent=2), encoding='utf-8')

    print('Preprocessing complete.')


if __name__ == '__main__':
    main()
