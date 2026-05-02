# OpenCode Portable Config

![Cover](cover.png)

Portable OpenCode / oh-my-openagent settings centered on three profiles:

- `gptglm`: `GPT-5.5 + GLM-5.1`
- `gptonly`: `GPT-5.5 only`
- `gptollama`: `GPT-5.5 + local Ollama gemma4:e4b`

This repository is a maintained snapshot of a working local setup. The old `normal / gpt-exhausted / emergency` flow is deprecated here.

## Files

- `opencode.json`
- `oh-my-openagent.json`
- `opencode-configs/opencode.json`
- `opencode-configs/oh-my-openagent.gptglm.json`
- `opencode-configs/oh-my-openagent.gptonly.json`
- `opencode-configs/oh-my-openagent.gptollama.json`
- `opencode-configs/switch-config.sh`
- `opencode-configs/oa-switch`

## Apply On a New Machine

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

## Profile Model Routing

### `gptglm`

- Heavy reasoning agents: `openai/gpt-5.5`
- Quick / research / worker lanes: `zai-coding-plan/glm-5.1`

### `gptonly`

- All agents and categories: `openai/gpt-5.5`

### `gptollama`

- Heavy reasoning agents: `openai/gpt-5.5`
- Quick / research / worker lanes: `ollama/gemma4:e4b`
- Requires local Ollama provider in `opencode.json`

## Switching

From `~/.config/opencode`:

```bash
./switch-config.sh gptglm
./switch-config.sh gptonly
./switch-config.sh gptollama
./switch-config.sh status
```

You can use either the wrapper script or a shell alias.

Wrapper install target:

```bash
oa-switch gptglm
oa-switch gptonly
oa-switch gptollama
oa-switch status
```

Or with a shell alias:

```bash
alias oa-switch="$HOME/.config/opencode/switch-config.sh"
```

Then:

```bash
oa-switch gptglm
oa-switch gptonly
oa-switch gptollama
oa-switch status
```

## What The Script Does

`switch-config.sh` swaps the active config file:

- `gptglm` copies `oh-my-openagent.gptglm.json` to `oh-my-openagent.json`
- `gptonly` copies `oh-my-openagent.gptonly.json` to `oh-my-openagent.json`
- `gptollama` copies `oh-my-openagent.gptollama.json` to `oh-my-openagent.json`
- `status` checks whether `ollama/gemma4:e4b` or `glm-5.1` appears in the active config

## Portable `opencode.json`

This repo keeps `opencode.json` portable on purpose:

- includes `oh-my-openagent@latest`
- includes `opencode-openai-codex-auth`
- includes OpenAI model definitions for `gpt-5.5`, `gpt-5.3-codex`, `gpt-5.3-codex-spark`
- includes fallback `opencode` provider entries for `kimi-k2.5-free` and `glm-4.7-free`
- includes local `ollama` provider entry for `gemma4:e4b`

Machine-specific plugins from the local workstation are intentionally excluded.

## Multimodal capability notes

The provider model declarations intentionally include non-text modalities where the served model is known to expose them through OpenCode:

| Model | Input modalities |
| --- | --- |
| `openai/gpt-5.5` | `text`, `image`, `pdf` |
| `openai/gpt-5.3-codex` | `text`, `image`, `pdf` |
| `openai/gpt-5.3-codex-spark` | `text`, `image`, `pdf` |
| `opencode/kimi-k2.5-free` | `text`, `image`, `video` |
| `ollama/gemma4:e4b` | `text`, `image` |
| `opencode/glm-4.7-free` | `text` only |

Do not collapse these entries back to `input: ["text"]` when syncing to another machine. OpenCode uses this metadata to decide whether image/PDF/video parts are sent to the model or replaced with a text-only error.

## Verify

After copying:

```bash
cd ~/.config/opencode
./switch-config.sh status
```

Check that:

- `gptglm` shows `GPTGLM mode`
- `gptonly` shows `GPTONLY mode`
- `gptollama` shows `GPTOLLAMA mode`
- `oh-my-openagent.json` changes accordingly

## Security

This repository intentionally excludes API keys, tokens, and machine-specific local plugin paths.
