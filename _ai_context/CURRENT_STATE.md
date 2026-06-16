# CURRENT_STATE.md
_최종 업데이트: 2026-06-16_

## 현재 구현 상태

### 파일 구조
```
1. 세상학개론 프로젝트/
  fanding_scraper.py     ← 메인 스크래퍼 (현재 작동 중)
  login_debug.py         ← 로그인 세션 저장용 (현재는 미사용, scraper에 통합)
  00_Posts/              ← 포스트 저장 폴더 (수집 중)
    _post_list.json      ← 포스트 목록 캐시
    2026-06-16_제목/
      post.md
      metadata.json
      images/
      ocr/
  _ai_context/           ← AI 맥락 공유 폴더 (이 폴더)
```

## 완료된 기능

- [x] Playwright Firefox 기반 브라우저 자동화
- [x] 수동 네이버 소셜 로그인 → Enter 후 자동 크롤링
- [x] 포스트 목록 수집 + `_post_list.json` 캐시 (재실행 시 재계산 안 함)
- [x] 포스트별 폴더 구조 (`YYYY-MM-DD_제목/`)
- [x] 이미지 파이프라인: src/data-src/srcset 전부 탐색 + 다운로드 로깅
- [x] OCR 선택적 분리 (현재 `ocr_enabled: False` — 나중에 별도 실행)
- [x] 재실행 안전성: 완료된 폴더 스킵, OCR 미완료만 재처리
- [x] Tesseract 5.4.0 + 한국어 팩 설치 완료

## 현재 막힌 문제

- [ ] 포스트 목록 셀렉터(`a[href*="/post/"]`)가 실제 fanding.kr 구조와 맞는지 미확인
  - 실제 실행 후 `총 0개 포스트 발견` 이슈가 있었음
  - 현재 코드는 `/@sesang101/` 패턴도 포함하도록 수정됨 — 검증 필요
- [ ] 이미지 lazy loading 처리 미검증 (data-src가 실제로 채워지는지)

## 다음 작업 후보

1. 실제 실행하여 포스트 수집 검증
2. 이미지 다운로드 성공률 확인
3. OCR 별도 스크립트(`ocr_runner.py`) 작성
4. Vision API 연동 설계 (차트/표 이미지 해석)
