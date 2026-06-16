# PROJECT_BRIEF.md

## 프로젝트 목적

멤버십 플랫폼의 특정 크리에이터 유료 포스트를 자동으로 수집하여
투자 지식 베이스를 구축하는 프로젝트.

## 핵심 철학

- **이미지 보존 우선**: OCR 완벽 구현보다 원본 이미지 누락 없이 저장하는 것이 먼저
- **단계별 처리**: 수집 → 이미지 저장 → OCR → Vision 해석 순으로 분리
- **재실행 안전성**: 중간에 멈춰도 이미 한 작업은 다시 하지 않음
- **자동화 범위 현실적으로**: 소셜 로그인 자동화는 하지 않음 (추가 인증 등 불확실성)

## 최종 목표

```
1차: 포스트 텍스트 + 이미지 원본 완전 수집
2차: OCR 가능한 이미지만 텍스트 추출
3차: 차트/표 이미지는 GPT/Claude Vision으로 해석
4차: 이미지 해석 결과를 post.md에 통합
```

## 중요한 제약사항

- 대상 플랫폼 로그인은 **소셜 로그인** → 자동화 불가 (추가 인증 발생)
- 로그인은 수동으로 하고, 그 이후 크롤링만 자동화
- Python 3.8 환경 (`C:\Program Files\Python38\python.exe`)
- playwright는 `C:\Users\user\AppData\Roaming\Python\Python38\site-packages\` 에 설치됨
- Tesseract OCR 5.4.0 설치됨 (`C:\Program Files\Tesseract-OCR\tesseract.exe`), 한국어 팩 포함

## 수집 대상

- 분야: 투자 (주가 차트, 데이터센터, GPU 공급망, 실적표, 애널리스트 리포트 등)
