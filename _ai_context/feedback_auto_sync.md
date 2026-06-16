---
name: auto-sync-on-session-end
description: 작업 종료 시 sync.ps1 자동 실행 규칙
metadata:
  type: feedback
---

작업이 끝날 때마다 Claude Code가 직접 `.\sync.ps1 "커밋메시지"`를 실행해서 _ai_context/ 변경사항을 GitHub에 push한다.
사용자가 수동으로 실행하지 않아도 됨.

**Why:** 사용자가 매번 수동 실행하는 번거로움을 없애기 위해 자동화 요청함.
**How to apply:** 세션에서 코드/문서 작업을 마칠 때마다 sync.ps1 실행. 경로: `C:\Users\user\Desktop\Claude Code\1. 세상학개론 프로젝트\sync.ps1`
