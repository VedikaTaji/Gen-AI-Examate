import requests
from pathlib import Path

RAW_FOLDER = Path("data/raw")
RAW_FOLDER.mkdir(parents=True, exist_ok=True)

DOCUMENTS = {
    "cpcb_aqi_portal.html": "https://airquality.cpcb.gov.in/AQI_India/",
    "About_AQI.pdf": "https://www.airquality.cpcb.gov.in/ccr_docs/About_AQI.pdf",
    "cpcb_ogd_resource.html": "https://www.data.gov.in/resource/real-time-air-quality-index-various-locations",
}

def download_documents():
    for filename, url in DOCUMENTS.items():
        file_path = RAW_FOLDER / filename

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            file_path.write_bytes(response.content)
            print(f"Downloaded: {filename}")

        except requests.exceptions.RequestException as error:
            print(f"Could not download {filename}: {error}")

if __name__ == "__main__":
    download_documents()
