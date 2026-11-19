import pytest

from app.agent_loop import extract_pollutants, run_agent
from app.tools import (
    aqi_subindex_calculator,
    calculate_subindex,
    get_aqi_category,
)


def test_agent_tool_calculates_single_pollutant():
    result = aqi_subindex_calculator("PM2.5", 45)

    assert result["pollutant"] == "PM2.5"
    assert result["sub_index"] == 75
    assert result["category"] == "Satisfactory"


def test_agent_tool_calculates_multiple_pollutants():
    result = aqi_subindex_calculator(
        {
            "PM2.5": 45,
            "PM10": 80,
        }
    )

    assert result["overall_aqi"] == 80
    assert result["dominant_pollutant"] == "PM10"
    assert len(result["pollutant_results"]) == 2


def test_calculator_rejects_negative_concentration():
    with pytest.raises(ValueError):
        calculate_subindex("PM2.5", -10)


def test_calculator_rejects_unknown_pollutant():
    with pytest.raises(ValueError):
        calculate_subindex("XYZ", 50)


def test_aqi_category():
    assert get_aqi_category(40) == "Good"
    assert get_aqi_category(80) == "Satisfactory"
    assert get_aqi_category(150) == "Moderately polluted"
    assert get_aqi_category(250) == "Poor"
    assert get_aqi_category(350) == "Very Poor"
    assert get_aqi_category(450) == "Severe"


def test_extract_pollutants():
    result = extract_pollutants("Calculate AQI for PM2.5 45 and PM10 80")

    assert result == {
        "PM2.5": 45.0,
        "PM10": 80.0,
    }


def test_agent_selects_calculator_tool():
    result = run_agent("Calculate AQI for PM2.5 45 and PM10 80")

    assert result["selected_tool"] == "aqi_subindex_calculator"
    assert result["agent"] == "AQI Calculator Agent"
    assert result["result"]["overall_aqi"] == 80


def test_agent_rejects_empty_question():
    with pytest.raises(ValueError):
        run_agent("")


def test_agent_rejects_invalid_top_k():
    with pytest.raises(ValueError):
        run_agent("What is AQI?", top_k=15)
