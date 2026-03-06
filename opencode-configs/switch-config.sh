#!/bin/bash
# OpenCode Config Switcher
# Usage: switch-config.sh [normal|spark-exhausted|emergency|status]
#
# Fallback 우선순위:
#   normal          → GPT-5.3 Codex + Spark (기본)
#   spark-exhausted → Spark 소진 시, 모든 agent를 Codex로
#   emergency       → OpenAI 장애 시, Kimi K2.5 Free + GLM 4.7 Free

CONFIG_DIR="$HOME/.config/opencode"
TARGET="$CONFIG_DIR/oh-my-opencode.json"

case "$1" in
  normal)
    cp "$CONFIG_DIR/oh-my-opencode.normal.json" "$TARGET"
    echo "[OK] Switched to NORMAL mode (GPT-5.4 complex + GPT-5.3 Codex coding + Spark helpers)"
    ;;
  spark-exhausted)
    cp "$CONFIG_DIR/oh-my-opencode.spark-exhausted.json" "$TARGET"
    echo "[OK] Switched to SPARK-EXHAUSTED mode (GPT-5.4 complex + GPT-5.3 Codex non-spark agents)"
    ;;
  emergency)
    cp "$CONFIG_DIR/oh-my-opencode.fallback.json" "$TARGET"
    echo "[OK] Switched to EMERGENCY mode (Kimi K2.5 Free + GLM 4.7 Free)"
    ;;
  status)
    if grep -q "kimi-k2.5-free" "$TARGET"; then
      echo "[STATUS] EMERGENCY mode (Kimi/GLM Free)"
    elif grep -q "gpt-5.3-codex-spark" "$TARGET"; then
      echo "[STATUS] NORMAL mode (GPT-5.4 complex + GPT-5.3 Codex coding + Spark helpers)"
    else
      echo "[STATUS] SPARK-EXHAUSTED mode (GPT-5.4 complex + GPT-5.3 Codex non-spark agents)"
    fi
    ;;
  *)
    echo "OpenCode Config Switcher"
    echo ""
    echo "Usage: $0 [normal|spark-exhausted|emergency|status]"
    echo ""
    echo "  normal          GPT-5.4 complex + GPT-5.3 Codex coding + Spark helpers (default)"
    echo "  spark-exhausted GPT-5.4 complex + GPT-5.3 Codex non-spark agents"
    echo "  emergency       Kimi K2.5 Free + GLM 4.7 Free (OpenAI down)"
    echo "  status          Show current config mode"
    ;;
esac
