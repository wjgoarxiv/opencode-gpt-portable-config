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

One-line prompt for your LLM agent:

```text
Please refer to [here](https://github.com/wjgoarxiv/opencode-gpt-portable-config). Copy `opencode.json` and `oh-my-opencode.json` from this repository into my local OpenCode config path (`~/.config/opencode` on macOS/Linux, `%USERPROFILE%\\.config\\opencode` on Windows), back up existing files first, then run doctor/check and confirm default model is `openai/gpt-5.3-codex` and fast model is `openai/gpt-5.3-codex-spark`.
```

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

## Fallback Configs

This repo includes a 3-tier fallback system for OpenAI outage resilience. All fallback configs are in the `opencode-configs/` directory.

| Mode | Config File | Models |
|------|-------------|--------|
| **normal** | `oh-my-opencode.normal.json` | GPT-5.3 Codex + Spark (default) |
| **spark-exhausted** | `oh-my-opencode.spark-exhausted.json` | All agents use GPT-5.3 Codex |
| **emergency** | `oh-my-opencode.fallback.json` | Kimi K2.5 Free + GLM 4.7 Free |

### Setup

Copy fallback configs and the switch script to your OpenCode config directory:

```bash
cp opencode-configs/*.json ~/.config/opencode/
cp opencode-configs/switch-config.sh ~/.config/opencode/
chmod +x ~/.config/opencode/switch-config.sh
```

### Usage

```bash
cd ~/.config/opencode

# Check current mode
./switch-config.sh status

# Spark quota exhausted → all agents use Codex
./switch-config.sh spark-exhausted

# OpenAI down → switch to Kimi/GLM free tier
./switch-config.sh emergency

# Back to normal
./switch-config.sh normal
```

### Emergency Model Mapping

| Normal Model | Emergency Fallback | Agents |
|--------------|--------------------|--------|
| `gpt-5.3-codex` | `kimi-k2.5-free` (256k ctx) | sisyphus, hephaestus, oracle, prometheus, metis, momus, atlas, plan, frontend, writer |
| `gpt-5.3-codex-spark` | `glm-4.7-free` (128k ctx) | librarian, explore, sisyphus-junior, build, OpenCode-Builder |

> **Note:** OpenCode does not support runtime auto-fallback. Config switching is manual via the script above.

## Verify

Run OpenCode doctor/check after applying. Validate that:

- provider is OpenAI
- default heavy model resolves to `gpt-5.3-codex`
- fast/explore model resolves to `gpt-5.3-codex-spark`

## Security

This repo intentionally excludes API keys and tokens.
