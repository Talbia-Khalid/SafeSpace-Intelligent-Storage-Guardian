import sqlite3
import os
from pathlib import Path
import matplotlib.pyplot as plt

# Find the SafeSpace project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database location
DB_PATH = BASE_DIR / "database" / "safespace.db"

# Graph save location
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

GRAPH_PATH = REPORTS_DIR / "storage_growth.png"


def generate_storage_graph():

    # Connect to the database
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Get table columns
    cursor.execute("PRAGMA table_info(storage_history)")
    columns = [row[1] for row in cursor.fetchall()]

    if not columns:
        print("Storage history table not found.")
        connection.close()
        return

    # Get saved storage records
    cursor.execute("SELECT * FROM storage_history")
    records = cursor.fetchall()

    connection.close()

    if not records:
        print("No storage history records found.")
        return

    # Convert records into dictionaries
    data = []

    for record in records:
        row = dict(zip(columns, record))
        data.append(row)

    # Identify database columns
    used_column = next(
        (c for c in columns if c.lower() in ["used", "used_storage"]),
        None
    )

    percentage_column = next(
        (c for c in columns if c.lower() in ["percentage", "usage_percentage"]),
        None
    )

    timestamp_column = next(
        (c for c in columns if c.lower() in ["timestamp", "date", "created_at"]),
        None
    )

    # Prepare graph data
    labels = []
    values = []

    for index, row in enumerate(data):

        if percentage_column:
            value = row[percentage_column]
            graph_label = "Storage Usage (%)"

        elif used_column:
            value = row[used_column] / (1024 * 1024 * 1024)
            graph_label = "Used Storage (GB)"

        else:
            print("Unable to identify storage data column.")
            return

        if timestamp_column:
            labels.append(str(row[timestamp_column]))
        else:
            labels.append(f"Snapshot {index + 1}")

        values.append(value)

    # Create graph
    plt.figure(figsize=(10, 5))

    plt.plot(labels, values, marker="o")

    plt.title("SafeSpace Storage Growth")
    plt.xlabel("Storage History")
    plt.ylabel(graph_label)

    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Save graph
    plt.savefig(GRAPH_PATH)

    plt.close()

    print("\nStorage graph generated successfully!")
    print("Saved at:", GRAPH_PATH)


if __name__ == "__main__":
    generate_storage_graph()
