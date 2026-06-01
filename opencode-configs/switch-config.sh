#!/bin/bash
# Oh-My-OpenAgent Config Switcher
# Usage: switch-config.sh [gptglm|gptonly|gptollama|status]
#
# Profiles:
#   gptglm   → GPT-5.5 + GLM-5.1 combination
#   gptonly  → OpenAI GPT model routing
#   gptollama → GPT-5.5 + local Ollama Gemma 4 E4B
#   status   → Show current active profile

CONFIG_DIR="$HOME/.config/opencode"
TARGET="$CONFIG_DIR/oh-my-openagent.json"

case "$1" in
  gptglm)
    cp "$CONFIG_DIR/oh-my-openagent.gptglm.json" "$TARGET"
    echo "[OK] Switched to GPTGLM mode (GPT-5.5 + GLM-5.1)"
    ;;
  gptonly)
    cp "$CONFIG_DIR/oh-my-openagent.gptonly.json" "$TARGET"
    echo "[OK] Switched to GPTONLY mode (OpenAI GPT model routing)"
    ;;
  gptollama)
    cp "$CONFIG_DIR/oh-my-openagent.gptollama.json" "$TARGET"
    echo "[OK] Switched to GPTOLLAMA mode (GPT-5.5 + Ollama Gemma 4 E4B)"
    ;;
  status)
    if grep -q "ollama/gemma4:e4b" "$TARGET"; then
      echo "[STATUS] GPTOLLAMA mode (GPT-5.5 + Ollama Gemma 4 E4B)"
    elif grep -q "zai-coding-plan/glm-5.1" "$TARGET"; then
      echo "[STATUS] GPTGLM mode (GPT-5.5 + GLM-5.1)"
    else
      echo "[STATUS] GPTONLY mode (OpenAI GPT model routing)"
    fi
    ;;
  *)
    echo "Oh-My-OpenAgent Config Switcher"
    echo ""
    echo "Usage: $0 [gptglm|gptonly|gptollama|status]"
    echo ""
    echo "  gptglm          GPT-5.5 + GLM-5.1 combination"
    echo "  gptonly         OpenAI GPT model routing"
    echo "  gptollama       GPT-5.5 + Ollama Gemma 4 E4B"
    echo "  status          Show current config mode"
    ;;
esac
