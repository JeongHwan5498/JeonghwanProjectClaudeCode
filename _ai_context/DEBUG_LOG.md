# DEBUG_LOG.md

---

## [2026-06-16] Python 3.8 타입 힌트 오류

**에러**: `TypeError: 'type' object is not subscriptable`
**위치**: `scraper.py` — `list[dict]` 타입 힌트
**원인**: Python 3.8은 `list[dict]` 문법 미지원 (3.9+에서 가능)
**해결**: `list[dict]` → `list` 로 변경
**결과**: ✅ 해결

---

## [2026-06-16] Playwright Chromium spawn UNKNOWN 오류

**에러**: `BrowserType.launch: spawn UNKNOWN`
**원인**: Windows 환경에서 Playwright Chromium 실행 파일이 `side-by-side configuration` 오류
**시도한 것**:
1. Visual C++ 재배포 패키지 설치 → 미해결
2. DLL 존재 확인 (msvcp140.dll 등) → 모두 존재, 무관
3. Firefox로 전환 → ✅ 해결
**결과**: Firefox 사용으로 확정

---

## [2026-06-16] playwright install 경로 불일치

**에러**: `Executable doesn't exist at C:\...\firefox-1465\firefox\firefox.exe`
**원인**: Claude Code 환경의 Python과 PowerShell의 Python이 달라 각각 다른 위치에 설치됨
**해결**: 사용자가 PowerShell에서 직접 `python -m playwright install firefox` 실행
**결과**: ✅ 해결

---

## [2026-06-16] 포스트 목록 0개 수집

**에러**: `총 0개 포스트 발견`
**원인**: 로그인이 실제로 실패했지만 URL 체크 조건이 통과됨
  - 로그인 후 OAuth 페이지로 리다이렉트됐는데 URL 체크 로직이 이를 통과시킴
  - 그 상태에서 포스트 목록 페이지 접근 → 다시 로그인 페이지로 리다이렉트
**해결**: 로그인 구조를 수동 로그인으로 전환 (사용자가 직접 로그인 후 Enter)
**결과**: ✅ 해결 (로그인 성공 확인됨)

---

## [2026-06-16] 소셜 로그인 버튼 탐색 실패

**에러**: 소셜 로그인 버튼 탐색 실패
**원인**:
- 플랫폼 로그인 버튼이 모달 형태 — "Log In" 버튼 클릭 후 모달이 열림
- 소셜 로그인 버튼들이 모두 동일한 class이고 텍스트/aria-label 없음
- SVG 아이콘만 있어 키워드 탐색 불가
**결론**: 소셜 로그인 자동화는 추가 인증 문제로 포기, 수동 로그인으로 확정

---

## [2026-06-16] OCR 작동 안 함 (Tesseract 미설치)

**에러**: OCR 결과 없음
**원인**: pytesseract는 Python 래퍼, 실제 Tesseract 바이너리가 별도 필요
**해결**:
1. `winget install UB-Mannheim.TesseractOCR` 설치
2. 한국어 팩 `kor.traineddata` 다운로드 (관리자 권한 필요)
3. 코드에 `pytesseract.pytesseract.tesseract_cmd` 경로 추가
**결과**: ✅ Tesseract 5.4.0 작동 확인
**추가 결정**: OCR은 스크래핑과 분리, 현재 `ocr_enabled: False`
