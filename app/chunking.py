
import csv
import hashlib
import json
from pathlib import Path

from pypdf import PdfReader


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

CHUNK_SIZE = 900
CHUNK_OVERLAP = 150


def split_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split text into overlapping chunks."""
    text = " ".join(text.split())

    if not text:
        return []

    if overlap >= chunk_size:
        raise ValueError("Overlap must be smaller than chunk size.")

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        if end < len(text):
            last_space = text.rfind(" ", start, end)
            if last_space > start:
                end = last_space

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = max(end - overlap, start + 1)

    return chunks


def make_chunks(text, source, title, page):
    """Create chunk dictionaries with source metadata."""
    output = []

    for index, chunk_text in enumerate(split_text(text)):
        unique_text = f"{source}|{page}|{index}|{chunk_text}"
        chunk_id = hashlib.sha256(
            unique_text.encode("utf-8")
        ).hexdigest()

        output.append({
            "id": chunk_id,
            "text": chunk_text,
            "metadata": {
                "source": str(source),
                "title": str(title),
                "page": str(page),
                "chunk_index": index
            }
        })

    return output


def load_pdf(path):
    """Extract text page by page from a PDF."""
    output = []
    reader = PdfReader(str(path))
    title = path.stem.replace("_", " ")

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        output.extend(
            make_chunks(
                text=text,
                source=path.relative_to(BASE_DIR),
                title=title,
                page=page_number
            )
        )

    return output


def load_csv(path):
    """Convert each CSV row into searchable text."""
    output = []
    title = path.stem.replace("_", " ")

    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row_number, row in enumerate(reader, start=1):
            text = " | ".join(
                f"{key}: {value}"
                for key, value in row.items()
                if value is not None and str(value).strip()
            )

            output.extend(
                make_chunks(
                    text=text,
                    source=path.relative_to(BASE_DIR),
                    title=title,
                    page=f"row-{row_number}"
                )
            )

    return output


def load_json(path):
    """Convert JSON records into searchable text."""
    output = []
    title = path.stem.replace("_", " ")

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if isinstance(data, list):
        records = data
    else:
        records = [data]

    for record_number, record in enumerate(records, start=1):
        text = json.dumps(record, ensure_ascii=False)

        output.extend(
            make_chunks(
                text=text,
                source=path.relative_to(BASE_DIR),
                title=title,
                page=f"record-{record_number}"
            )
        )

    return output


def load_all_chunks():
    """Load and chunk supported documents from the data folder."""
    all_chunks = []

    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Data folder not found: {DATA_DIR}")

    for path in sorted(DATA_DIR.rglob("*")):
        if not path.is_file():
            continue

        suffix = path.suffix.lower()

        if suffix == ".pdf":
            print(f"Reading PDF: {path.name}")
            all_chunks.extend(load_pdf(path))

        elif suffix == ".csv":
            print(f"Reading CSV: {path.name}")
            all_chunks.extend(load_csv(path))

        elif suffix == ".json":
            print(f"Reading JSON: {path.name}")
            all_chunks.extend(load_json(path))

    return all_chunks


if __name__ == "__main__":
    chunks = load_all_chunks()

    print("\nChunking completed.")
    print("Total chunks:", len(chunks))

    for chunk in chunks[:3]:
        print("\nTitle:", chunk["metadata"]["title"])
        print("Source:", chunk["metadata"]["source"])
        print("Page/row:", chunk["metadata"]["page"])
        print("Text:", chunk["text"][:200])
