# OpenCode Portable Config (Multi-Model)

![Cover](cover.png)

Portable OpenCode/oh-my-opencode settings using a multi-model strategy: each agent routes to its optimal model via GitHub Copilot + OpenAI direct. 3-tier fallback for full resilience.

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
Please refer to [here](https://github.com/wjgoarxiv/opencode-gpt-portable-config). Clone or download this repo, then: (1) copy `opencode-configs/opencode.json` and `opencode-configs/oh-my-opencode.normal.json` into my OpenCode config path (`~/.config/opencode` on macOS/Linux, `%USERPROFILE%\.config\opencode` on Windows), renaming `oh-my-opencode.normal.json` to `oh-my-opencode.json`; (2) copy all fallback configs (`oh-my-opencode.gpt-exhausted.json`, `oh-my-opencode.fallback.json`) and `switch-config.sh` into the same directory; (3) make `switch-config.sh` executable; (4) back up any existing files first; (5) run doctor/check and confirm agents resolve correctly.
```

macOS/Linux default path:

```bash
mkdir -p ~/.config/opencode
cp opencode-configs/opencode.json ~/.config/opencode/opencode.json
cp opencode-configs/oh-my-opencode.normal.json ~/.config/opencode/oh-my-opencode.json
cp opencode-configs/oh-my-opencode.gpt-exhausted.json ~/.config/opencode/
cp opencode-configs/oh-my-opencode.fallback.json ~/.config/opencode/
cp opencode-configs/switch-config.sh ~/.config/opencode/
chmod +x ~/.config/opencode/switch-config.sh
```

Windows (PowerShell) default path:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.config\opencode" | Out-Null
Copy-Item .\opencode-configs\opencode.json "$env:USERPROFILE\.config\opencode\opencode.json" -Force
Copy-Item .\opencode-configs\oh-my-opencode.normal.json "$env:USERPROFILE\.config\opencode\oh-my-opencode.json" -Force
Copy-Item .\opencode-configs\oh-my-opencode.gpt-exhausted.json "$env:USERPROFILE\.config\opencode\" -Force
Copy-Item .\opencode-configs\oh-my-opencode.fallback.json "$env:USERPROFILE\.config\opencode\" -Force
Copy-Item .\opencode-configs\switch-config.sh "$env:USERPROFILE\.config\opencode\" -Force
```

## Model Routing

This config routes each agent to its optimal model based on the oh-my-opencode architecture docs. All post-2026.2 models via GitHub Copilot.

### Normal Mode Agent Routing

| Agent | Model | Provider | Reason |
|-------|-------|----------|--------|
| **sisyphus** | claude-opus-4-6 (max) | Copilot | Claude-optimized orchestration prompts |
| **prometheus** | claude-opus-4-6 (max) | Copilot | Claude-like strategic planning |
| **metis** | claude-opus-4-6 (max) | Copilot | Critical plan verification |
| **plan** | claude-opus-4-6 | Copilot | Detailed step-by-step planning |
| **hephaestus** | gpt-5.4 (medium) | OpenAI direct | GPT-native deep executor |
| **oracle** | gpt-5.4 (high) | Copilot | GPT strength for architecture |
| **atlas** | claude-sonnet-4-6 | Copilot | Task orchestration |
| **momus** | claude-sonnet-4-6 (medium) | Copilot | Critic |
| **document-writer** | claude-sonnet-4-6 | Copilot | Long-form writing |
| **OpenCode-Builder** | claude-sonnet-4-6 | Copilot | Scaffolding |
| **frontend-ui-ux-engineer** | gemini-3.1-pro | Copilot | Gemini excels at visual/frontend |
| **multimodal-looker** | gemini-3.1-pro | Copilot | Vision & multimodal |
| **librarian** | gemini-3-flash | Copilot | Fast doc research (0.33x cost) |
| **explore** | grok-code-fast-1 | Copilot | Optimized for code search (0.25x cost) |
| **build** | grok-code-fast-1 | Copilot | Fast build execution (0.25x cost) |
| **sisyphus-junior** | gpt-5-mini | Copilot | General worker (0x cost) |

### Normal Mode Category Routing

| Category | Model | Provider |
|----------|-------|----------|
| visual-engineering | gemini-3.1-pro (high) | Copilot |
| ultrabrain | gpt-5.4 (max) | OpenAI direct |
| deep | claude-opus-4-6 (medium) | Copilot |
| artistry | gemini-3.1-pro (high) | Copilot |
| quick | grok-code-fast-1 | Copilot |
| unspecified-low | gpt-5-mini | Copilot |
| unspecified-high | claude-opus-4-6 (max) | Copilot |
| writing | claude-sonnet-4-6 | Copilot |

## Fallback System

3-tier fallback for full resilience. OpenCode does not support runtime auto-fallback — run the switch script manually, then restart OpenCode.

```
┌─────────────────────────────────────────────────────┐
│                    NORMAL (default)                  │
│         ./switch-config.sh normal                   │
│                                                     │
│  Sisyphus/Prometheus → Claude Opus 4.6 (Copilot)   │
│  Hephaestus          → GPT-5.4 (OpenAI direct)     │
│  Oracle              → GPT-5.4 (Copilot)            │
│  Frontend/Vision     → Gemini 3.1 Pro (Copilot)    │
│  Explore/Build       → Grok Code Fast 1 (Copilot)  │
│  Quick workers       → GPT-5 Mini (Copilot, free)  │
└─────────────────────┬───────────────────────────────┘
                      │
           OpenAI direct quota exhausted?
                      │ YES
                      ▼
┌─────────────────────────────────────────────────────┐
│                 GPT-EXHAUSTED                     │
│         ./switch-config.sh gpt-exhausted          │
│                                                     │
│  All agents → GitHub Copilot only                  │
│  Hephaestus → GPT-5.4 (Copilot)                   │
│  ultrabrain → GPT-5.4 (Copilot, max)              │
└─────────────────────┬───────────────────────────────┘
                      │
        Both OpenAI AND Copilot unavailable?
                      │ YES
                      ▼
┌─────────────────────────────────────────────────────┐
│                   EMERGENCY                         │
│         ./switch-config.sh emergency                │
│                                                     │
│  Heavy tasks → kimi-k2.5-free (256k ctx)           │
│  Fast tasks  → glm-4.7-free (128k ctx)             │
└─────────────────────────────────────────────────────┘

  Recovery: ./switch-config.sh normal → back to default
```

```
  Mode             Cost       Perf      Availability
  ────────────────────────────────────────────────────
  NORMAL           $$+        ★★★★★    OpenAI + Copilot
  GPT-EXHAUSTED  $$         ★★★★½    Copilot only
  EMERGENCY        FREE       ★★★      Kimi/GLM (independent)
```

### When to Switch

| Symptom | Action | Command |
|---------|--------|---------|
| OpenAI direct 429/500/503 (Codex quota) | Switch to gpt-exhausted | `./switch-config.sh gpt-exhausted` |
| All OpenAI calls failing (full outage) | Switch to gpt-exhausted | `./switch-config.sh gpt-exhausted` |
| Both OpenAI AND Copilot unavailable | Switch to emergency | `./switch-config.sh emergency` |
| OpenAI restored / quota reset | Switch back to normal | `./switch-config.sh normal` |

### Config Files

| Mode | Config File | Models |
|------|-------------|--------|
| **normal** | `oh-my-opencode.normal.json` | Multi-model: Copilot + OpenAI direct |
| **gpt-exhausted** | `oh-my-opencode.gpt-exhausted.json` | All GitHub Copilot |
| **emergency** | `oh-my-opencode.fallback.json` | Kimi K2.5 Free + GLM 4.7 Free |

### Setup

```bash
cp opencode-configs/oh-my-opencode.gpt-exhausted.json ~/.config/opencode/
cp opencode-configs/oh-my-opencode.fallback.json ~/.config/opencode/
cp opencode-configs/switch-config.sh ~/.config/opencode/
chmod +x ~/.config/opencode/switch-config.sh
```

### Usage

```bash
cd ~/.config/opencode

# Check current mode
./switch-config.sh status

# OpenAI direct quota exhausted → switch to all-Copilot
./switch-config.sh gpt-exhausted

# Both providers down → switch to free Kimi/GLM
./switch-config.sh emergency

# Back to normal
./switch-config.sh normal
```

### Emergency Model Mapping

| Normal Model | Emergency Fallback | Agents |
|--------------|--------------------|--------|
| claude-opus-4-6, gpt-5.4 | `kimi-k2.5-free` (256k ctx) | sisyphus, oracle, prometheus, metis, momus, atlas, plan, hephaestus, multimodal-looker, frontend-ui-ux-engineer, document-writer |
| gemini-3-flash, grok-code-fast-1, gpt-5-mini | `glm-4.7-free` (128k ctx) | librarian, explore, sisyphus-junior, build, OpenCode-Builder |

## Verify

Run OpenCode doctor/check after applying. Validate that:

- `sisyphus` resolves to `github-copilot/claude-opus-4-6`
- `hephaestus` resolves to `openai/gpt-5.4`
- `explore` resolves to `github-copilot/grok-code-fast-1`
- `frontend-ui-ux-engineer` resolves to `github-copilot/gemini-3.1-pro`

## Security

This repo intentionally excludes API keys and tokens.
