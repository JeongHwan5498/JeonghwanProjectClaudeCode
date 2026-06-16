# TASK_QUEUE.md
_최종 업데이트: 2026-06-16_

## 우선순위 기준
- P1: 지금 당장 필요
- P2: 곧 필요
- P3: 나중에

---

## TODO

| 우선순위 | 작업 | 메모 |
|---------|------|------|
| P1 | 실제 실행 후 포스트 수집 검증 | 포스트 수가 0이 나오는 이슈 재확인 필요 |
| P1 | 이미지 다운로드 성공률 확인 | lazy loading 처리 여부 검증 |
| P1 | post_id 체계 추가 | 현재 폴더명이 날짜+제목이라 WorldModel evidence 연결 불가. metadata.json에 post_id 필드 추가 필요 |
| P2 | `ocr_runner.py` 작성 | `00_Posts/` 순회하며 OCR만 별도 실행 |
| P2 | 포스트 본문 셀렉터 정확도 개선 | `.post-content` 등이 실제로 맞는지 확인 |
| P2 | `convert_to_markdown.py` 작성 | grok-4 Vision API로 이미지+본문 → 정제 마크다운 변환 스크립트 |
| P3 | Vision API 연동 설계 | 차트/표 이미지 → GPT-4o 또는 Claude Vision |
| P3 | 수집 결과 검색/조회 인터페이스 | 로컬 Markdown 뷰어 or 간단한 검색 스크립트 |

---

## DOING

| 작업 | 시작일 |
|------|--------|
| scraper.py 실행 및 검증 | 2026-06-16 |

---

## DONE

| 작업 | 완료일 |
|------|--------|
| Playwright 설치 및 Firefox 설정 | 2026-06-16 |
| 수동 로그인 → 자동 크롤링 구조 완성 | 2026-06-16 |
| 포스트별 폴더 구조 설계 | 2026-06-16 |
| 이미지 파이프라인 (src/data-src/srcset) | 2026-06-16 |
| OCR 선택적 분리 | 2026-06-16 |
| 포스트 목록 캐시 (_post_list.json) | 2026-06-16 |
| 재실행 안전성 (스킵/OCR 재처리) | 2026-06-16 |
| Tesseract 5.4.0 + 한국어 팩 설치 | 2026-06-16 |
| _ai_context 문서 구조 구축 | 2026-06-16 |
| GitHub 연동 (Private → Public 전환) | 2026-06-16 |

---

## BLOCKED

| 작업 | 이유 | 해제 조건 |
|------|------|----------|
| 소셜 로그인 자동화 | 추가 인증 발생으로 자동화 불가 | 해제 불필요 (수동으로 확정) |
| Chromium 사용 | spawn UNKNOWN 오류 | Firefox로 대체 완료 |
