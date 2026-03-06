# OpenCode Portable Config (GPT-5.4 + Codex)

![Cover](cover.png)

Portable OpenCode/oh-my-opencode settings that route complex tasks to `gpt-5.4`, code/script tasks to `gpt-5.3-codex`, and search helpers to `gpt-5.3-codex-spark`.

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
Please refer to [here](https://github.com/wjgoarxiv/opencode-gpt-portable-config). Clone or download this repo, then: (1) copy `opencode-configs/opencode.json` and `opencode-configs/oh-my-opencode.normal.json` into my OpenCode config path (`~/.config/opencode` on macOS/Linux, `%USERPROFILE%\.config\opencode` on Windows), renaming `oh-my-opencode.normal.json` to `oh-my-opencode.json`; (2) copy the fallback configs (`oh-my-opencode.spark-exhausted.json`, `oh-my-opencode.fallback.json`) and `switch-config.sh` into the same directory; (3) make `switch-config.sh` executable; (4) back up any existing files first; (5) run doctor/check and confirm complex model is `openai/gpt-5.4` and coding model is `openai/gpt-5.3-codex`.
```

macOS/Linux default path:

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

Windows (PowerShell) default path:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.config\opencode" | Out-Null
Copy-Item .\opencode-configs\opencode.json "$env:USERPROFILE\.config\opencode\opencode.json" -Force
Copy-Item .\opencode-configs\oh-my-opencode.normal.json "$env:USERPROFILE\.config\opencode\oh-my-opencode.json" -Force
Copy-Item .\opencode-configs\oh-my-opencode.spark-exhausted.json "$env:USERPROFILE\.config\opencode\" -Force
Copy-Item .\opencode-configs\oh-my-opencode.fallback.json "$env:USERPROFILE\.config\opencode\" -Force
Copy-Item .\opencode-configs\oh-my-opencode.normal.json "$env:USERPROFILE\.config\opencode\" -Force
Copy-Item .\opencode-configs\switch-config.sh "$env:USERPROFILE\.config\opencode\" -Force
```

## Fallback System

This repo includes a 3-tier fallback system for OpenAI outage resilience.

> **Important:** OpenCode does not support runtime auto-fallback. You must manually run the switch script when issues occur, then restart OpenCode.

### How It Works

```
                     ┌──────────────┐
                     │   NORMAL     │  ./switch-config.sh normal
                     │   (default)  │
                     └──────┬───────┘
                            │
           ┌────────────────┴────────────────┐
           │                                 │
    ┌──────┴───────┐                ┌────────┴──────┐
    │  Heavy Tasks  │                │  Fast Tasks    │
    │  gpt-5.4     │                │ gpt-5.3-codex │
    │  (1.05M ctx) │                │    -spark      │
    └──────────────┘                │  (128k ctx)   │
                                    └───────────────┘
                            │
                     Spark quota gone?
                            │ YES
                            ▼
              ┌────────────────────────┐
              │    SPARK-EXHAUSTED     │  ./switch-config.sh spark-exhausted
              │                        │
              │  Non-spark agents →    │
              │  gpt-5.3-codex (400k)  │
              └────────────┬───────────┘
                            │
                     OpenAI down?
                            │ YES
                            ▼
              ┌────────────────────────┐
              │      EMERGENCY         │  ./switch-config.sh emergency
              └────────────┬───────────┘
                            │
           ┌────────────────┴────────────────┐
           │                                 │
    ┌──────┴───────┐                ┌────────┴──────┐
    │  Heavy Tasks  │                │  Fast Tasks    │
    │ kimi-k2.5    │                │  glm-4.7      │
    │   -free       │                │   -free        │
    │  (256k ctx)  │                │  (128k ctx)   │
    └──────────────┘                └───────────────┘

  Recovery: ./switch-config.sh normal → back to default
```

```
  Mode              Cost     Perf     Availability
  ──────────────────────────────────────────────────
  NORMAL            $$$$    ★★★★★   Depends on OpenAI
  SPARK-EXHAUSTED   $$$     ★★★★    Depends on OpenAI
  EMERGENCY         FREE    ★★★     Independent (Kimi/GLM)
```

### When to Switch

| Symptom | Action | Command |
|---------|--------|---------|
| Spark agents failing with quota errors | Switch to spark-exhausted | `./switch-config.sh spark-exhausted` |
| All OpenAI calls returning 429/500/503 | Switch to emergency | `./switch-config.sh emergency` |
| OpenAI status page shows outage | Switch to emergency | `./switch-config.sh emergency` |
| OpenAI restored / quota reset | Switch back to normal | `./switch-config.sh normal` |

### Config Files

All fallback configs are in the `opencode-configs/` directory.

| Mode | Config File | Models |
|------|-------------|--------|
| **normal** | `oh-my-opencode.normal.json` | GPT-5.4 (complex) + GPT-5.3 Codex (coding) + Spark helpers |
| **spark-exhausted** | `oh-my-opencode.spark-exhausted.json` | GPT-5.4 (complex) + GPT-5.3 Codex (non-spark agents) |
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

# Spark quota exhausted → non-spark agents use Codex
./switch-config.sh spark-exhausted

# OpenAI down → switch to Kimi/GLM free tier
./switch-config.sh emergency

# Back to normal
./switch-config.sh normal
```

### Emergency Model Mapping

| Normal Model | Emergency Fallback | Agents |
|--------------|--------------------|--------|
| `gpt-5.4` | `kimi-k2.5-free` (256k ctx) | sisyphus, oracle, prometheus, metis, momus, atlas, plan |
| `gpt-5.3-codex` | `kimi-k2.5-free` (256k ctx) | hephaestus, multimodal-looker, frontend, writer |
| `gpt-5.3-codex-spark` | `glm-4.7-free` (128k ctx) | librarian, explore, sisyphus-junior, build, OpenCode-Builder |

## Verify

Run OpenCode doctor/check after applying. Validate that:

- provider is OpenAI
- default complex model resolves to `gpt-5.4`
- coding/script model resolves to `gpt-5.3-codex`

## Security

This repo intentionally excludes API keys and tokens.
