import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


OPENAI_ONLY_CONFIGS = [
    ROOT / "opencode-configs" / "oh-my-openagent.gptonly.json",
    ROOT / "opencode-configs" / "oh-my-opencode.normal.json",
]


EXPECTED_AGENT_MODELS = {
    "librarian": "openai/gpt-5.4-mini",
    "explore": "openai/gpt-5.4-mini",
    "sisyphus-junior": "openai/gpt-5.3-codex",
    "build": "openai/gpt-5.3-codex-spark",
}


EXPECTED_CATEGORY_MODELS = {
    "quick": "openai/gpt-5.4-mini",
    "unspecified-low": "openai/gpt-5.3-codex",
    "ultrabrain": "openai/gpt-5.5",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def test_openai_only_configs_use_lazycodex_gpt_model_routing():
    for path in OPENAI_ONLY_CONFIGS:
        config = load_json(path)
        agents = config["agents"]
        categories = config["categories"]

        for agent, model in EXPECTED_AGENT_MODELS.items():
            assert agents[agent]["model"] == model, f"{path}:{agent}"

        for category, model in EXPECTED_CATEGORY_MODELS.items():
            assert categories[category]["model"] == model, f"{path}:{category}"

        assert categories["ultrabrain"]["variant"] == "xhigh", f"{path}:ultrabrain"
        assert len({agent["model"] for agent in agents.values()}) >= 3, path


def test_openai_model_definitions_include_lazycodex_fast_and_codex_models():
    expected_models = {
        "gpt-5.4-mini",
        "gpt-5.3-codex",
        "gpt-5.3-codex-spark",
        "gpt-5.5",
    }

    for path in [ROOT / "opencode.json", ROOT / "opencode-configs" / "opencode.json"]:
        models = load_json(path)["provider"]["openai"]["models"]
        assert expected_models <= set(models), path


def test_user_facing_gptonly_label_describes_model_routing_not_single_model():
    switcher = (ROOT / "opencode-configs" / "switch-config.sh").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_ko = (ROOT / "README-Ko-KR.md").read_text(encoding="utf-8")

    assert "GPT-5.5 only" not in switcher
    assert "`gptonly`: `OpenAI GPT model routing`" in readme
    assert "`gptonly`: `OpenAI GPT model routing`" in readme_ko
