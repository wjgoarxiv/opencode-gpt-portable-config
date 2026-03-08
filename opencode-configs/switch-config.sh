#!/bin/bash
# OpenCode Config Switcher
# Usage: switch-config.sh [normal|gpt-exhausted|emergency|status]
#
# Mode priority:
#   normal          → Multi-model: Claude Opus 4.6 (Copilot) + GPT-5.4 (OpenAI direct) + Gemini/Grok (Copilot)
#   gpt-exhausted → OpenAI direct quota spent: all agents via GitHub Copilot
#   emergency       → Both providers down: Kimi K2.5 Free + GLM 4.7 Free

CONFIG_DIR="$HOME/.config/opencode"
TARGET="$CONFIG_DIR/oh-my-opencode.json"

case "$1" in
  normal)
    cp "$CONFIG_DIR/oh-my-opencode.normal.json" "$TARGET"
    echo "[OK] Switched to NORMAL mode (Multi-model: Copilot + OpenAI direct)"
    ;;
  gpt-exhausted)
    cp "$CONFIG_DIR/oh-my-opencode.gpt-exhausted.json" "$TARGET"
    echo "[OK] Switched to GPT-EXHAUSTED mode (All agents via GitHub Copilot)"
    ;;
  emergency)
    cp "$CONFIG_DIR/oh-my-opencode.fallback.json" "$TARGET"
    echo "[OK] Switched to EMERGENCY mode (Kimi K2.5 Free + GLM 4.7 Free)"
    ;;
  status)
    if grep -q "kimi-k2.5-free" "$TARGET"; then
      echo "[STATUS] EMERGENCY mode (Kimi/GLM Free)"
    elif grep -q "GPT-EXHAUSTED" "$TARGET"; then
      echo "[STATUS] GPT-EXHAUSTED mode (All GitHub Copilot)"
    else
      echo "[STATUS] NORMAL mode (Multi-model: Copilot + OpenAI direct)"
    fi
    ;;
  *)
    echo "OpenCode Config Switcher"
    echo ""
    echo "Usage: $0 [normal|gpt-exhausted|emergency|status]"
    echo ""
    echo "  normal          Multi-model: Claude Opus 4.6 (Copilot) + GPT-5.4 (OpenAI) + Gemini/Grok (default)"
    echo "  gpt-exhausted All agents via GitHub Copilot (OpenAI direct quota exhausted)"
    echo "  emergency       Kimi K2.5 Free + GLM 4.7 Free (both providers down)"
    echo "  status          Show current config mode"
    ;;
esac
