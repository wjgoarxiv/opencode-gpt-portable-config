import filecmp
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LIVE_CONFIG_DIR = Path(os.environ.get("OPENCODE_LIVE_CONFIG_DIR", Path.home() / ".config" / "opencode"))

SYNCED_FILES = [
    "opencode.json",
    "oa-switch",
    "switch-config.sh",
    "oh-my-openagent.gptglm.json",
    "oh-my-openagent.gptonly.json",
    "oh-my-openagent.gptollama.json",
    "oh-my-opencode.fallback.json",
    "oh-my-opencode.gpt-exhausted.json",
    "oh-my-opencode.normal.json",
]


def repo_path(name: str) -> Path:
    return ROOT / "opencode-configs" / name


def live_path(name: str) -> Path:
    return LIVE_CONFIG_DIR / name


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def test_live_opencode_config_files_match_portable_templates():
    for name in SYNCED_FILES:
        assert live_path(name).exists(), f"missing live config: {name}"
        assert filecmp.cmp(repo_path(name), live_path(name), shallow=False), name


def test_live_active_gptonly_config_uses_lazycodex_routing():
    active = load_json(LIVE_CONFIG_DIR / "oh-my-openagent.json")

    assert active["agents"]["librarian"]["model"] == "openai/gpt-5.4-mini"
    assert active["agents"]["explore"]["model"] == "openai/gpt-5.4-mini"
    assert active["agents"]["sisyphus-junior"]["model"] == "openai/gpt-5.3-codex"
    assert active["agents"]["build"]["model"] == "openai/gpt-5.3-codex-spark"
    assert active["categories"]["quick"]["model"] == "openai/gpt-5.4-mini"
    assert active["categories"]["unspecified-low"]["model"] == "openai/gpt-5.3-codex"
