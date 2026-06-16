# CODE_CHANGELOG.md

---

## [2026-06-16] 초기 버전 → 현재 버전 (대규모 리팩토링)

### 수정 파일: `fanding_scraper.py`

| 변경 항목 | 내용 |
|----------|------|
| 타입 힌트 | `list[dict]` → `list` (Python 3.8 호환) |
| 브라우저 | `chromium` → `firefox` |
| 로그인 | 자동 로그인 → 수동 로그인 + Enter 대기 |
| 폴더 구조 | `post_0001.md` → `YYYY-MM-DD_제목/post.md` |
| 이미지 탐색 | `src`만 → `src + data-src + srcset` 전부 |
| 이미지 로깅 | 없음 → HTTP status/content-type/파일크기 로그 |
| OCR | 필수 포함 → 선택적 분리 (`ocr_enabled: False`) |
| 포스트 목록 | 매번 재계산 → `_post_list.json` 캐시 |
| 재실행 | 없음 → 완료 폴더 스킵 + OCR 미완료 재처리 |
| OCR 저장 | 본문 인라인 → `ocr/image_001.txt` 별도 저장 |

### 수정 파일: `login_debug.py`

- 초기: 자동 네이버 로그인 디버깅 스크립트
- 현재: 수동 로그인 + Enter 후 세션 저장 (현재는 scraper에 통합되어 미사용)

### 설치한 패키지/도구

```
pip install playwright pillow pytesseract requests
python -m playwright install firefox
winget install UB-Mannheim.TesseractOCR
# kor.traineddata 한국어 팩 수동 설치
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

### GitHub 연동 [2026-06-16]

- `_ai_context/` 폴더만 추적, 나머지 전부 .gitignore 제외
- remote: https://github.com/JeongHwan5498/JeonghwanProjectClaudeCode
- `sync.ps1`: 작업 종료 시 자동 커밋 + push 스크립트
- Claude Code가 작업 종료 시 자동으로 실행

### 실행 방법

```powershell
cd "C:\Users\user\Desktop\Claude Code\1. 세상학개론 프로젝트"
python fanding_scraper.py
# 브라우저에서 네이버 소셜 로그인 완료 후 Enter
```

### 테스트 결과

- 로그인: ✅ 수동 로그인 후 Enter로 정상 진행 확인
- 포스트 목록: 🔄 실제 수집 수 미검증
- 이미지 다운로드: 🔄 실제 실행 후 확인 필요
- OCR: ✅ Tesseract 작동 확인, 현재 비활성화 상태
- GitHub push: ✅ master 브랜치 연결 완료
