
import json
import pandas as pd
from pathlib import Path

DATA_FILE = Path("data/records.json")


def explore_records():

    with DATA_FILE.open("r", encoding="utf-8") as file:
        records = json.load(file)

    if not records:
        print("No AQI records available.")
        return

    df = pd.DataFrame(records)

    print("\n===== AQIEXPLAINER DATA ANALYSIS =====")

    # Fact 1: Total cities
    print("\n1. Total AQI records:", len(df))

    # Fact 2: City with highest AQI
    highest = df.loc[df["aqi_value"].idxmax()]
    print(
        "\n2. Highest AQI:",
        highest["city"],
        "-",
        highest["aqi_value"]
    )

    # Fact 3: Most common AQI category
    common_category = df["aqi_category"].mode()[0]
    print(
        "\n3. Most common AQI category:",
        common_category
    )


if __name__ == "__main__":
    explore_records()
