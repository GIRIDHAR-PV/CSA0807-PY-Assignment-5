
# TASK A2 – CLEANING AND NORMALISATION DESIGN

## A2.1 – Cleaning Rules

The collected air-quality data may contain missing values, impossible values, duplicate records and different temperature units. The following rules will be applied.

### 1. Missing Values

- Missing readings will first be filled using the previous valid reading from the same station.
- If no previous reading is available, the median value of that station will be used.
- This method helps preserve the number of records and reduces the effect of missing data.

### 2. Impossible Values

- Negative pollution readings will be treated as invalid.
- PM2.5 readings above 999 will be considered sensor errors.
- Other impossible readings will be identified using valid sensor limits.
- Invalid values will be treated as missing and filled using the selected missing-value rules.

### 3. Duplicate Rows

- Duplicate readings with the same station, date and hour will be identified.
- Only one valid record will be retained.
- This prevents repeated readings from affecting the analysis.

### 4. Fahrenheit Temperature Conversion

- Temperatures reported in Fahrenheit will be converted into Celsius.
- Formula:

Celsius = (Fahrenheit - 32) × 5 / 9

- All temperature readings will be stored in Celsius for consistency.

## A2.2 – Normalisation

Normalisation is used to bring data values into a common scale for comparison and analysis.

### 1. Min-Max Normalisation

Formula:

Normalized Value = (Value - Minimum) / (Maximum - Minimum)

- It converts PM2.5 values into a range between 0 and 1.
- It is suitable when a fixed range is required for comparison and visualisation.
- It is sensitive to extreme values.

### 2. Z-Score Standardisation

Formula:

Z = (Value - Mean) / Standard Deviation

- It converts PM2.5 values based on the mean and standard deviation.
- The resulting values have a mean close to 0 and a standard deviation close to 1.
- It is useful when comparing values with different distributions.

### Comparison

Min-max normalisation produces values between 0 and 1, whereas z-score standardisation produces values based on their distance from the mean.

If the maximum and minimum values are equal, min-max normalisation will return 0 for all values to avoid division by zero. If the standard deviation is zero, z-score values will also be set to 0.

## A2.3 – Formatting

The following standard formats will be used in the cleaned dataset.

1. Dates: YYYY-MM-DD format.
2. Station names: Consistent names with leading and trailing spaces removed.
3. Numbers: Numeric values stored as integers or floating-point values.
4. Temperature: All readings converted to Celsius.
5. Missing values: Stored as NULL in SQLite.
6. PM2.5, PM10 and NO2: Stored as non-negative numeric values.

These formats improve consistency and make data analysis easier.

## Alternative Concept and Complexity Analysis

If missing readings were dropped instead of being filled using previous values or the median, the program would remove all records containing missing readings.

### Effect on Daily Averages

- Dropping missing readings reduces the number of available records.
- Daily averages may become less representative if many readings are missing.
- Forward filling preserves more records but may repeat earlier values.
- Median filling provides a typical value but may reduce natural variations.

### Time Complexity

1. Dropping missing values: O(n), because every record is checked once.
2. Forward filling: O(n), because records are processed sequentially.
3. Median filling: O(n log n), because sorting is required to calculate the median.

### Space Complexity

- Dropping values can be performed using O(1) additional space if records are processed in place.
- Forward filling requires O(1) additional space when processed sequentially.
- Median calculation may require O(n) additional space if a separate collection is created.

### Conclusion

Forward filling and median filling are preferred because they preserve more useful records for air-quality analysis. Dropping missing readings is simpler but may reduce the accuracy of daily summaries when many readings are unavailable.
