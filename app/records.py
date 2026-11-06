from data.sample_records import SAMPLE_RECORDS

# Load all records
def load_records():
    return SAMPLE_RECORDS

# Search records using a keyword
def search(records, keyword):
    keyword = keyword.lower()
    results = []
    for record in records:
        searchable_text = str(record).lower()
        if keyword in searchable_text:
            results.append(record)
    return results

# Count records by category
def count_by(records, field="aqi_category"):
    counts = {}
    for record in records:
        category = record[field]
        counts[category] = counts.get(category, 0) + 1
    return counts

# Get record by ID
def get_by_id(records, record_id):
    for record in records:
        if record["id"] == record_id:
            return record
    return None
