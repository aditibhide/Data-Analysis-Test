# Battery Data Analysis

## Overview

This project involves the analysis and visualization of battery data collected from multiple CSV files. The data includes various battery signals such as energy remaining, charge power availability, and other metrics collected over time. The main purpose of this project is to calculate the monthly charge power availability for each battery, analyze the state of energy (SOE), and visualize the results using different plotting techniques.

The Python script processes the battery data by calculating metrics like State of Energy (SOE), filtering data based on certain conditions, and calculating charge power availability over time. Finally, the script visualizes the battery data using various plots generated with the help of `seaborn` and `matplotlib`.

## Dependencies

- `pandas`: for data manipulation and analysis
- `matplotlib`: for plotting graphs
- `seaborn`: for enhanced visualizations

Ensure all dependencies are installed before running the script. You can install them using the following command:

```sh
pip install pandas matplotlib seaborn
```

## Data Description

The data is in CSV files, with each file containing battery measurements recorded over time. Each CSV file has the following structure:
- `timestamp`: Unix epoch time in milliseconds representing the time of data collection.
- `signal_name`: The name of the signal being recorded, such as `PW_AvailableChargePower` or `PW_EnergyRemaining`.
- `signal_value`: The recorded value of the signal.

## Code Flow and Explanation

### 1. Import Libraries
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
```
- `pandas` is used for loading and manipulating the data.
- `matplotlib.pyplot` and `seaborn` are used for visualization.

### 2. Load Battery Data
**Function: `load_battery_data(file_path)`**
- This function is used to load the CSV data and convert timestamps to datetime.
- The function performs a pivot operation to restructure the data, filling any missing values.
- This results in a DataFrame with `signal_name` as columns and timestamps as the index.

### 3. Calculate State of Energy (SOE)
**Function: `calculate_soe(df)`**
- This function computes the State of Energy (SOE) as a percentage using the columns `PW_EnergyRemaining` and `PW_FullPackEnergyAvailable`.
- Missing SOE values are forward-filled.
- This metric helps understand how much energy remains compared to the full available capacity.

### 4. Calculate Monthly Charge Power Availability
**Function: `calculate_charge_availability(df, rated_capacity=3300, exclude_high_soe=False)`**
- This function calculates the **monthly average percentage of time for which Battery 001** has its `PW_AvailableChargePower` greater than or equal to its rated capacity (3300 W). This metric is called **"charge power availability"**.
- It also has an option to **exclude rows where SOE exceeds 90%**, which is useful for calculating the availability excluding times when the battery is close to full capacity.

### 5. Visualization Functions

#### 5.1. Visualize Availability for Each Battery
**Function: `visualize_availability()`**
- Plots a bar chart showing the **monthly availability for a single battery**, suitable for both technical and non-technical audiences.

#### 5.2. Combined Monthly Availability Heatmap
**Function: `visualize_combined_heatmap()`**
- Plots a heatmap comparing the **monthly availability across all batteries**.

#### 5.3. FacetGrid for Each Battery
**Function: `visualize_facetgrid()`**
- Creates individual bar plots for each battery's availability using `FacetGrid`.

#### 5.4. Line Plot with Seaborn
**Function: `visualize_lineplot()`**
- Plots a line chart showing the **monthly availability trend across all batteries**.

#### 5.5. Distribution Plot of SOE Values
**Function: `visualize_soe_distribution()`**
- Plots the distribution of **SOE values** using a histogram.

#### 5.6. Box Plot for Availability Across Batteries
**Function: `visualize_boxplot()`**
- Creates a box plot showing the **availability distribution across different batteries**.

### 6. Main Workflow
- The script processes each CSV file iteratively:
  1. Load the data using `load_battery_data()`, calculate SOE using `calculate_soe()`, and calculate monthly charge power availability using `calculate_charge_availability()`. Visualize the monthly availability.
  2. After processing all batteries, the combined monthly availability is calculated and visualized to show comparative insights across all batteries.

## How to Run the Code
1. Update the `battery_files` list in the script to point to the correct file paths for the CSV files.

```python
battery_files = [
    "C:/path/to/001.csv",
    "C:/path/to/002.csv",
    "C:/path/to/003.csv",
    "C:/path/to/004.csv",
    "C:/path/to/005.csv"
]
```

2. Run the script using Python:

```sh
python battery_analysis.py
```

## Output
- The script will generate a **monthly availability bar chart for Battery 001**, showing the percentage of time the available charge power is greater than or equal to **3300 W**.
- A revised monthly availability chart is also generated for **Battery 001**, **excluding times when SOE > 90%**.
- A combined monthly availability chart is generated for **all 5 batteries**, excluding periods where SOE > 90%.
- Additional visualizations include:
  - A heatmap comparing all batteries' monthly availability.
  - A FacetGrid view showing individual plots for each battery.
  - A line plot for trends in availability.
  - A histogram for the SOE distribution across all data.
  - A box plot to show availability distribution across batteries.

These plots help in understanding the behavior of battery charge power availability and energy usage trends over time.

## Mapping Code to Exercises

### Exercise 1
- **Calculate Monthly Charge Power Availability for Battery 001**: This is addressed by the `calculate_charge_availability(df, rated_capacity=3300)` function, which calculates the percentage time for which Battery 001's available charge power is greater than or equal to the rated capacity.
- **Visualization**: The function `visualize_availability()` is used to plot this data for a single battery.

### Exercise 2
- **Exclude SOE > 90% for Battery 001**: The `calculate_charge_availability(df, rated_capacity=3300, exclude_high_soe=True)` function is used with `exclude_high_soe=True` to calculate the availability excluding data points where SOE exceeds 90%.
- **Visualization**: The function `visualize_availability()` is used to show the new monthly availability.

### Exercise 3
- **Combined Monthly Availability for All Batteries**: The combined availability across all 5 batteries is calculated after processing each individual battery. The visualization is handled by the `visualize_combined_heatmap()`, `visualize_lineplot()`, and `visualize_facetgrid()` functions to show the comparative results across all batteries.

## Notes
- The data must be in a valid CSV format and contain appropriate signal names for successful analysis.
- Missing data is handled using forward and backward filling, but if the data has significant gaps, it might affect the accuracy of the visualizations.
