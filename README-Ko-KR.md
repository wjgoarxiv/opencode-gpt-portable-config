# OpenCode 이식형 설정 (GPT-5.4 + Codex)

![Cover](cover.png)

복잡한 작업은 `gpt-5.4`, 코드/스크립트 작성 작업은 `gpt-5.3-codex`, 탐색/리서치 보조는 `gpt-5.3-codex-spark`로 라우팅하는 OpenCode/oh-my-opencode 설정입니다.

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
Please refer to [here](https://github.com/wjgoarxiv/opencode-gpt-portable-config). Clone or download this repo, then: (1) copy `opencode-configs/opencode.json` and `opencode-configs/oh-my-opencode.normal.json` into my OpenCode config path (`~/.config/opencode` on macOS/Linux, `%USERPROFILE%\.config\opencode` on Windows), renaming `oh-my-opencode.normal.json` to `oh-my-opencode.json`; (2) copy the fallback configs (`oh-my-opencode.spark-exhausted.json`, `oh-my-opencode.fallback.json`) and `switch-config.sh` into the same directory; (3) make `switch-config.sh` executable; (4) back up any existing files first; (5) run doctor/check and confirm complex model is `openai/gpt-5.4` and coding model is `openai/gpt-5.3-codex`.
```

macOS/Linux 기본 경로:

```bash
mkdir -p ~/.config/opencode
cp opencode-configs/opencode.json ~/.config/opencode/opencode.json
cp opencode-configs/oh-my-opencode.normal.json ~/.config/opencode/oh-my-opencode.json
cp opencode-configs/oh-my-opencode.spark-exhausted.json ~/.config/opencode/
cp opencode-configs/oh-my-opencode.fallback.json ~/.config/opencode/
cp opencode-configs/oh-my-opencode.normal.json ~/.config/opencode/
cp opencode-configs/switch-config.sh ~/.config/opencode/
chmod +x ~/.config/opencode/switch-config.sh
```

Windows (PowerShell) 기본 경로:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.config\opencode" | Out-Null
Copy-Item .\opencode-configs\opencode.json "$env:USERPROFILE\.config\opencode\opencode.json" -Force
Copy-Item .\opencode-configs\oh-my-opencode.normal.json "$env:USERPROFILE\.config\opencode\oh-my-opencode.json" -Force
Copy-Item .\opencode-configs\oh-my-opencode.spark-exhausted.json "$env:USERPROFILE\.config\opencode\" -Force
Copy-Item .\opencode-configs\oh-my-opencode.fallback.json "$env:USERPROFILE\.config\opencode\" -Force
Copy-Item .\opencode-configs\oh-my-opencode.normal.json "$env:USERPROFILE\.config\opencode\" -Force
Copy-Item .\opencode-configs\switch-config.sh "$env:USERPROFILE\.config\opencode\" -Force
```

## Fallback 시스템

OpenAI 장애/quota 소진에 대비한 3단계 fallback 시스템이 포함되어 있습니다.

> **중요:** OpenCode는 런타임 자동 폴백을 지원하지 않습니다. 문제 발생 시 아래 스크립트를 수동 실행한 후 OpenCode를 재시작해야 합니다.

### 작동 원리

```
                     ┌──────────────┐
                     │   NORMAL     │  ./switch-config.sh normal
                     │    (기본)     │
                     └──────┬───────┘
                            │
           ┌────────────────┴────────────────┐
           │                                 │
    ┌──────┴───────┐                ┌────────┴──────┐
    │  고성능 작업   │                │  빠른 작업     │
    │  gpt-5.4     │                │ gpt-5.3-codex │
    │  (400k ctx)  │                │    -spark      │
    └──────────────┘                │  (128k ctx)   │
                                    └───────────────┘
                            │
                     Spark quota 소진?
                            │ YES
                            ▼
              ┌────────────────────────┐
              │    SPARK-EXHAUSTED     │  ./switch-config.sh spark-exhausted
              │                        │
              │  spark 미사용 agent →    │
              │  gpt-5.3-codex (400k)  │
              └────────────┬───────────┘
                            │
                     OpenAI 장애?
                            │ YES
                            ▼
              ┌────────────────────────┐
              │      EMERGENCY         │  ./switch-config.sh emergency
              └────────────┬───────────┘
                            │
           ┌────────────────┴────────────────┐
           │                                 │
    ┌──────┴───────┐                ┌────────┴──────┐
    │  고성능 작업   │                │  빠른 작업     │
    │ kimi-k2.5    │                │  glm-4.7      │
    │   -free       │                │   -free        │
    │  (256k ctx)  │                │  (128k ctx)   │
    └──────────────┘                └───────────────┘

  복구 시: ./switch-config.sh normal → 원래 상태로 복원
```

```
  모드              비용     성능     가용성
  ──────────────────────────────────────────────────
  NORMAL            $$$$    ★★★★★   OpenAI 의존
  SPARK-EXHAUSTED   $$$     ★★★★    OpenAI 의존
  EMERGENCY         FREE    ★★★     독립 (Kimi/GLM)
```

### 언제 전환해야 하나요?

| 증상 | 조치 | 명령어 |
|------|------|--------|
| Spark agent가 quota 에러로 실패 | spark-exhausted로 전환 | `./switch-config.sh spark-exhausted` |
| 모든 OpenAI 호출이 429/500/503 반환 | emergency로 전환 | `./switch-config.sh emergency` |
| OpenAI 상태 페이지에 장애 표시 | emergency로 전환 | `./switch-config.sh emergency` |
| OpenAI 복구 / quota 리셋 | normal로 복원 | `./switch-config.sh normal` |

### 설정 파일

모든 fallback 설정은 `opencode-configs/` 디렉터리에 있습니다.

| 모드 | 설정 파일 | 모델 |
|------|-----------|------|
| **normal** | `oh-my-opencode.normal.json` | GPT-5.4 (복잡) + GPT-5.3 Codex (코딩) + Spark 보조 |
| **spark-exhausted** | `oh-my-opencode.spark-exhausted.json` | GPT-5.4 (복잡) + GPT-5.3 Codex (spark 미사용 agent) |
| **emergency** | `oh-my-opencode.fallback.json` | Kimi K2.5 Free + GLM 4.7 Free |

### 설치

Fallback 설정 파일과 전환 스크립트를 OpenCode 설정 디렉터리에 복사합니다:

```bash
cp opencode-configs/*.json ~/.config/opencode/
cp opencode-configs/switch-config.sh ~/.config/opencode/
chmod +x ~/.config/opencode/switch-config.sh
```

### 사용법

```bash
cd ~/.config/opencode

# 현재 모드 확인
./switch-config.sh status

# Spark quota 소진 시 → spark 미사용 agent를 Codex로
./switch-config.sh spark-exhausted

# OpenAI 장애 시 → Kimi/GLM 무료 티어로 전환
./switch-config.sh emergency

# 정상 복구 시
./switch-config.sh normal
```

### 비상 모델 매핑

| 기본 모델 | 비상 대체 모델 | 대상 Agent |
|-----------|---------------|------------|
| `gpt-5.4` | `kimi-k2.5-free` (256k ctx) | sisyphus, oracle, prometheus, metis, momus, atlas, plan |
| `gpt-5.3-codex` | `kimi-k2.5-free` (256k ctx) | hephaestus, multimodal-looker, frontend, writer |
| `gpt-5.3-codex-spark` | `glm-4.7-free` (128k ctx) | librarian, explore, sisyphus-junior, build, OpenCode-Builder |

## 검증 포인트

적용 후 OpenCode doctor/check를 실행하여 아래를 확인하세요.

- provider가 OpenAI인지
- 기본(복잡) 모델이 `gpt-5.4`로 해석되는지
- 코드/스크립트 모델이 `gpt-5.3-codex`로 해석되는지

## 보안

이 저장소에는 API 키/토큰을 포함하지 않습니다.
