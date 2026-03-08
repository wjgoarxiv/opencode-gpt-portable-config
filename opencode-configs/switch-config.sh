#!/bin/bash
# OpenCode Config Switcher
# Usage: switch-config.sh [normal|emergency|status]
#
# Mode priority:
#   normal    → All agents use GPT-5.4 (default)
#   emergency → OpenAI outage: Kimi K2.5 Free + GLM 4.7 Free

CONFIG_DIR="$HOME/.config/opencode"
TARGET="$CONFIG_DIR/oh-my-opencode.json"

case "$1" in
  normal|spark-exhausted)
    cp "$CONFIG_DIR/oh-my-opencode.normal.json" "$TARGET"
    echo "[OK] Switched to NORMAL mode (All agents use GPT-5.4)"
    ;;
  emergency)
    cp "$CONFIG_DIR/oh-my-opencode.fallback.json" "$TARGET"
    echo "[OK] Switched to EMERGENCY mode (Kimi K2.5 Free + GLM 4.7 Free)"
    ;;
  status)
    if grep -q "kimi-k2.5-free" "$TARGET"; then
      echo "[STATUS] EMERGENCY mode (Kimi/GLM Free)"
    else
      echo "[STATUS] NORMAL mode (All agents use GPT-5.4)"
    fi
    ;;
  *)
    echo "OpenCode Config Switcher"
    echo ""
    echo "Usage: $0 [normal|emergency|status]"
    echo ""
    echo "  normal    All agents use GPT-5.4 (default)"
    echo "  emergency Kimi K2.5 Free + GLM 4.7 Free (OpenAI down)"
    echo "  status    Show current config mode"
    ;;
esac
