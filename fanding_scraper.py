"""
fanding.kr 포스트 수집 스크립트 (세상학개론 프로젝트)

실행:
    python fanding_scraper.py

구조:
    00_Posts/
      2026-06-16_포스트제목/
        post.md
        metadata.json
        images/
          image_001.jpg
        ocr/
          image_001.txt
"""

import asyncio
import json
import re
import os
from pathlib import Path
from datetime import datetime

# ================================
# 설정
# ================================
CONFIG = {
    "email": "REDACTED_EMAIL",
    "password": "REDACTED_PASSWORD",
    "creator_url": "https://fanding.kr/@sesang101/posts",
    "output_dir": "./00_Posts",
    "delay": 2,
    "headless": False,
    "ocr_enabled": False,  # True로 바꾸면 OCR 활성화 (나중에 별도 실행 권장)
}

# ================================
# OCR 설정 (선택적)
# ================================
OCR_AVAILABLE = False
if CONFIG["ocr_enabled"]:
    try:
        import pytesseract
        from PIL import Image
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        # 설치 확인
        ver = pytesseract.get_tesseract_version()
        langs = pytesseract.get_languages()
        print(f"✅ Tesseract {ver} | 언어팩: {langs}")
        OCR_AVAILABLE = "kor" in langs or "kor+eng" in " ".join(langs)
        if not OCR_AVAILABLE:
            print("⚠️  한국어 언어팩(kor) 없음 - 영어로만 OCR 시도")
            OCR_AVAILABLE = True
    except Exception as e:
        print(f"⚠️  OCR 비활성화: {e}")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("⚠️  requests 없음 - 이미지 다운로드 불가")


# ================================
# 유틸
# ================================
def slugify(text: str, max_len: int = 40) -> str:
    """제목을 폴더명으로 변환"""
    text = re.sub(r'[\\/*?:"<>|]', "", text)
    text = text.strip().replace(" ", "_")
    return text[:max_len] if text else "untitled"


def log(tag: str, msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}][{tag}] {msg}")


# ================================
# 이미지 파이프라인
# ================================
def normalize_image_url(src: str, base: str = "https://fanding.kr") -> str:
    """상대 URL → 절대 URL"""
    if not src:
        return ""
    src = src.strip().split(" ")[0]  # srcset에서 첫 번째 URL만
    if src.startswith("data:"):
        return ""  # base64 이미지 스킵
    if src.startswith("//"):
        return "https:" + src
    if src.startswith("/"):
        return base + src
    return src


def extract_image_urls(img_el_attrs: dict) -> str:
    """img 태그 속성에서 실제 이미지 URL 추출 (우선순위: data-src > src > srcset)"""
    for attr in ["data-src", "src", "srcset"]:
        val = img_el_attrs.get(attr, "")
        url = normalize_image_url(val)
        if url and url.startswith("http"):
            return url
    return ""


def download_image(url: str, save_path: Path, post_cookies: dict = None) -> dict:
    """이미지 다운로드 + 결과 로깅"""
    result = {
        "url": url,
        "save_path": str(save_path),
        "status": None,
        "content_type": None,
        "file_size": None,
        "success": False,
        "error": None,
    }
    if not REQUESTS_AVAILABLE or not url:
        result["error"] = "requests 미설치 또는 URL 없음"
        return result
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, timeout=15, headers=headers, cookies=post_cookies or {})
        result["status"] = resp.status_code
        result["content_type"] = resp.headers.get("content-type", "")

        if resp.status_code != 200:
            result["error"] = f"HTTP {resp.status_code}"
            return result

        save_path.parent.mkdir(parents=True, exist_ok=True)
        save_path.write_bytes(resp.content)
        result["file_size"] = len(resp.content)
        result["success"] = True
    except Exception as e:
        result["error"] = str(e)
    return result


def run_ocr(image_path: Path, ocr_dir: Path, img_name: str) -> dict:
    """OCR 실행 (선택적) - 결과를 txt 파일로 저장"""
    result = {"success": False, "text": "", "error": None, "txt_path": None}
    if not OCR_AVAILABLE:
        result["error"] = "OCR 비활성화"
        return result

    txt_path = ocr_dir / f"{img_name}.txt"
    result["txt_path"] = str(txt_path)

    try:
        img = Image.open(image_path)
        lang = "kor+eng" if OCR_AVAILABLE else "eng"
        text = pytesseract.image_to_string(img, lang=lang).strip()
        ocr_dir.mkdir(parents=True, exist_ok=True)
        txt_path.write_text(text, encoding="utf-8")
        result["success"] = True
        result["text"] = text
    except Exception as e:
        result["error"] = str(e)
        ocr_dir.mkdir(parents=True, exist_ok=True)
        txt_path.write_text(f"[OCR 실패: {e}]", encoding="utf-8")

    return result


# ================================
# 이미지 태그 전체 속성 추출
# ================================
async def extract_all_img_attrs(page) -> list:
    """페이지의 모든 img 태그 속성 추출"""
    return await page.evaluate("""() => {
        return Array.from(document.querySelectorAll('img')).map(img => ({
            src: img.getAttribute('src') || '',
            dataSrc: img.getAttribute('data-src') || '',
            srcset: img.getAttribute('srcset') || '',
            alt: img.getAttribute('alt') || '',
            className: img.className || '',
            width: img.naturalWidth || img.width || 0,
            height: img.naturalHeight || img.height || 0,
        }));
    }""")


# ================================
# 포스트 목록 수집
# ================================
async def get_post_links(page, creator_url: str) -> list:
    log("CRAWL", f"포스트 목록 수집: {creator_url}")
    await page.goto(creator_url)
    await page.wait_for_load_state("networkidle")
    await asyncio.sleep(CONFIG["delay"])

    posts = []
    prev_count = 0

    while True:
        links = await page.query_selector_all('a[href]')
        for link in links:
            href = await link.get_attribute("href") or ""
            if "/post/" not in href and "/@sesang101/" not in href:
                continue
            if href in ["/", creator_url]:
                continue
            full_url = f"https://fanding.kr{href}" if href.startswith("/") else href
            if not any(p["url"] == full_url for p in posts):
                title = ""
                try:
                    el = await link.query_selector("h3, h4, p, span")
                    if el:
                        title = (await el.inner_text()).strip()
                except:
                    pass
                posts.append({"url": full_url, "title": title})

        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(CONFIG["delay"])

        if len(posts) == prev_count:
            break
        prev_count = len(posts)
        log("CRAWL", f"  {len(posts)}개 발견...")

    log("CRAWL", f"총 {len(posts)}개 포스트 발견")
    return posts


# ================================
# 포스트 단건 스크래핑
# ================================
async def scrape_post(page, post_url: str, post_dir: Path) -> dict:
    images_dir = post_dir / "images"
    ocr_dir = post_dir / "ocr"
    images_dir.mkdir(parents=True, exist_ok=True)

    await page.goto(post_url)
    await page.wait_for_load_state("networkidle")
    await asyncio.sleep(CONFIG["delay"])

    metadata = {
        "url": post_url,
        "scraped_at": datetime.now().isoformat(),
        "title": "",
        "date": "",
        "body_text": "",
        "images": [],
    }

    # 제목
    try:
        el = await page.query_selector("h1, h2, .post-title")
        if el:
            metadata["title"] = (await el.inner_text()).strip()
    except:
        pass

    # 날짜
    try:
        el = await page.query_selector("time, .date, .created-at")
        if el:
            metadata["date"] = (await el.inner_text()).strip()
    except:
        pass

    # 본문 텍스트
    try:
        for sel in [".post-content", "article", ".content", "main"]:
            el = await page.query_selector(sel)
            if el:
                metadata["body_text"] = (await el.inner_text()).strip()
                break
    except:
        pass

    # ── 이미지 파이프라인 ──────────────────────────────────────
    log("IMG", f"이미지 태그 탐색 중...")
    all_imgs = await extract_all_img_attrs(page)
    log("IMG", f"img 태그 총 {len(all_imgs)}개 발견")

    skip_keywords = ["avatar", "logo", "icon", "emoji", "placeholder"]
    img_results = []
    img_counter = 0

    for attrs in all_imgs:
        # 디버그: 각 img 태그 출력
        log("IMG", f"  src={attrs['src'][:60]} | data-src={attrs['dataSrc'][:40]} | "
                   f"alt={attrs['alt'][:20]} | {attrs['width']}x{attrs['height']}")

        url = extract_image_urls({
            "src": attrs["src"],
            "data-src": attrs["dataSrc"],
            "srcset": attrs["srcset"],
        })

        if not url:
            log("IMG", f"    → URL 없음, 스킵")
            continue
        if any(kw in url.lower() for kw in skip_keywords):
            log("IMG", f"    → 스킵 키워드 ({url[:50]})")
            continue

        img_counter += 1
        img_name = f"image_{img_counter:03d}"
        ext = url.split("?")[0].rsplit(".", 1)[-1][:5].lower()
        if ext not in ["jpg", "jpeg", "png", "webp", "gif", "svg"]:
            ext = "jpg"
        filename = f"{img_name}.{ext}"
        save_path = images_dir / filename

        # 다운로드
        dl = download_image(url, save_path)
        log("IMG", f"    [{img_name}] HTTP={dl['status']} | "
                   f"type={dl['content_type']} | size={dl['file_size']} | "
                   f"{'✅' if dl['success'] else '❌ ' + str(dl['error'])}")

        # OCR (선택적 - 다운로드 성공한 경우만)
        ocr_result = {"success": False, "text": "", "error": "OCR 스킵", "txt_path": None}
        if dl["success"] and CONFIG["ocr_enabled"]:
            ocr_result = run_ocr(save_path, ocr_dir, img_name)
            log("OCR", f"    [{img_name}] {'✅ ' + str(len(ocr_result['text'])) + '자' if ocr_result['success'] else '❌ ' + str(ocr_result['error'])}")

        img_results.append({
            "index": img_counter,
            "name": img_name,
            "filename": filename,
            "url": url,
            "attrs": attrs,
            "download": dl,
            "ocr": ocr_result,
        })

    metadata["images"] = img_results
    return metadata


# ================================
# Markdown 생성
# ================================
def to_markdown(metadata: dict) -> str:
    lines = []
    lines.append("---")
    lines.append(f"source_url: {metadata['url']}")
    lines.append(f"date: {metadata['date']}")
    lines.append(f"scraped_at: {metadata['scraped_at']}")
    lines.append(f"image_count: {len(metadata['images'])}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {metadata['title'] or '(제목 없음)'}")
    lines.append("")

    if metadata["body_text"]:
        lines.append("## 본문")
        lines.append(metadata["body_text"])
        lines.append("")

    if metadata["images"]:
        lines.append("## 이미지")
        for img in metadata["images"]:
            name = img["name"]
            filename = img["filename"]
            dl = img["download"]
            ocr = img["ocr"]

            if dl["success"]:
                lines.append(f"![{name}](./images/{filename})")
            else:
                lines.append(f"<!-- 이미지 다운로드 실패: {img['url'][:80]} -->")
                lines.append(f"> ❌ 다운로드 실패: {dl['error']}")

            # OCR 결과
            if ocr["success"] and ocr["text"]:
                lines.append(f"<!-- OCR: ./ocr/{name}.txt -->")
                lines.append(f"> {ocr['text'][:200]}")
            elif ocr["error"] and ocr["error"] != "OCR 스킵":
                lines.append(f"> OCR 실패: {ocr['error']}")

            lines.append("")

    return "\n".join(lines)


# ================================
# 메인
# ================================
async def main():
    from playwright.async_api import async_playwright

    output_dir = Path(CONFIG["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    post_list_path = output_dir / "_post_list.json"

    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        context = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await context.new_page()

        # 수동 로그인
        await page.goto("https://fanding.kr/login")
        await page.wait_for_load_state("networkidle")

        print("\n" + "=" * 50)
        print("👆 브라우저에서 로그인을 완료해주세요.")
        print("   (네이버 소셜 로그인 → 인증 완료 → fanding.kr 메인 화면)")
        print("=" * 50)

        while True:
            await asyncio.get_event_loop().run_in_executor(None, input, "\n로그인 완료 후 Enter 키를 누르세요...")
            await asyncio.sleep(1)
            if "fanding.kr" in page.url and "/login" not in page.url:
                break
            print("⚠️  아직 로그인 전입니다. fanding.kr 메인까지 완료 후 Enter를 누르세요.")

        log("LOGIN", f"로그인 확인 - 크롤링 시작")

        # 포스트 목록 (캐시 우선)
        if post_list_path.exists():
            posts = json.loads(post_list_path.read_text(encoding="utf-8"))
            log("CACHE", f"저장된 포스트 목록 로드: {len(posts)}개 (새로 계산 안 함)")
            log("CACHE", "새 포스트 추가 시 _post_list.json 삭제 후 재실행하세요")
        else:
            posts = await get_post_links(page, CONFIG["creator_url"])
            post_list_path.write_text(json.dumps(posts, ensure_ascii=False, indent=2), encoding="utf-8")

        # 이미 수집된 폴더 목록
        existing_dirs = {d.name for d in output_dir.iterdir() if d.is_dir()}

        # OCR 미완료 확인
        needs_ocr = set()
        if CONFIG["ocr_enabled"] and OCR_AVAILABLE:
            for d in output_dir.iterdir():
                if not d.is_dir():
                    continue
                meta_path = d / "metadata.json"
                if not meta_path.exists():
                    continue
                try:
                    data = json.loads(meta_path.read_text(encoding="utf-8"))
                    for img in data.get("images", []):
                        if img["download"]["success"] and not img["ocr"]["success"]:
                            needs_ocr.add(d.name)
                            break
                except:
                    pass
            if needs_ocr:
                log("OCR", f"OCR 미완료 폴더: {len(needs_ocr)}개 → 재처리 예정")

        # 수집 시작
        print(f"\n📥 포스트 수집 시작... (총 {len(posts)}개)")
        for idx, post_meta in enumerate(posts):
            date_str = datetime.now().strftime("%Y-%m-%d")
            title_slug = slugify(post_meta.get("title", "") or f"post_{idx+1:04d}")
            folder_name = f"{date_str}_{title_slug}"
            post_dir = output_dir / folder_name

            # OCR 재처리
            if folder_name in needs_ocr:
                log("OCR", f"[{idx+1}/{len(posts)}] OCR 재처리: {folder_name}")
                try:
                    meta_path = post_dir / "metadata.json"
                    data = json.loads(meta_path.read_text(encoding="utf-8"))
                    for img in data["images"]:
                        if img["download"]["success"] and not img["ocr"]["success"]:
                            img_path = post_dir / "images" / img["filename"]
                            ocr_dir = post_dir / "ocr"
                            ocr_result = run_ocr(img_path, ocr_dir, img["name"])
                            img["ocr"] = ocr_result
                            log("OCR", f"  {img['name']}: {'✅' if ocr_result['success'] else '❌'}")
                    meta_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
                    (post_dir / "post.md").write_text(to_markdown(data), encoding="utf-8")
                except Exception as e:
                    log("OCR", f"  ❌ 재처리 실패: {e}")
                continue

            # 이미 완료된 폴더 스킵
            if folder_name in existing_dirs and (post_dir / "metadata.json").exists():
                log("SKIP", f"[{idx+1}/{len(posts)}] 스킵: {folder_name}")
                continue

            log("POST", f"[{idx+1}/{len(posts)}] 수집 중: {folder_name}")
            try:
                metadata = await scrape_post(page, post_meta["url"], post_dir)

                # metadata.json 저장
                (post_dir / "metadata.json").write_text(
                    json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
                )
                # post.md 저장
                (post_dir / "post.md").write_text(to_markdown(metadata), encoding="utf-8")

                img_ok = sum(1 for i in metadata["images"] if i["download"]["success"])
                img_total = len(metadata["images"])
                ocr_ok = sum(1 for i in metadata["images"] if i["ocr"]["success"])
                log("POST", f"  ✅ 완료 - 이미지 {img_ok}/{img_total}개 저장, OCR {ocr_ok}개")
                await asyncio.sleep(1)

            except Exception as e:
                log("POST", f"  ❌ 실패: {e}")
                continue

        await browser.close()

    print(f"\n🎉 완료! {output_dir}에 저장됨")


if __name__ == "__main__":
    asyncio.run(main())
