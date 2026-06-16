# AI_RULES.md
_이 프로젝트에서 AI가 지켜야 할 행동 원칙_

---

## 절대 하면 안 되는 것

- `00_Posts/` 안의 원본 포스트 수정 금지
- 동의 없이 바로 실행 금지 — 항상 먼저 제안하고 승인받기
- 설계 변경을 코드로 먼저 구현하지 말 것
- WorldModel 파일을 overwrite하지 말 것 (merge만)

---

## 작업 전 반드시 할 것

- `CURRENT_STATE.md`와 `TASK_QUEUE.md` 먼저 읽기
- 이미 `DECISIONS.md`에 기각된 방향 다시 제안하지 말 것
- 불명확한 게 있으면 실행 전에 질문하기

---

## 작업 후 반드시 할 것

- `CODE_CHANGELOG.md` 업데이트
- `HANDOFF_TO_CHAT.md` 최신화
- 디버깅했으면 `DEBUG_LOG.md` 기록
