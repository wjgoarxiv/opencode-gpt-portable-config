#!/bin/bash
# Oh-My-OpenAgent Config Switcher
# Usage: switch-config.sh [gptglm|gptonly|status]
#
# Profiles:
#   gptglm   → GPT-5.4 + GLM-5.1 combination
#   gptonly  → GPT-5.4 only
#   status   → Show current active profile

CONFIG_DIR="$HOME/.config/opencode"
TARGET="$CONFIG_DIR/oh-my-openagent.json"

case "$1" in
  gptglm)
    cp "$CONFIG_DIR/oh-my-openagent.gptglm.json" "$TARGET"
    echo "[OK] Switched to GPTGLM mode (GPT-5.4 + GLM-5.1)"
    ;;
  gptonly)
    cp "$CONFIG_DIR/oh-my-openagent.gptonly.json" "$TARGET"
    echo "[OK] Switched to GPTONLY mode (GPT-5.4 only)"
    ;;
  status)
    if grep -q "zai-coding-plan/glm-5.1" "$TARGET"; then
      echo "[STATUS] GPTGLM mode (GPT-5.4 + GLM-5.1)"
    else
      echo "[STATUS] GPTONLY mode (GPT-5.4 only)"
    fi
    ;;
  *)
    echo "Oh-My-OpenAgent Config Switcher"
    echo ""
    echo "Usage: $0 [gptglm|gptonly|status]"
    echo ""
    echo "  gptglm          GPT-5.4 + GLM-5.1 combination"
    echo "  gptonly         GPT-5.4 only"
    echo "  status          Show current config mode"
    ;;
esac
