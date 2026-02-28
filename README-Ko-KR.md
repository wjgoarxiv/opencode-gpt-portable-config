# OpenCode 이식형 설정 (Codex + Spark)

무거운 작업은 `gpt-5.3-codex`, 빠른 작업은 `gpt-5.3-codex-spark`로 라우팅하는 OpenCode/oh-my-opencode 설정입니다.

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
이 저장소의 `opencode.json`과 `oh-my-opencode.json`을 내 로컬 OpenCode 설정 경로(macOS/Linux: `~/.config/opencode`, Windows: `%USERPROFILE%\\.config\\opencode`)에 복사하고, 기존 파일은 먼저 백업한 뒤 doctor/check를 실행해서 기본 모델이 `openai/gpt-5.3-codex`, 빠른 모델이 `openai/gpt-5.3-codex-spark`로 설정되었는지 확인해줘.
```

macOS/Linux 기본 경로:

```bash
mkdir -p ~/.config/opencode
cp opencode.json ~/.config/opencode/opencode.json
cp oh-my-opencode.json ~/.config/opencode/oh-my-opencode.json
```

Windows (PowerShell) 기본 경로:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.config\opencode" | Out-Null
Copy-Item .\opencode.json "$env:USERPROFILE\.config\opencode\opencode.json" -Force
Copy-Item .\oh-my-opencode.json "$env:USERPROFILE\.config\opencode\oh-my-opencode.json" -Force
```

## 검증 포인트

적용 후 OpenCode doctor/check를 실행하여 아래를 확인하세요.

- provider가 OpenAI인지
- 기본(고성능) 모델이 `gpt-5.3-codex`로 해석되는지
- 빠른 작업 모델이 `gpt-5.3-codex-spark`로 해석되는지

## 보안

이 저장소에는 API 키/토큰을 포함하지 않습니다.
