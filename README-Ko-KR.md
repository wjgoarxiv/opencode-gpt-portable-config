# OpenCode 이식형 설정

![Cover](cover.png)

이 저장소는 현재 로컬에서 쓰는 OpenCode / oh-my-openagent 설정을 이식형으로 정리한 것입니다. 기준 프로파일은 세 가지입니다.

- `gptglm`: `GPT-5.5 + GLM-5.1`
- `gptonly`: `GPT-5.5 only`
- `gptollama`: `GPT-5.5 + local Ollama gemma4:e4b`

예전 `normal / gpt-exhausted / emergency` 체계는 이 저장소에서 더 이상 기준으로 쓰지 않습니다.

## 파일 구성

- `opencode.json`
- `oh-my-openagent.json`
- `opencode-configs/opencode.json`
- `opencode-configs/oh-my-openagent.gptglm.json`
- `opencode-configs/oh-my-openagent.gptonly.json`
- `opencode-configs/oh-my-openagent.gptollama.json`
- `opencode-configs/switch-config.sh`
- `opencode-configs/oa-switch`

## 새 PC 적용 방법

macOS/Linux:

```bash
mkdir -p ~/.config/opencode
cp opencode-configs/opencode.json ~/.config/opencode/opencode.json
cp opencode-configs/oh-my-openagent.gptglm.json ~/.config/opencode/oh-my-openagent.gptglm.json
cp opencode-configs/oh-my-openagent.gptonly.json ~/.config/opencode/oh-my-openagent.gptonly.json
cp opencode-configs/oh-my-openagent.gptollama.json ~/.config/opencode/oh-my-openagent.gptollama.json
cp opencode-configs/oh-my-openagent.gptglm.json ~/.config/opencode/oh-my-openagent.json
cp opencode-configs/switch-config.sh ~/.config/opencode/switch-config.sh
cp opencode-configs/oa-switch ~/.local/bin/oa-switch
chmod +x ~/.config/opencode/switch-config.sh
chmod +x ~/.local/bin/oa-switch
```

Windows (PowerShell):

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.config\opencode" | Out-Null
Copy-Item .\opencode-configs\opencode.json "$env:USERPROFILE\.config\opencode\opencode.json" -Force
Copy-Item .\opencode-configs\oh-my-openagent.gptglm.json "$env:USERPROFILE\.config\opencode\oh-my-openagent.gptglm.json" -Force
Copy-Item .\opencode-configs\oh-my-openagent.gptonly.json "$env:USERPROFILE\.config\opencode\oh-my-openagent.gptonly.json" -Force
Copy-Item .\opencode-configs\oh-my-openagent.gptollama.json "$env:USERPROFILE\.config\opencode\oh-my-openagent.gptollama.json" -Force
Copy-Item .\opencode-configs\oh-my-openagent.gptglm.json "$env:USERPROFILE\.config\opencode\oh-my-openagent.json" -Force
Copy-Item .\opencode-configs\switch-config.sh "$env:USERPROFILE\.config\opencode\switch-config.sh" -Force
```

## 프로파일 설명

### `gptglm`

- 고난도 reasoning agent: `openai/gpt-5.5`
- 빠른 검색 / 리서치 / 워커 계열: `zai-coding-plan/glm-5.1`

### `gptonly`

- 모든 agent와 category를 `openai/gpt-5.5`로 통일

### `gptollama`

- 고난도 reasoning agent: `openai/gpt-5.5`
- 빠른 검색 / 리서치 / 워커 계열: `ollama/gemma4:e4b`
- `opencode.json`에 로컬 Ollama provider 설정이 필요

## 전환 방법

`~/.config/opencode`에서:

```bash
./switch-config.sh gptglm
./switch-config.sh gptonly
./switch-config.sh gptollama
./switch-config.sh status
```

래퍼 스크립트를 써도 되고, alias로 써도 됩니다.

래퍼 스크립트를 설치했다면:

```bash
oa-switch gptglm
oa-switch gptonly
oa-switch gptollama
oa-switch status
```

또는 alias:

```bash
alias oa-switch="$HOME/.config/opencode/switch-config.sh"
```

그다음부터는:

```bash
oa-switch gptglm
oa-switch gptonly
oa-switch gptollama
oa-switch status
```

## 스크립트가 하는 일

`switch-config.sh`는 활성 파일을 바꿉니다.

- `gptglm` -> `oh-my-openagent.gptglm.json`을 `oh-my-openagent.json`으로 복사
- `gptonly` -> `oh-my-openagent.gptonly.json`을 `oh-my-openagent.json`으로 복사
- `gptollama` -> `oh-my-openagent.gptollama.json`을 `oh-my-openagent.json`으로 복사
- `status` -> 현재 활성 파일에 `glm-5.1` 또는 `ollama/gemma4:e4b`가 있는지 확인

## 이식형 `opencode.json`

이 저장소의 `opencode.json`은 이식성을 우선합니다.

- `oh-my-openagent@latest` 포함
- `opencode-openai-codex-auth` 포함
- OpenAI 모델 정의: `gpt-5.5`, `gpt-5.3-codex`, `gpt-5.3-codex-spark`
- 보조 provider 정의: `kimi-k2.5-free`, `glm-4.7-free`
- 로컬 Ollama provider 정의: `gemma4:e4b`

로컬 전용 플러그인 경로는 일부러 넣지 않았습니다.

## 멀티모달 capability 메모

이 저장소의 provider 모델 정의는 OpenCode에서 해당 모델이 실제로 노출하는 비텍스트 입력 capability를 명시합니다.

| 모델 | 입력 modality |
| --- | --- |
| `openai/gpt-5.5` | `text`, `image`, `pdf` |
| `openai/gpt-5.3-codex` | `text`, `image`, `pdf` |
| `openai/gpt-5.3-codex-spark` | `text`, `image`, `pdf` |
| `opencode/kimi-k2.5-free` | `text`, `image`, `video` |
| `ollama/gemma4:e4b` | `text`, `image` |
| `opencode/glm-4.7-free` | `text` only |

다른 PC로 동기화할 때 이 항목들을 다시 `input: ["text"]`로 줄이면 안 됩니다. OpenCode는 이 metadata를 보고 이미지/PDF/video 입력을 모델에 보낼지, 아니면 text-only 오류로 대체할지 결정합니다.

## 검증

복사 후:

```bash
cd ~/.config/opencode
./switch-config.sh status
```

다음을 확인하면 됩니다.

- `gptglm` 전환 시 `GPTGLM mode`
- `gptonly` 전환 시 `GPTONLY mode`
- `gptollama` 전환 시 `GPTOLLAMA mode`
- `oh-my-openagent.json` 내용이 함께 바뀜

## 보안

이 저장소에는 API 키, 토큰, 머신 종속 로컬 플러그인 경로를 포함하지 않습니다.
