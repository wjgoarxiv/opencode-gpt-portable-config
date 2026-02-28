# OpenCode Portable Config (Codex + Spark)

Portable OpenCode/oh-my-opencode settings that route heavy tasks to `gpt-5.3-codex` and fast tasks to `gpt-5.3-codex-spark`.

## Files

- `opencode.json`
- `oh-my-opencode.json`
- `README.md`
- `README-Ko-KR.md`

## Apply On a New Machine

1. Back up existing files.
2. Copy these files into your OpenCode config directory.
3. Run doctor/check commands.

macOS/Linux default path:

```bash
mkdir -p ~/.config/opencode
cp opencode.json ~/.config/opencode/opencode.json
cp oh-my-opencode.json ~/.config/opencode/oh-my-opencode.json
```

Windows (PowerShell) default path:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.config\opencode" | Out-Null
Copy-Item .\opencode.json "$env:USERPROFILE\.config\opencode\opencode.json" -Force
Copy-Item .\oh-my-opencode.json "$env:USERPROFILE\.config\opencode\oh-my-opencode.json" -Force
```

## Verify

Run OpenCode doctor/check after applying. Validate that:

- provider is OpenAI
- default heavy model resolves to `gpt-5.3-codex`
- fast/explore model resolves to `gpt-5.3-codex-spark`

## Security

This repo intentionally excludes API keys and tokens.
