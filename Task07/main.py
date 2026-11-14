
import sqlite3

readings = [
    ("Adyar", "2026-10-01", 48.0),
    ("Guindy", "2026-10-01", 95.0),
    ("Guindy", "2026-10-03", 121.0),
    ("Adyar", "2026-10-04", 60.0)
]

con = sqlite3.connect("Task07/adversarial.db")

con.execute("""
CREATE TABLE IF NOT EXISTS aq (
    station TEXT,
    day TEXT,
    pm25 REAL
)
""")

con.execute("DELETE FROM aq")

con.executemany(
    "INSERT INTO aq VALUES (?, ?, ?)",
    readings
)

con.commit()

def station_average(name):
    result = con.execute(
        "SELECT AVG(pm25) FROM aq WHERE station = ?",
        (name,)
    ).fetchone()

    return result[0]

print("Station Averages:")
print(station_average("Adyar"), station_average("Guindy"))

print("SQL Injection Test:")
print(station_average("Adyar' OR '1'='1"))

con.close()


import csv
import io

def inspect_csv(data, delimiter=","):
    if not data.strip():
        return "Empty file"

    reader = csv.DictReader(io.StringIO(data), delimiter=delimiter)

    if not reader.fieldnames:
        return "Missing header"

    required = {"station", "day", "pm25"}

    if not required.issubset(set(reader.fieldnames)):
        return "Missing column or incorrect delimiter"

    return "CSV structure is valid"

print("\nCSV Adversarial Tests:")
print(inspect_csv("station,day\nAdyar,2026-10-01"))
print(inspect_csv("station;day;pm25\nAdyar;2026-10-01;48"))
print(inspect_csv(""))
print(inspect_csv("station,day,pm25\nAdyar,2026-10-01,48"))

try:
    "station,day,pm25".encode("cp1252").decode("utf-8")
except UnicodeDecodeError:
    print("Encoding Test: UTF-8 decoding failed for incompatible encoding")


positive = {"good", "clean", "helpful", "improved"}
negative = {"bad", "dirty", "slow", "rude"}
negators = {"not", "never", "no"}


def sentiment(text):
    words = text.lower().replace(".", "").replace(",", "").split()
    score = 0
    negate_next = False

    for word in words:
        if word in negators:
            negate_next = True
            continue

        value = 1 if word in positive else -1 if word in negative else 0

        if negate_next and value != 0:
            value = -value
            negate_next = False

        score += value

    return score
try:
    b"\x96".decode("utf-8")
except UnicodeDecodeError:
    print("Encoding Test: UTF-8 decoding failed")