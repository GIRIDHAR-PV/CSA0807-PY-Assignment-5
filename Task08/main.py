
import csv
import sqlite3
import time
import os
import pandas as pd
from datetime import date, timedelta
from collections import defaultdict

os.makedirs("Task08/input", exist_ok=True)
os.makedirs("Task08/output", exist_ok=True)

def create_dataset(stations):
    path = f"Task08/input/air_quality_{stations}_stations.csv"
    start = date(2026, 1, 1)

    with open(path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["station", "day", "pm25"])

        for s in range(1, stations + 1):
            for i in range(8760):
                day = start + timedelta(days=i // 24)
                pm25 = round(20 + s * 0.1 + (i // 24 % 30) * 0.2 + (i % 24) * 0.05, 2)
                writer.writerow([f"Station{s:03d}", day, pm25])

    return path

def python_loops(path):
    totals = defaultdict(lambda: [0, 0])
    start = time.perf_counter()

    with open(path, newline="") as file:
        for row in csv.DictReader(file):
            key = (row["station"], row["day"])
            totals[key][0] += float(row["pm25"])
            totals[key][1] += 1

    result = [
        (station, day, round(total / count, 3))
        for (station, day), (total, count) in totals.items()
    ]

    return sorted(result), time.perf_counter() - start

def pandas_groupby(path):
    start = time.perf_counter()

    df = pd.read_csv(path)
    grouped = df.groupby(["station", "day"])["pm25"].mean().reset_index()

    result = sorted([
        (row.station, row.day, round(row.pm25, 3))
        for row in grouped.itertuples()
    ])

    return result, time.perf_counter() - start

def sql_groupby(path):
    start = time.perf_counter()
    con = sqlite3.connect(":memory:")

    con.execute("""
        CREATE TABLE readings (
            station TEXT,
            day TEXT,
            pm25 REAL
        )
    """)

    with open(path, newline="") as file:
        reader = csv.DictReader(file)
        con.executemany(
            "INSERT INTO readings VALUES (?, ?, ?)",
            (
                (row["station"], row["day"], float(row["pm25"]))
                for row in reader
            )
        )

    result = con.execute("""
        SELECT station, day, ROUND(AVG(pm25), 3)
        FROM readings
        GROUP BY station, day
        ORDER BY station, day
    """).fetchall()

    con.close()
    return result, time.perf_counter() - start

timings = []

for stations in [1, 12, 120]:
    print(f"\nTesting {stations} stations...")

    path = create_dataset(stations)

    loop_result, loop_time = python_loops(path)
    pandas_result, pandas_time = pandas_groupby(path)
    sql_result, sql_time = sql_groupby(path)

    match = loop_result == pandas_result == sql_result

    print("Python loops:", round(loop_time, 3), "seconds")
    print("Pandas:", round(pandas_time, 3), "seconds")
    print("SQLite:", round(sql_time, 3), "seconds")
    print("All results match:", match)

    timings.extend([
        [stations, "Python CSV loops", round(loop_time, 4)],
        [stations, "Pandas groupby", round(pandas_time, 4)],
        [stations, "SQLite GROUP BY", round(sql_time, 4)]
    ])

    if stations == 120:
        with open("Task08/output/daily_averages.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["station", "day", "average_pm25"])
            writer.writerows(loop_result)

with open("Task08/output/timing_results.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["stations", "method", "time_seconds"])
    writer.writerows(timings)

print("\nBenchmark completed.")
print("Results saved in Task08/output/")




import matplotlib.pyplot as plt

methods = ["Python CSV loops", "Pandas groupby", "SQLite GROUP BY"]

for stations in [1, 12, 120]:
    values = [
        row[2] for row in timings if row[0] == stations
    ]

    plt.figure(figsize=(8, 5))
    plt.bar(methods, values)
    plt.xlabel("Processing Method")
    plt.ylabel("Execution Time (seconds)")
    plt.title(f"Performance Comparison - {stations} Stations")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(f"Task08/output/performance_{stations}_stations.png")
    plt.close()

print("Performance charts saved successfully.")
