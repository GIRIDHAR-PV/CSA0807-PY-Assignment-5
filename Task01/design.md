
# TASK A1 – DATA ACQUISITION DESIGN

## A1.1 – Inspect the Source

The city air-quality monitoring network receives daily CSV files from 12 monitoring stations. Each CSV file contains the date, hour, PM2.5, PM10, NO2 and temperature readings.

Expected data-quality problems:

1. Missing values – PM2.5 may contain blank values or NA.
2. Negative values – Sensor faults may produce negative pollution readings.
3. Impossible values – Some readings may be extremely high or exceed realistic limits.
4. Duplicate rows – The same station may report the same date and hour more than once.
5. Different temperature units – Two stations report temperature in Fahrenheit instead of Celsius.
6. Incorrect data types – Numeric readings may be stored as text.
7. Incorrect date formats – Dates may be stored in different formats.
8. Inconsistent station names – Station names may contain spelling differences or extra spaces.

## A1.2 – Design the Storage

SQLite will be used to store station information and air-quality readings.

### Table 1: Stations

| Column | Data Type | Constraint |
|---|---|---|
| station_id | INTEGER | Primary Key |
| station_name | TEXT | UNIQUE, NOT NULL |

### Table 2: Readings

| Column | Data Type | Constraint |
|---|---|---|
| station_id | INTEGER | Foreign Key |
| reading_date | TEXT | NOT NULL |
| reading_hour | INTEGER | NOT NULL |
| pm25 | REAL | |
| pm10 | REAL | |
| no2 | REAL | |
| temperature | REAL | |
| | | Composite Primary Key (station_id, reading_date, reading_hour) |

### CSV to SQLite Mapping

- Station name is stored in the Stations table.
- Station ID connects the two tables.
- Date and hour are stored in the Readings table.
- PM2.5, PM10, NO2 and temperature are stored as REAL values.
- Fahrenheit temperatures are converted to Celsius before storage.

### Reason for Choosing SQLite

SQLite provides structured storage, primary keys, foreign keys and SQL queries. It helps avoid duplicate records and makes searching and analysing large amounts of data easier.

## A1.3 – CSV or SQL?

Three typical questions and their solutions:

### Question 1: Find the average PM2.5 of Adyar station in October.

CSV: Read all CSV files, filter Adyar records for October and calculate the average using Python.

SQL:
SELECT AVG(pm25)
FROM Readings
JOIN Stations USING (station_id)
WHERE station_name = 'Adyar'
AND reading_date BETWEEN '2026-10-01' AND '2026-10-31';

### Question 2: Find the station with the highest PM2.5 reading.

CSV: Read all files, compare PM2.5 values and identify the highest reading.

SQL:
SELECT station_name, MAX(pm25)
FROM Readings
JOIN Stations USING (station_id)
GROUP BY station_name;

### Question 3: Find the number of valid readings for each station.

CSV: Read each file and count valid readings using Python.

SQL:
SELECT station_name, COUNT(pm25)
FROM Readings
JOIN Stations USING (station_id)
WHERE pm25 IS NOT NULL
GROUP BY station_name;

### Comparison

CSV is simple and suitable for small datasets. However, repeated file reading requires scanning the data for every question.

SQLite is more suitable for large datasets because it supports structured queries and indexes. It reduces repeated file processing and provides efficient data retrieval.

## Alternative Concept and Complexity Analysis

If the data were stored only in CSV files, Python and pandas could be used to read the files into a DataFrame for every question.

### Time Complexity

- CSV full scan: O(n) per question.
- SQLite indexed lookup: approximately O(log n) for locating matching indexed records, followed by processing the matching records.

### Space Complexity

- CSV: Data is stored on disk, reducing continuous memory usage.
- Pandas: The loaded DataFrame occupies memory proportional to O(n).
- SQLite: Data remains stored on disk, with additional memory used for query processing and indexes.

### Conclusion

SQLite is preferred for the city air-quality monitoring system because it provides reliable storage, indexing and efficient querying for repeated analysis.
