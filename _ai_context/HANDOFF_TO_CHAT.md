# HANDOFF_TO_CHAT.md
_Claude Chat / GPT에 그대로 붙여넣을 수 있는 요약_
_최종 업데이트: 2026-06-16_

---

## 프로젝트 한 줄 요약

멤버십 플랫폼의 특정 크리에이터 유료 포스트를 자동 수집하여 투자 지식 베이스를 만드는 프로젝트.

---

## 현재 상태

Playwright(Firefox) + Python 3.8로 스크래퍼를 구현했고, 현재 실제 포스트 수집 단계에 있다.

**작동 방식**:
1. `python scraper.py` 실행
2. Firefox 브라우저가 열리고 플랫폼 로그인 페이지로 이동
3. 사용자가 직접 소셜 로그인 완료
4. 터미널에서 Enter → 자동으로 포스트 수집 시작
5. 결과는 `00_Posts/YYYY-MM-DD_제목/` 폴더에 저장

**Vision 변환 흐름**:
1. `python scraper.py` → `00_Posts/` 수집 완료
2. `.env` 파일에 `XAI_API_KEY=...` 설정
3. `python convert_to_markdown.py` → 각 포스트 폴더에 `post_refined.md` 생성

**저장 구조**:
```
00_Posts/
  _post_list.json           ← 포스트 목록 + post_id 캐시
  2026-06-16_포스트제목/
    post.md                 ← 원본 본문 (frontmatter에 post_id 포함)
    post_refined.md         ← grok-4 Vision 정제 결과
    metadata.json           ← post_id + 이미지 다운로드 결과 등 전체 메타데이터
    images/                 ← 원본 이미지
    ocr/                    ← OCR 결과 txt (현재 비활성화)
```

---

## 확정된 설계 결정

| 결정 | 이유 |
|------|------|
| 로그인은 수동으로 | 소셜 로그인 자동화 시 추가 인증 발생 |
| OCR은 현재 비활성화 | 차트/표 이미지는 OCR보다 Vision API가 적합, 나중에 별도 실행 |
| Firefox 사용 | Chromium이 Windows 환경에서 spawn UNKNOWN 오류 |
| 포스트 목록 캐시 | `_post_list.json` 저장, 재실행 시 재계산 안 함 |
| 재실행 안전 | 완료된 폴더 스킵, OCR 미완료만 재처리 |
| post_id 부여 | 폴더명(날짜+제목)만으론 WorldModel evidence 연결 불가 → post_0001~으로 고정 ID |
| Vision API: xAI grok-4 | convert_to_markdown.py로 이미지+본문 → 정제 마크다운 변환 |

---

## 지금 당장 해결이 필요한 것

1. **포스트 목록 수집 검증**: 실제 실행 시 포스트가 정상적으로 탐지되는지 확인
   - 과거에 `총 0개 포스트 발견` 이슈 있었음
2. **이미지 다운로드 성공률 확인**: lazy loading 처리 여부
3. **XAI_API_KEY 발급 후 convert_to_markdown.py 실행** 검증

---

## 다음 단계 (우선순위 순)

1. 실제 실행 → 포스트/이미지 수집 확인
2. `convert_to_markdown.py` 실행 (API 키 필요)
3. `ocr_runner.py` 작성 (수집된 이미지에 OCR만 별도 실행)

---

## 환경 정보

- OS: Windows 10
- Python: 3.8 (`C:\Program Files\Python38\python.exe`)
- 브라우저: Playwright Firefox
- OCR: Tesseract 5.4.0, 한국어 팩 포함
- Vision: xAI grok-4 (`https://api.x.ai/v1`) — `.env`에 `XAI_API_KEY` 필요
- GitHub: https://github.com/JeongHwan5498/JeonghwanProjectClaudeCode

---

## 핵심 파일

- `scraper.py` — 메인 스크래퍼 (post_id 자동 부여 포함)
- `convert_to_markdown.py` — grok-4 Vision으로 post_refined.md 생성
- `.env.example` — API 키 예시
- `00_Posts/_post_list.json` — 포스트 목록 캐시 (삭제하면 재수집)
- `_ai_context/` — 이 문서들이 있는 폴더
