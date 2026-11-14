
import csv
import sqlite3
import time
import os
from collections import Counter

os.makedirs("Task09/output", exist_ok=True)

POSITIVE = {"good", "clean", "fast", "helpful", "improved"}
NEGATIVE = {"bad", "dirty", "slow", "rude", "smoke", "broken"}
NEGATORS = {"not", "never", "no"}

def score(text):
    words = text.lower().replace(".", " ").replace(",", " ").split()
    total = 0
    negate_next = False

    for word in words:
        if word in NEGATORS:
            negate_next = True
            continue

        value = 1 if word in POSITIVE else -1 if word in NEGATIVE else 0

        if negate_next and value != 0:
            value = -value
            negate_next = False

        total += value

    return total

def label(text):
    value = score(text)
    return "positive" if value > 0 else "negative" if value < 0 else "neutral"



with open("Task09/input/complaints.csv", newline="", encoding="utf-8-sig") as file:
    reader = csv.reader(file)
    rows = list(reader)

print("CSV Header:", rows[0])

complaints = []

for row in rows[1:]:
    if row:
        complaints.append(row[0].strip())

print("Total complaints:", len(complaints))



results = [(text, score(text), label(text)) for text in complaints]

with open("Task09/output/sentiment_results.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["complaint", "score", "predicted_label"])
    writer.writerows(results)

print("Total complaints:", len(complaints))
print("\nSentiment Results:")

for text, value, prediction in results:
    print(prediction, "|", text)

def summarise(texts, count=5):
    words = Counter(
        word.lower().strip(".,!?")
        for text in texts
        for word in text.split()
        if len(word) > 3
    )

    ranked = sorted(
        enumerate(texts),
        key=lambda item: sum(
            words[word.lower().strip(".,!?")]
            for word in item[1].split()
        ),
        reverse=True
    )

    selected = sorted(ranked[:count])
    return [text for _, text in selected]

summary = summarise(complaints)

with open("Task09/output/summary.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(summary))

print("\nExtractive Summary:")
for sentence in summary:
    print(sentence)

con = sqlite3.connect("Task09/output/complaints.db")

con.execute("""
CREATE TABLE IF NOT EXISTS readings (
    station TEXT,
    day TEXT,
    pm25 REAL
)
""")

con.execute("DELETE FROM readings")

sample_data = [
    (f"Station{i % 100:03d}", f"2026-10-{i % 30 + 1:02d}", float(i % 150))
    for i in range(100000)
]

con.executemany("INSERT INTO readings VALUES (?, ?, ?)", sample_data)
con.commit()

query = "SELECT AVG(pm25) FROM readings WHERE station = ? AND day = ?"
params = ("Station025", "2026-10-10")

start = time.perf_counter()
con.execute(query, params).fetchone()
before = time.perf_counter() - start

con.execute("CREATE INDEX IF NOT EXISTS idx_station_day ON readings(station, day)")
con.commit()

start = time.perf_counter()
con.execute(query, params).fetchone()
after = time.perf_counter() - start

print("\nQuery Performance:")
print("Before index:", round(before, 6), "seconds")
print("After index:", round(after, 6), "seconds")

con.close()

print("\nTask09 processing completed.")
