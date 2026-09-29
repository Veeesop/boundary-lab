import runpy
import tomllib
from pathlib import Path

RELEASE_TOOLS = Path(__file__).resolve().parents[1] / "scripts" / "release_tools.py"


def test_release_wheel_gate_accepts_the_declared_engine_pin():
    gate = runpy.run_path(str(RELEASE_TOOLS))["BEAT_RELEASE_WHEEL"]
    project = tomllib.loads(RELEASE_TOOLS.parents[1].joinpath("pyproject.toml").read_text(encoding="utf-8"))["project"]
    beat_wheel = next(dependency for dependency in project["dependencies"] if dependency.startswith("beat-engine @ "))

    assert gate.fullmatch(beat_wheel)


def test_release_wheel_gate_rejects_non_wheel_assets():
    gate = runpy.run_path(str(RELEASE_TOOLS))["BEAT_RELEASE_WHEEL"]
    project = tomllib.loads(RELEASE_TOOLS.parents[1].joinpath("pyproject.toml").read_text(encoding="utf-8"))["project"]
    beat_wheel = next(dependency for dependency in project["dependencies"] if dependency.startswith("beat-engine @ "))

    assert not gate.fullmatch(beat_wheel.replace("beat_engine-", "engine-"))
