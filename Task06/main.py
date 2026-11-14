
import csv
import io

RAW = """station,date,pm25
Adyar,2026-10-01,48
Adyar,2026-10-02,NA
Adyar,2026-10-03,
Guindy,2026-10-01,95
Guindy,2026-10-02,-5
Guindy,2026-10-03,121
Adyar,2026-10-04,1500
"""

def load_clean(text):
    rows = []
    reader = csv.DictReader(io.StringIO(text))

    for row in reader:
        value = row["pm25"].strip()

        if value == "" or value.upper() == "NA":
            continue

        pm25 = float(value)

        if pm25 < 0 or pm25 > 999:
            continue

        rows.append((row["station"], row["date"], pm25))

    return rows

def min_max(values):
    minimum = min(values)
    maximum = max(values)

    if maximum == minimum:
        return [0.0 for value in values]

    return [round((value - minimum) / (maximum - minimum), 3) for value in values]

clean = load_clean(RAW)

print("Cleaned Data:")
print(clean)

print("Normalised Values:")
print(min_max([pm for _, _, pm in clean]))


import sqlite3

con = sqlite3.connect("Task06/air_quality.db")
con.execute("DROP TABLE IF EXISTS readings")

con.execute("""
CREATE TABLE readings (
    station TEXT,
    date TEXT,
    pm25 REAL
)
""")

con.executemany(
    "INSERT INTO readings VALUES (?, ?, ?)",
    clean
)

con.commit()

print("\nAll Readings:")
for row in con.execute("SELECT * FROM readings"):
    print(row)

print("\nAverage PM2.5 by Station:")
for row in con.execute(
    "SELECT station, AVG(pm25) FROM readings GROUP BY station"
):
    print(row)

print("\nHighest PM2.5 Reading:")
print(con.execute(
    "SELECT station, date, MAX(pm25) FROM readings"
).fetchone())

con.close()



import matplotlib.pyplot as plt
import os

station_data = {}

for station, date, pm25 in clean:
    station_data.setdefault(station, []).append(pm25)

stations = list(station_data.keys())
averages = [
    sum(values) / len(values)
    for values in station_data.values()
]

plt.figure(figsize=(8, 5))
plt.bar(stations, averages)
plt.xlabel("Monitoring Stations")
plt.ylabel("Average PM2.5")
plt.title("Average PM2.5 by Monitoring Station")
plt.tight_layout()

os.makedirs("Task06/output", exist_ok=True)
plt.savefig("Task06/output/station_comparison.png")

print("Chart saved successfully!")

plt.show()
