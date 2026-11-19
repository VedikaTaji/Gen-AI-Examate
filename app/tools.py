import math

# CPCB AQI concentration breakpoints.
# Each segment: (concentration_low, concentration_high,
#                aqi_low, aqi_high)
#
# CO: mg/m3
# Other pollutants: µg/m3

CPCB_BREAKPOINTS = {
    "PM2.5": {
        "unit": "µg/m3",
        "segments": [
            (0, 30, 0, 50),
            (30, 60, 50, 100),
            (60, 90, 100, 200),
            (90, 120, 200, 300),
            (120, 250, 300, 400),
        ],
        "severe_threshold": 250,
    },
    "PM10": {
        "unit": "µg/m3",
        "segments": [
            (0, 50, 0, 50),
            (50, 100, 50, 100),
            (100, 250, 100, 200),
            (250, 350, 200, 300),
            (350, 430, 300, 400),
        ],
        "severe_threshold": 430,
    },
    "NO2": {
        "unit": "µg/m3",
        "segments": [
            (0, 40, 0, 50),
            (40, 80, 50, 100),
            (80, 180, 100, 200),
            (180, 280, 200, 300),
            (280, 400, 300, 400),
        ],
        "severe_threshold": 400,
    },
    "O3": {
        "unit": "µg/m3",
        "segments": [
            (0, 50, 0, 50),
            (50, 100, 50, 100),
            (100, 168, 100, 200),
            (168, 208, 200, 300),
            (208, 748, 300, 400),
        ],
        "severe_threshold": 748,
    },
    "CO": {
        "unit": "mg/m3",
        "segments": [
            (0, 1, 0, 50),
            (1, 2, 50, 100),
            (2, 10, 100, 200),
            (10, 17, 200, 300),
            (17, 34, 300, 400),
        ],
        "severe_threshold": 34,
    },
    "SO2": {
        "unit": "µg/m3",
        "segments": [
            (0, 40, 0, 50),
            (40, 80, 50, 100),
            (80, 380, 100, 200),
            (380, 800, 200, 300),
            (800, 1600, 300, 400),
        ],
        "severe_threshold": 1600,
    },
    "NH3": {
        "unit": "µg/m3",
        "segments": [
            (0, 200, 0, 50),
            (200, 400, 50, 100),
            (400, 800, 100, 200),
            (800, 1200, 200, 300),
            (1200, 1800, 300, 400),
        ],
        "severe_threshold": 1800,
    },
    "Pb": {
        "unit": "µg/m3",
        "segments": [
            (0, 0.5, 0, 50),
            (0.5, 1, 50, 100),
            (1, 2, 100, 200),
            (2, 3, 200, 300),
            (3, 3.5, 300, 400),
        ],
        "severe_threshold": 3.5,
    },
}


def get_aqi_category(aqi):
    """Return the CPCB category for an AQI value."""

    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Satisfactory"
    elif aqi <= 200:
        return "Moderately polluted"
    elif aqi <= 300:
        return "Poor"
    elif aqi <= 400:
        return "Very Poor"
    else:
        return "Severe"


def calculate_subindex(pollutant, concentration):
    """Calculate one pollutant's AQI sub-index."""

    pollutant = pollutant.upper().replace(" ", "")

    # Normalize common pollutant names.
    aliases = {
        "PM25": "PM2.5",
        "PM2.5": "PM2.5",
        "PM10": "PM10",
        "NO2": "NO2",
        "O3": "O3",
        "CO": "CO",
        "SO2": "SO2",
        "NH3": "NH3",
        "PB": "Pb",
    }

    if pollutant not in aliases:
        raise ValueError(f"Unsupported pollutant: {pollutant}")

    pollutant = aliases[pollutant]
    concentration = float(concentration)

    if not math.isfinite(concentration) or concentration < 0:
        raise ValueError("Concentration must be a finite, non-negative number.")

    breakpoint_data = CPCB_BREAKPOINTS[pollutant]

    # The CPCB Severe band has no upper concentration breakpoint.
    # For this implementation, cap values at the Severe threshold to 500.
    if concentration >= breakpoint_data["severe_threshold"]:
        subindex = 500
    else:
        subindex = None

        for c_low, c_high, i_low, i_high in breakpoint_data["segments"]:
            if c_low <= concentration <= c_high:
                value = ((i_high - i_low) / (c_high - c_low)) * (
                    concentration - c_low
                ) + i_low

                # CPCB example: PM2.5 concentration 31 gives sub-index 51.
                subindex = math.floor(value)
                break

        if subindex is None:
            raise ValueError("Could not map concentration to a CPCB breakpoint.")

    return {
        "pollutant": pollutant,
        "concentration": concentration,
        "unit": breakpoint_data["unit"],
        "sub_index": subindex,
        "category": get_aqi_category(subindex),
    }


def aqi_subindex_calculator(pollutant, concentration=None):
    """
    Agent tool.

    Single pollutant:
        aqi_subindex_calculator("PM2.5", 45)

    Multiple pollutants:
        aqi_subindex_calculator({
            "PM2.5": 45,
            "PM10": 80,
            "NO2": 30
        })
    """

    # Multiple pollutant input: calculate overall AQI.
    if isinstance(pollutant, dict) and concentration is None:
        if not pollutant:
            raise ValueError("Provide at least one pollutant concentration.")

        results = []

        for name, value in pollutant.items():
            results.append(calculate_subindex(name, value))

        worst = max(results, key=lambda item: item["sub_index"])

        return {
            "pollutant_results": results,
            "overall_aqi": worst["sub_index"],
            "overall_category": worst["category"],
            "dominant_pollutant": worst["pollutant"],
        }

    # Single pollutant input.
    if concentration is None:
        raise ValueError("Concentration is required for a single pollutant.")

    return calculate_subindex(pollutant, concentration)
