import pytest
from edsl.scenarios.Scenario import Scenario
from edsl.scenarios.ScenarioList import ScenarioList
import tempfile
import os


def test_expand():
    s = ScenarioList([Scenario({"a": 1, "b": [1, 2]})])
    expanded = s.expand("b")
    expected = ScenarioList([Scenario({"a": 1, "b": 1}), Scenario({"a": 1, "b": 2})])
    assert expanded == expected


def test_filter():
    s = ScenarioList([Scenario({"a": 1, "b": 1}), Scenario({"a": 1, "b": 2})])
    filtered = s.filter("b == 2")
    expected = ScenarioList([Scenario({"a": 1, "b": 2})])
    assert filtered == expected


def test_from_csv():
    with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".csv") as f:
        _ = f.write("name,age,location\nAlice,30,New York\nBob,25,Los Angeles\n")
        temp_filename = f.name

    scenario_list = ScenarioList.from_csv(temp_filename)
    os.remove(temp_filename)  # Clean up the temp file

    assert len(scenario_list) == 2
    assert scenario_list[0]["name"] == "Alice"
    assert scenario_list[1]["age"] == "25"


def test_to_dict():
    s = ScenarioList(
        [Scenario({"food": "wood chips"}), Scenario({"food": "wood-fired pizza"})]
    )
    result = s.to_dict()
    assert isinstance(result, dict)
    assert "scenarios" in result
    assert len(result["scenarios"]) == 2
    assert result["scenarios"][0]["food"] == "wood chips"
    assert result["scenarios"][1]["food"] == "wood-fired pizza"


if __name__ == "__main__":
    pytest.main()
