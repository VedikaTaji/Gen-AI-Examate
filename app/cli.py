from app.records import load_records, search, count_by, get_by_id

# Load records
records = load_records()

# Display all records
def show_all():
    print("\n===== ALL AQI RECORDS =====")
    for record in records:
        print(record)

# Search records
def search_records():
    keyword = input("\nEnter city/category/pollutant: ")
    results = search(records, keyword)
    
    if results:
        for record in results:
            print(record)
    else:
        print("No matching records found.")

# Count records by category
def show_count():
    counts = count_by(records)
    print("\n===== AQI CATEGORY COUNT =====")
    for category, total in counts.items():
        print(f"{category}: {total}")

# Find record by ID
def find_record():
    try:
        record_id = int(input("\nEnter record ID: "))
        result = get_by_id(records, record_id)

        if result:
            print(result)
        else:
            print("Record not found.")

    except ValueError:
        print("Please enter a valid number.")

# Main menu
while True:

    print("\n====== AQIEXPLAINER ======")
    print("1. Display all records")
    print("2. Search records")
    print("3. Count AQI categories")
    print("4. Get record by ID")
    print("0. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        show_all()
    elif choice == "2":
        search_records()
    elif choice == "3":
        show_count()
    elif choice == "4":
        find_record()
    elif choice == "0":
        print("Thank you for using AQIExplainer!")
        break
    else:
        print("Invalid choice. Try again.")
