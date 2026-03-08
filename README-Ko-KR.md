# OpenCode 이식형 설정 (GPT-First)

![Cover](cover.png)

모든 작업을 OpenAI GPT-5.4로 직접 라우팅하는 OpenCode/oh-my-opencode 설정입니다. 속도가 중요한 작업은 GPT-5.3 Codex Spark를 사용하며, 3단계 fallback으로 완전한 복원력을 제공합니다.

## 파일 구성

- `opencode.json`
- `oh-my-opencode.json`
- `README.md`
- `README-Ko-KR.md`

## 새 PC 적용 방법

1. 기존 설정 파일을 백업합니다.
2. 이 저장소의 파일을 OpenCode 설정 디렉터리에 복사합니다.
3. doctor/check 명령으로 동작을 검증합니다.

LLM 에이전트용 원라인 프롬프트:

```text
Please refer to [here](https://github.com/wjgoarxiv/opencode-gpt-portable-config). Clone or download this repo, then: (1) copy `opencode-configs/opencode.json` and `opencode-configs/oh-my-opencode.normal.json` into my OpenCode config path (`~/.config/opencode` on macOS/Linux, `%USERPROFILE%\.config\opencode` on Windows), renaming `oh-my-opencode.normal.json` to `oh-my-opencode.json`; (2) copy all fallback configs (`oh-my-opencode.gpt-exhausted.json`, `oh-my-opencode.fallback.json`) and `switch-config.sh` into the same directory; (3) make `switch-config.sh` executable; (4) back up any existing files first; (5) run doctor/check and confirm all agents resolve to `openai/gpt-5.4`.
```

macOS/Linux 기본 경로:

```bash
mkdir -p ~/.config/opencode
cp opencode-configs/opencode.json ~/.config/opencode/opencode.json
cp opencode-configs/oh-my-opencode.normal.json ~/.config/opencode/oh-my-opencode.json
cp opencode-configs/oh-my-opencode.gpt-exhausted.json ~/.config/opencode/
cp opencode-configs/oh-my-opencode.fallback.json ~/.config/opencode/
cp opencode-configs/switch-config.sh ~/.config/opencode/
chmod +x ~/.config/opencode/switch-config.sh
```

Windows (PowerShell) 기본 경로:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.config\opencode" | Out-Null
Copy-Item .\opencode-configs\opencode.json "$env:USERPROFILE\.config\opencode\opencode.json" -Force
Copy-Item .\opencode-configs\oh-my-opencode.normal.json "$env:USERPROFILE\.config\opencode\oh-my-opencode.json" -Force
Copy-Item .\opencode-configs\oh-my-opencode.gpt-exhausted.json "$env:USERPROFILE\.config\opencode\" -Force
Copy-Item .\opencode-configs\oh-my-opencode.fallback.json "$env:USERPROFILE\.config\opencode\" -Force
Copy-Item .\opencode-configs\switch-config.sh "$env:USERPROFILE\.config\opencode\" -Force
```

## 모델 라우팅

### Normal 모드 Agent 라우팅

| Agent | 모델 | 용도 |
|-------|------|------|
| **sisyphus** | gpt-5.4 (max) | 오케스트레이터 |
| **hephaestus** | gpt-5.4 (medium) | 딥 실행자 |
| **oracle** | gpt-5.4 (high) | 아키텍처 / 난해한 문제 |
| **prometheus** | gpt-5.4 (max) | 전략 기획 |
| **metis** | gpt-5.4 (max) | 계획 검증 |
| **plan** | gpt-5.4 | 단계별 계획 수립 |
| **atlas** | gpt-5.4 | 작업 오케스트레이션 |
| **momus** | gpt-5.4 (medium) | 비평 |
| **document-writer** | gpt-5.4 | 장문 문서 작성 |
| **OpenCode-Builder** | gpt-5.4 | 프로젝트 스캐폴딩 |
| **frontend-ui-ux-engineer** | gpt-5.4 | 프론트엔드 / 스타일링 |
| **multimodal-looker** | gpt-5.4 | 멀티모달 워크플로 |
| **librarian** | gpt-5.3-codex | 문서 리서치 |
| **sisyphus-junior** | gpt-5.3-codex | 작업 실행 워커 |
| **explore** | gpt-5.3-codex-spark | 파일 스캔 / 검색 |
| **build** | gpt-5.3-codex-spark | 빌드 명령 |

## Fallback 시스템

OpenAI 장애에 대비한 3단계 fallback 시스템이 포함되어 있습니다.

> **중요:** OpenCode는 런타임 자동 폴백을 지원하지 않습니다. 문제 발생 시 아래 스크립트를 수동 실행한 후 OpenCode를 재시작해야 합니다.

### 작동 원리

```
┌─────────────────────────────────────────────────────┐
│                    NORMAL (기본)                     │
│         ./switch-config.sh normal                   │
│                                                     │
│  모든 thinking agent → GPT-5.4 (OpenAI direct)     │
│  리서치 / 워커        → GPT-5.3 Codex               │
│  빠른 검색 / 빌드     → GPT-5.3 Codex Spark         │
└─────────────────────┬───────────────────────────────┘
                      │
           OpenAI direct 할당량 소진?
                      │ YES
                      ▼
┌─────────────────────────────────────────────────────┐
│                 GPT-EXHAUSTED                       │
│         ./switch-config.sh gpt-exhausted            │
│                                                     │
│  모든 agent → GitHub Copilot only                  │
└─────────────────────┬───────────────────────────────┘
                      │
        OpenAI AND Copilot 모두 불가?
                      │ YES
                      ▼
┌─────────────────────────────────────────────────────┐
│                   EMERGENCY                         │
│         ./switch-config.sh emergency                │
│                                                     │
│  고성능 작업 → kimi-k2.5-free (256k ctx)            │
│  빠른 작업  → glm-4.7-free (128k ctx)              │
└─────────────────────────────────────────────────────┘

  복구 시: ./switch-config.sh normal → 원래 상태로 복원
```

```
  모드             비용     성능     가용성
  ─────────────────────────────────────────────
  NORMAL           $$+     ★★★★★   OpenAI direct
  GPT-EXHAUSTED    $$      ★★★★½   Copilot only
  EMERGENCY        FREE    ★★★     독립 (Kimi/GLM)
```

### 언제 전환해야 하나요?

| 증상 | 조치 | 명령어 |
|------|------|--------|
| OpenAI direct 429/500/503 | gpt-exhausted로 전환 | `./switch-config.sh gpt-exhausted` |
| 모든 OpenAI 호출 실패 | gpt-exhausted로 전환 | `./switch-config.sh gpt-exhausted` |
| OpenAI AND Copilot 모두 불가 | emergency로 전환 | `./switch-config.sh emergency` |
| OpenAI 복구 / quota 리셋 | normal로 복원 | `./switch-config.sh normal` |

### 설정 파일

| 모드 | 설정 파일 | 모델 |
|------|-----------|------|
| **normal** | `oh-my-opencode.normal.json` | GPT-5.4 (전체) · GPT-5.3 Codex Spark (빠른 작업) |
| **gpt-exhausted** | `oh-my-opencode.gpt-exhausted.json` | GitHub Copilot 전체 |
| **emergency** | `oh-my-opencode.fallback.json` | Kimi K2.5 Free + GLM 4.7 Free |

### 설치

```bash
cp opencode-configs/oh-my-opencode.gpt-exhausted.json ~/.config/opencode/
cp opencode-configs/oh-my-opencode.fallback.json ~/.config/opencode/
cp opencode-configs/switch-config.sh ~/.config/opencode/
chmod +x ~/.config/opencode/switch-config.sh
```

### 사용법

```bash
cd ~/.config/opencode

# 현재 모드 확인
./switch-config.sh status

# OpenAI direct 할당량 소진 → Copilot으로 전환
./switch-config.sh gpt-exhausted

# OpenAI AND Copilot 모두 불가 → Kimi/GLM 무료 티어로 전환
./switch-config.sh emergency

# 정상 복구 시
./switch-config.sh normal
```

### 비상 모델 매핑

| 기본 모델 | 비상 대체 모델 | 대상 Agent |
|-----------|---------------|------------|
| `gpt-5.4` | `kimi-k2.5-free` (256k ctx) | sisyphus, oracle, prometheus, metis, momus, atlas, plan, hephaestus, multimodal-looker, frontend-ui-ux-engineer, document-writer |
| `gpt-5.3-codex`, `gpt-5.3-codex-spark` | `glm-4.7-free` (128k ctx) | librarian, explore, sisyphus-junior, build, OpenCode-Builder |

## 검증 포인트

적용 후 OpenCode doctor/check를 실행하여 아래를 확인하세요.

- `sisyphus`가 `openai/gpt-5.4`로 해석되는지
- `hephaestus`가 `openai/gpt-5.4`로 해석되는지
- `explore`가 `openai/gpt-5.3-codex-spark`로 해석되는지
- `build`가 `openai/gpt-5.3-codex-spark`로 해석되는지

## 보안

이 저장소에는 API 키/토큰을 포함하지 않습니다.
