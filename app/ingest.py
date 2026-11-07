
import csv
import json
from pathlib import Path
from datetime import datetime
from dataclasses import asdict

from app.models import Record

RAW_FILE = Path("data/raw/aqi_data.csv")
OUTPUT_FILE = Path("data/records.json")

REQUIRED_FIELDS = [
    "city",
    "bulletin_date",
    "aqi_value",
    "aqi_category",
    "prominent_pollutant",
    "stations_reporting"
]


def clean_records():

    records = []

    try:
        with RAW_FILE.open(
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            # Detect comma or semicolon separator
            sample = file.read(4096)
            file.seek(0)

            try:
                dialect = csv.Sniffer().sniff(
                    sample,
                    delimiters=",;\t"
                )
            except csv.Error:
                dialect = csv.excel

            reader = csv.DictReader(file, dialect=dialect)

            # Clean column headings
            if reader.fieldnames:
                reader.fieldnames = [
                    name.strip().lower().replace(" ", "_")
                    for name in reader.fieldnames
                ]

            print("Detected CSV headings:", reader.fieldnames)

            if not reader.fieldnames or not all(
                field in reader.fieldnames
                for field in REQUIRED_FIELDS
            ):
                raise ValueError(
                    "CSV headings do not match required fields."
                )

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

                    if not record.city:
                        raise ValueError("City is empty")

                    datetime.strptime(
                        record.bulletin_date,
                        "%Y-%m-%d"
                    )

                    if not 0 <= record.aqi_value <= 500:
                        raise ValueError("Invalid AQI value")

                    if not all([
                        record.aqi_category,
                        record.prominent_pollutant,
                        record.stations_reporting
                    ]):
                        raise ValueError("Required field is empty")

                    records.append(asdict(record))

                except (ValueError, TypeError, KeyError) as error:
                    print(f"Skipping row {row_number}: {error}")

        OUTPUT_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with OUTPUT_FILE.open("w", encoding="utf-8") as file:
            json.dump(records, file, indent=4)

        print("\nData cleaning completed!")
        print("Valid records:", len(records))
        print("Saved file:", OUTPUT_FILE)

    except FileNotFoundError:
        print("Error: aqi_data.csv was not found.")

    except (OSError, ValueError) as error:
        print("Could not process the CSV:", error)


if __name__ == "__main__":
    clean_records()
