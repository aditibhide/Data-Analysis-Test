# Data-Analysis-Test
Battery Data Analysis

Overview

This project involves the analysis and visualization of battery data collected from multiple CSV files. The data includes various battery signals such as energy remaining, charge power availability, and other metrics collected over time. The main purpose of this project is to calculate the monthly charge power availability for each battery, analyze the state of energy (SOE), and visualize the results using different plotting techniques.

The Python script processes the battery data by calculating metrics like State of Energy (SOE), filtering data based on certain conditions, and calculating charge power availability over time. Finally, the script visualizes the battery data using various plots generated with the help of seaborn and matplotlib.

Dependencies

pandas: for data manipulation and analysis

matplotlib: for plotting graphs

seaborn: for enhanced visualizations

Ensure all dependencies are installed before running the script. You can install them using the following command:

pip install pandas matplotlib seaborn

Data Description

The data is in CSV files, with each file containing battery measurements recorded over time. Each CSV file has the following structure:

timestamp: Unix epoch time in milliseconds representing the time of data collection.

signal_name: The name of the signal being recorded, such as PW_AvailableChargePower or PW_EnergyRemaining.

signal_value: The recorded value of the signal.

Code Flow and Explanation

1. Import Libraries

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pandas is used for loading and manipulating the data.

matplotlib.pyplot and seaborn are used for visualization.

2. Load Battery Data

The function load_battery_data(file_path) is used to load the CSV data and convert timestamps to datetime.

The function performs a pivot operation to restructure the data, filling any missing values.

This results in a DataFrame with signal_name as columns and timestamps as the index.

3. Calculate State of Energy (SOE)

The function calculate_soe(df) computes the State of Energy (SOE) as a percentage using the columns PW_EnergyRemaining and PW_FullPackEnergyAvailable.

Missing SOE values are forward-filled.

This metric helps understand how much energy remains compared to the full available capacity.

4. Calculate Monthly Charge Power Availability

The function calculate_charge_availability(df, rated_capacity=3300, exclude_high_soe=False) calculates the monthly average charge power availability.

The availability is calculated by checking if PW_AvailableChargePower meets or exceeds a specified rated capacity (default: 3300).

There is an option to exclude rows where SOE exceeds 90%.

5. Visualization Functions

visualize_availability(): Plots a bar chart showing the monthly availability for a single battery.

visualize_combined_heatmap(): Plots a heatmap comparing all the batteries' monthly availability.

visualize_facetgrid(): Creates individual bar plots for each battery's availability using FacetGrid.

visualize_lineplot(): Plots a line chart showing the monthly availability trend across all batteries.

visualize_soe_distribution(): Plots the distribution of SOE values using a histogram.

visualize_boxplot(): Creates a box plot showing the availability distribution across different batteries.

6. Main Workflow

The script processes each CSV file iteratively:

Load the data using load_battery_data().

Calculate SOE using calculate_soe().

Calculate monthly charge power availability using calculate_charge_availability().

Visualize the monthly availability.

Finally, combined visualizations are generated to show comparative insights across all batteries.

How to Run the Code

Update the battery_files list in the script to point to the correct file paths for the CSV files.

battery_files = [
    "C:/path/to/001.csv",
    "C:/path/to/002.csv",
    "C:/path/to/003.csv",
    "C:/path/to/004.csv",
    "C:/path/to/005.csv"
]

Run the script using Python:

python battery_analysis.py

Output

The script will generate several visualizations, including:

Monthly availability bar charts for each battery.

A heatmap comparing the monthly availability across all batteries.

A FacetGrid view showing individual plots for each battery.

A line plot for trends in availability.

A histogram for the SOE distribution across all data.

A box plot to show availability distribution across batteries.

These plots help in understanding the behavior of battery charge power availability and energy usage trends over time.

Notes

The data must be in a valid CSV format and contain appropriate signal names for successful analysis.

Missing data is handled using forward and backward filling, but if the data has significant gaps, it might affect the accuracy of the visualizations.
