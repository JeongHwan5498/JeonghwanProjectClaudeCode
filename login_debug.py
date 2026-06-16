"""
fanding.kr 로그인 세션 저장 스크립트

실행 후 브라우저에서 직접 로그인하면 세션이 저장됩니다.
저장된 세션은 fanding_scraper.py에서 재사용됩니다.

실행:
    python login_debug.py
"""

import asyncio
from pathlib import Path
from datetime import datetime


AUTH_DIR = Path("./auth")
STATE_PATH = AUTH_DIR / "storageState.json"


def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def is_logged_in(url: str) -> bool:
    return "fanding.kr" in url and "/login" not in url


async def main():
    from playwright.async_api import async_playwright

    AUTH_DIR.mkdir(exist_ok=True)

    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            # 팝업 허용
            java_script_enabled=True,
        )
        page = await context.new_page()

        log("브라우저를 열었습니다. fanding.kr 로그인 페이지로 이동합니다...")
        await page.goto("https://fanding.kr/login")
        await page.wait_for_load_state("networkidle")

        log("=" * 50)
        log("👆 브라우저에서 직접 로그인해주세요.")
        log("   네이버 소셜 로그인 → ID/PW 입력 → 추가 인증 완료")
        log("   로그인 완료 후 이 터미널에서 Enter 키를 누르세요.")
        log("=" * 50)

        # 사용자가 로그인 완료 후 Enter 누를 때까지 반복 대기
        while True:
            await asyncio.get_event_loop().run_in_executor(None, input, "\n로그인 완료 후 Enter 키를 누르세요...")
            await asyncio.sleep(1)
            cur_url = page.url
            log(f"현재 URL: {cur_url}")
            if "fanding.kr" in cur_url and "/login" not in cur_url:
                break
            log("⚠️  아직 로그인 전입니다. fanding.kr 메인 화면까지 완료한 후 Enter를 누르세요.")

        log(f"✅ 로그인 확인! URL: {page.url}")
        await context.storage_state(path=str(STATE_PATH))
        log(f"💾 세션 저장 완료: {STATE_PATH}")
        log("이제 fanding_scraper.py를 실행하면 로그인 없이 크롤링됩니다.")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
