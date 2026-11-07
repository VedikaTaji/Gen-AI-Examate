import csv
import json
from pathlib import Path
from app.models import Record

RAW_FILE = Path("data/raw/aqi_data.csv")
OUTPUT_FILE = Path("data/records.json")

def clean_records():
    records = []

    try:
        with RAW_FILE.open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            required_fields = [
                "city",
                "bulletin_date",
                "aqi_value",
                "aqi_category",
                "prominent_pollutant",
                "stations_reporting"
            ]

            if not reader.fieldnames or not all(
                field in reader.fieldnames for field in required_fields
            ):
                raise ValueError("CSV is missing required columns.")

            for row_number, row in enumerate(reader, start=2):
                try:
                    record = Record(
                        city=row["city"].strip(),
                        bulletin_date=row["bulletin_date"].strip(),
                        aqi_value=int(row["aqi_value"]),
                        aqi_category=row["aqi_category"].strip(),
                        prominent_pollutant=row["prominent_pollutant"].strip(),
                        stations_reporting=row["stations_reporting"].strip()
                    )

                    if not record.city or not 0 <= record.aqi_value <= 500:
                        raise ValueError("Invalid city or AQI value.")

                    records.append(record)

                except (ValueError, TypeError, KeyError) as error:
                    print(f"Skipping bad row {row_number}: {error}")

        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

        with OUTPUT_FILE.open("w", encoding="utf-8") as file:
            json.dump(
                [record.__dict__ for record in records],
                file,
                indent=4
            )

        print(f"\nSuccessfully saved {len(records)} records.")
        print(f"Output file: {OUTPUT_FILE}")

    except FileNotFoundError:
        print(f"CSV file not found: {RAW_FILE}")
    except (OSError, ValueError) as error:
        print(f"Could not process the CSV: {error}")

if __name__ == "__main__":
    clean_records()
