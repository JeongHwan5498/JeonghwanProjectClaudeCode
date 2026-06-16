# CURRENT_STATE.md
_최종 업데이트: 2026-06-16_

## 현재 구현 상태

### 파일 구조
```
프로젝트 루트/
  scraper.py             ← 메인 스크래퍼 (현재 작동 중)
  convert_to_markdown.py ← grok-4 Vision으로 post_refined.md 생성
  login_debug.py         ← 로그인 세션 저장용 (현재는 미사용, scraper에 통합)
  .env.example           ← API 키 예시 (실제 .env는 gitignore)
  00_Posts/              ← 포스트 저장 폴더 (수집 중)
    _post_list.json      ← 포스트 목록 캐시 (post_id 포함)
    2026-06-16_제목/
      post.md            ← 원본 본문 + 이미지 링크 (frontmatter에 post_id 포함)
      post_refined.md    ← grok-4 Vision 정제 결과 (convert_to_markdown.py 실행 후 생성)
      metadata.json      ← 전체 메타데이터 (post_id 포함)
      images/
      ocr/
  _ai_context/           ← AI 맥락 공유 폴더 (이 폴더)
```

## 완료된 기능

- [x] Playwright Firefox 기반 브라우저 자동화
- [x] 수동 소셜 로그인 → Enter 후 자동 크롤링
- [x] 포스트 목록 수집 + `_post_list.json` 캐시 (재실행 시 재계산 안 함)
- [x] **post_id 자동 부여** (post_0001, post_0002... → _post_list.json, metadata.json, post.md에 포함)
- [x] 포스트별 폴더 구조 (`YYYY-MM-DD_제목/`)
- [x] 이미지 파이프라인: src/data-src/srcset 전부 탐색 + 다운로드 로깅
- [x] OCR 선택적 분리 (현재 `ocr_enabled: False` — 나중에 별도 실행)
- [x] 재실행 안전성: 완료된 폴더 스킵, OCR 미완료만 재처리
- [x] Tesseract 5.4.0 + 한국어 팩 설치 완료
- [x] **convert_to_markdown.py** — xAI grok-4 Vision으로 post_refined.md 생성
- [x] **.env.example** 추가 (XAI_API_KEY)

## 현재 막힌 문제

- [ ] 포스트 목록 셀렉터가 실제 플랫폼 구조와 맞는지 미확인
  - 실제 실행 후 `총 0개 포스트 발견` 이슈가 있었음
  - 현재 코드는 복수 패턴 포함하도록 수정됨 — 검증 필요
- [ ] 이미지 lazy loading 처리 미검증 (data-src가 실제로 채워지는지)

## 다음 작업 후보

1. 실제 실행하여 포스트/이미지 수집 검증
2. `convert_to_markdown.py` 실제 실행 (XAI_API_KEY 필요)
3. OCR 별도 스크립트(`ocr_runner.py`) 작성
