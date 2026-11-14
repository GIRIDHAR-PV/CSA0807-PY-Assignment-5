
# TASK A3 – ANALYSIS AND VISUALISATION DESIGN

## A3.1 – Choose the Charts

Different charts will be used to analyse air-quality readings and identify pollution patterns.

### 1. Trend of PM2.5 Over a Month – Line Chart

- A line chart will display daily PM2.5 readings over a month.
- The X-axis represents dates.
- The Y-axis represents average PM2.5 values.
- It helps identify increasing or decreasing pollution trends over time.

### 2. Comparison of Stations – Bar Chart

- A bar chart will compare the average PM2.5 readings of different stations.
- The X-axis represents station names.
- The Y-axis represents average PM2.5 values.
- It helps identify stations with higher pollution levels.

### 3. Relationship Between Temperature and PM2.5 – Scatter Plot

- A scatter plot will show the relationship between temperature and PM2.5.
- The X-axis represents temperature in Celsius.
- The Y-axis represents PM2.5 readings.
- It helps identify whether temperature changes are associated with changes in pollution levels.

### 4. Hours with the Worst Air Quality – Box Plot

- A box plot will compare PM2.5 readings across different hours.
- The X-axis represents hours of the day.
- The Y-axis represents PM2.5 values.
- It helps identify hours with high pollution levels, variations and extreme readings.

## A3.2 – Design the Summary Table

A daily summary table will be created for each monitoring station.

### Daily Summary Table Structure

| Column | Description |
|---|---|
| station_name | Name of the monitoring station |
| reading_date | Date of the readings |
| minimum_pm25 | Minimum PM2.5 value |
| maximum_pm25 | Maximum PM2.5 value |
| average_pm25 | Mean PM2.5 value |
| valid_readings | Number of valid readings |

### Method of Producing the Summary

1. Read the cleaned air-quality data from the SQLite database.
2. Group readings by station name and date.
3. Calculate the minimum PM2.5 value.
4. Calculate the maximum PM2.5 value.
5. Calculate the average PM2.5 value.
6. Count the valid readings.
7. Store and display the daily summary.

### SQL Query

SELECT
    station_name,
    reading_date,
    MIN(pm25) AS minimum_pm25,
    MAX(pm25) AS maximum_pm25,
    AVG(pm25) AS average_pm25,
    COUNT(pm25) AS valid_readings
FROM Readings
JOIN Stations USING (station_id)
GROUP BY station_name, reading_date;

## Alternative Concept and Complexity Analysis

If daily summaries were calculated using Python loops after reading all records instead of SQL GROUP BY, the program would process each reading and maintain summary values for each station and date.

### Python Loop Approach

1. Read all records from the database.
2. Create a dictionary for each station and date.
3. Calculate minimum, maximum, total and count.
4. Calculate the mean using total divided by count.
5. Display the daily summary.

### SQL GROUP BY Approach

SQL groups the readings by station and date and calculates the minimum, maximum, average and count directly inside the database.

### Time Complexity

- Python loops: O(n), because every reading is processed once.
- SQL GROUP BY: Approximately O(n) for processing all readings, with additional grouping or sorting costs depending on the database execution plan.

### Space Complexity

- Python loops after loading all rows: O(n) for storing the input records, with additional O(g) space for summary groups.
- SQL GROUP BY: Uses database-managed aggregation memory, generally related to the number of groups, O(g), although temporary storage may be required.

Here, n represents the total number of readings and g represents the number of station-date groups.

### Conclusion

SQL GROUP BY is preferred for daily automated summaries because it performs aggregation inside the database and avoids transferring all records into Python memory. Python loops are useful for small datasets and custom calculations.
