# Battery Charge Power Availability Analysis

## Overview
This project provides a Python program that reads battery time series data from five CSV files and performs analysis to evaluate the charging behavior of each battery. The analysis focuses on calculating monthly average "charge power availability" for each battery, both in general and under specific conditions. The project also includes several visualizations to help understand trends and patterns in battery performance.

The key questions answered by this analysis are:
1. **Monthly average charge power availability for each battery**.
2. **Monthly charge power availability excluding data points where SOE (State of Energy) exceeds 90%**.
3. **Combined monthly charge power availability for all batteries, excluding data points where SOE > 90%**.

## Functions Overview
The following functions answer the questions in the exercise:

1. **`calculate_charge_availability(df, rated_capacity=3300)`**
   - **Question 1**: This function calculates the monthly average percentage of time for which a battery has its "PW_AvailableChargePower" greater than or equal to its rated capacity (3300 W). The result is visualized using the function `visualize_availability()`.

2. **`calculate_charge_availability(df, rated_capacity=3300, exclude_high_soe=True)`**
   - **Question 2**: This function calculates the monthly charge power availability for each battery while excluding data points where the State of Energy (SOE) is greater than 90%. The visualization of the results is done using `visualize_availability()`.

3. **`pd.concat(availability_dict.values(), axis=1).mean(axis=1)`**
   - **Question 3**: This step calculates the combined monthly charge power availability across all five batteries, excluding data points where SOE > 90%. The visualization is also handled by `visualize_availability()`.

## Data Description
The data is in CSV files, with each file containing battery measurements recorded over time. Each CSV file has the following structure:

- **`timestamp`**: Unix epoch time in milliseconds representing the time of data collection.
- **`signal_name`**: The name of the signal being recorded, such as `PW_AvailableChargePower` or `PW_EnergyRemaining`.
- **`signal_value`**: The recorded value of the signal.

## Visualizations and Insights
The project includes various visualization functions that provide valuable insights into the data, aimed at both technical and non-technical audiences:

1. **Monthly Charge Power Availability (`visualize_availability()`)**
   - This visualization displays a bar graph for each battery, showing the monthly average charge power availability. It provides a clear view of how frequently each battery was capable of charging at its rated capacity.

2. **Heatmap for Combined Availability (`visualize_combined_heatmap()`)**
   - This heatmap visualizes the charge power availability for all batteries across different months in a compact format. The diverging color palette allows for easy identification of patterns, enabling stakeholders to quickly pinpoint any inconsistencies or significant variations among the batteries.

3. **Line Plot of Availability Trends (`visualize_lineplot()`)**
   - The line plot displays the availability trends over time for all batteries combined. It is useful in identifying trends and fluctuations that could be missed with individual or bar visualizations. It is especially helpful for technical teams in understanding seasonal trends or monthly changes.

4. **Distribution Plot of SOE (`visualize_soe_distribution()`)**
   - This histogram with KDE (Kernel Density Estimate) displays the distribution of the State of Energy (SOE) across all batteries. The median line helps determine whether batteries typically operate near full or low capacity. Insights from this plot could be used to adjust charging strategies to avoid overcharging or underutilizing batteries.

5. **Individual Box Plots for Each Battery (`visualize_individual_boxplots()`)**
   - Box plots summarize the distribution of charge power availability for each battery individually. The box plots help in identifying the spread, central tendency, and outliers for each battery's availability. This visualization is particularly useful for understanding variations in battery behavior and identifying any anomalies or exceptional cases.

## Business Impact
The insights gained from this analysis have several potential business impacts:

1. **Optimized Charging Strategies**: By understanding the charge power availability and SOE distribution, stakeholders can optimize charging strategies to maximize battery life, avoid overcharging, and ensure efficient energy usage.

2. **Maintenance Planning**: Identifying trends in charge power availability and fluctuations across different batteries helps in anticipating maintenance needs. For example, batteries that consistently fail to reach their rated capacity might need servicing or replacement.

3. **Operational Efficiency**: Understanding monthly and combined availability allows for better operational planning, especially in environments where batteries are used in critical operations. Ensuring high charge power availability reduces downtime and improves overall system reliability.

4. **Data-Driven Decision Making**: The visualizations provide stakeholders (both technical and non-technical) with an easily interpretable way to make decisions based on trends and data-driven insights.

## Code Flow and Explanation
1. **Import Libraries**
   - **`pandas`** is used for loading and manipulating the data.
   - **`matplotlib.pyplot`** and **`seaborn`** are used for visualizations.

2. **Load Battery Data (`load_battery_data(file_path)`)**
   - This function is used to load the CSV data and convert timestamps to datetime.
   - The function performs a pivot operation to restructure the data, filling any missing values.
   - This results in a DataFrame with `signal_name` as columns and timestamps as the index.

3. **Calculate State of Energy (SOE) (`calculate_soe(df)`)**
   - This function computes the State of Energy (SOE) as a percentage using the columns `PW_EnergyRemaining` and `PW_FullPackEnergyAvailable`.
   - Missing SOE values are forward-filled.
   - This metric helps understand how much energy remains compared to the full available capacity.

4. **Calculate Monthly Charge Power Availability (`calculate_charge_availability(df, rated_capacity=3300, exclude_high_soe=False)`)**
   - This function calculates the monthly average percentage of time for which the battery has its `PW_AvailableChargePower` greater than or equal to its rated capacity (3300 W). This metric is called "charge power availability".
   - It also has an option to exclude rows where SOE exceeds 90%, which is useful for calculating the availability excluding times when the battery is close to full capacity.

5. **Visualization Functions**
   - **`visualize_availability()`**: Plots a bar chart showing the monthly availability for a single battery, suitable for both technical and non-technical audiences.
   - **`visualize_combined_heatmap()`**: Plots a heatmap comparing the monthly availability across all batteries.
   - **`visualize_lineplot()`**: Plots a line chart showing the monthly availability trend across all batteries.
   - **`visualize_soe_distribution()`**: Plots the distribution of SOE values using a histogram.
   - **`visualize_individual_boxplots()`**: Creates box plots showing the availability distribution for each battery individually.

6. **Main Workflow**
   - The script processes each CSV file iteratively:
     - Load the data using `load_battery_data()`, calculate SOE using `calculate_soe()`, and calculate monthly charge power availability using `calculate_charge_availability()`.
     - Visualize the monthly availability.
     - After processing all batteries, the combined monthly availability is calculated and visualized to show comparative insights across all batteries.

## Usage
### Running the Code
1. Place the battery data CSV files in the designated paths as specified in the `battery_files` list.
2. Ensure all dependencies are installed, including `pandas`, `matplotlib`, and `seaborn`.
3. Run the script to load the data, calculate metrics, and generate visualizations.

### Required Libraries
- `pandas`: For data manipulation and analysis.
- `matplotlib.pyplot`: For plotting visualizations.
- `seaborn`: For advanced visualizations with aesthetic themes.

To install these dependencies, run:
```bash
pip install pandas matplotlib seaborn
```
- If Using Google Collab- Change Line 36 of the Code to: monthly_availability = df['is_available'].resample('ME').mean() * 100
- If Using PyCharm- Change Line 36 of the Code to: monthly_availability = df['is_available'].resample('M').mean() * 100
  
## Conclusion
This analysis provides an in-depth understanding of battery charging behavior over time. The program calculates key metrics like charge power availability, evaluates how often batteries reach their rated capacity, and visualizes trends and distributions. This data can be used to optimize charging strategies, improve battery efficiency, and reduce maintenance costs. The provided visualizations make complex data easy to interpret, enabling informed, data-driven decision-making for both technical teams and business stakeholders.
