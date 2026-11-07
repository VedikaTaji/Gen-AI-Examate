from dataclasses import dataclass

@dataclass
class Record:
    city: str
    bulletin_date: str
    aqi_value: int
    aqi_category: str
    prominent_pollutant: str
    stations_reporting: str
