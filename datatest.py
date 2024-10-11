import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Load the data for a given battery and convert timestamps
def load_battery_data(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    # Convert 'timestamp' from Unix epoch to datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', errors='coerce')
    # Remove rows with invalid timestamps
    df.dropna(subset=['timestamp'], inplace=True)
    # Set 'timestamp' as the index
    df.set_index('timestamp', inplace=True)
    # Pivot the data to have 'signal_name' as columns and 'signal_value' as values
    df = df.pivot(columns='signal_name', values='signal_value')
    # Forward fill missing values to handle NaNs
    df.ffill(inplace=True)
    # Backward fill missing values to handle initial NaNs
    df.bfill(inplace=True)
    # Drop any remaining NaNs after filling
    df.dropna(inplace=True)
    # Debugging output to verify the loaded and pivoted data
    print(f"Data after loading and pivoting from {file_path}:", df.head())
    return df


# Calculate State of Energy (SOE)
def calculate_soe(df):
    # Check if required columns are available for SOE calculation
    if 'PW_EnergyRemaining' in df.columns and 'PW_FullPackEnergyAvailable' in df.columns:
        # Calculate SOE as a percentage
        df['SOE'] = (df['PW_EnergyRemaining'] / df['PW_FullPackEnergyAvailable']) * 100
        # Forward fill missing SOE values to handle NaN values
        df['SOE'] = df['SOE'].ffill()
        # Drop rows where SOE calculation failed (resulted in NaN)
        df.dropna(subset=['SOE'], inplace=True)
    # Debugging output to verify the SOE calculation
    print("Data after calculating SOE:\n", df.head())
    return df


# Calculate monthly average charge power availability, with an option to exclude SOE > 90%
def calculate_charge_availability(df, rated_capacity=3300, exclude_high_soe=False):
    # Check if 'PW_AvailableChargePower' column exists
    if 'PW_AvailableChargePower' in df.columns:
        # If exclude_high_soe is True, filter out rows with SOE > 90%
        if exclude_high_soe and 'SOE' in df.columns:
            df = df[df['SOE'] <= 90].copy()
        # Determine availability based on 'PW_AvailableChargePower'
        df['is_available'] = (df['PW_AvailableChargePower'] >= rated_capacity)
        # Forward fill availability values to handle missing values
        df['is_available'] = df['is_available'].ffill()
        # Drop rows where availability calculation resulted in NaN
        df.dropna(subset=['is_available'], inplace=True)
        # Debugging output to verify the filtered data and availability
        print("Data after filtering and calculating availability:\n", df.head())
        # Calculate monthly availability as a percentage
        monthly_availability = df['is_available'].resample('M').mean() * 100
        print("Monthly availability calculated:\n", monthly_availability)  # Debugging output
        return monthly_availability
    return None


# Visualization function using seaborn
def visualize_availability(availability, title):
    # Set the theme for seaborn plots
    sns.set_theme(style="whitegrid")
    # Create a bar plot for monthly availability
    ax = sns.barplot(x=availability.index.strftime('%Y-%m'), y=availability.values, color='skyblue', errorbar=None)
    ax.set_title(title)
    ax.set_xlabel('Month')
    ax.set_ylabel('Charge Power Availability (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Combined monthly availability heatmap
def visualize_combined_heatmap(availability_dict):
    # Create a DataFrame from the availability dictionary
    combined_df = pd.DataFrame(availability_dict)
    # Create a heatmap of the combined availability
    sns.heatmap(combined_df, annot=True, cmap='Blues', fmt=".1f")
    plt.title('Combined Monthly Availability Heatmap for All Batteries')
    plt.xlabel('Battery')
    plt.ylabel('Month')
    plt.tight_layout()
    plt.show()


# FacetGrid for each battery
def visualize_facetgrid(availability_dict):
    # Create a DataFrame from the availability dictionary
    combined_df = pd.DataFrame(availability_dict)
    # Reset index to keep it as a column named 'timestamp'
    combined_df.reset_index(drop=False, inplace=True)
    combined_df.rename(columns={'index': 'timestamp'}, inplace=True)
    # Melt the DataFrame to have a long format suitable for FacetGrid
    melted_df = combined_df.melt(id_vars='timestamp', var_name='Battery', value_name='Availability')
    # Ensure 'timestamp' is in datetime format
    melted_df['timestamp'] = pd.to_datetime(melted_df['timestamp'], format='%Y-%m', errors='coerce')
    # Create a FacetGrid for each battery
    g = sns.FacetGrid(melted_df, col='Battery', col_wrap=3, height=4, aspect=1.5)
    g.map_dataframe(sns.barplot, x='timestamp', y='Availability', color='skyblue', errorbar=None)
    g.set_titles(col_template='Battery {col_name}')
    g.set_axis_labels('Month', 'Charge Power Availability (%)')
    # Rotate x-axis labels for better readability
    for ax in g.axes.flatten():
        for label in ax.get_xticklabels():
            label.set_rotation(45)
    plt.tight_layout()
    plt.show()


# Line plot with Seaborn
def visualize_lineplot(availability_dict):
    # Create a DataFrame from the availability dictionary
    combined_df = pd.DataFrame(availability_dict)
    # Ensure index is in datetime format
    combined_df.index = pd.to_datetime(combined_df.index, format='%Y-%m', errors='coerce')
    # Create a line plot for availability over time
    sns.lineplot(data=combined_df, markers=True, dashes=False)
    plt.title('Monthly Charge Power Availability for All Batteries')
    plt.xlabel('Month')
    plt.ylabel('Charge Power Availability (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Distribution plot of SOE values
def visualize_soe_distribution(df_list):
    # Combine SOE values from all DataFrames into one series
    combined_soe = pd.concat([df['SOE'] for df in df_list if 'SOE' in df.columns])
    # Create a histogram with KDE for SOE values
    sns.histplot(combined_soe, kde=True, bins=30)
    plt.title('Distribution of State of Energy (SOE) Values')
    plt.xlabel('State of Energy (%)')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.show()


# Box plot for availability across batteries
def visualize_boxplot(availability_dict):
    # Create a DataFrame from the availability dictionary
    combined_df = pd.DataFrame(availability_dict)
    # Create a box plot to show distribution of availability across batteries
    sns.boxplot(data=combined_df)
    plt.title('Box Plot of Charge Power Availability Across Batteries')
    plt.xlabel('Battery')
    plt.ylabel('Charge Power Availability (%)')
    plt.tight_layout()
    plt.show()


# Main program
if __name__ == "__main__":
    # List of CSV files for different batteries
    battery_files = [
        "C:/Users/vishw/PycharmProjects/pythonProject/001.csv",
        "C:/Users/vishw/PycharmProjects/pythonProject/002.csv",
        "C:/Users/vishw/PycharmProjects/pythonProject/003.csv",
        "C:/Users/vishw/PycharmProjects/pythonProject/004.csv",
        "C:/Users/vishw/PycharmProjects/pythonProject/005.csv"
    ]

    availability_dict = {}
    df_list = []

    # Process and visualize each battery
    for i, file_path in enumerate(battery_files):
        # Load the battery data from CSV file
        df = load_battery_data(file_path)
        # Calculate State of Energy (SOE)
        df = calculate_soe(df)
        df_list.append(df)

        # Calculate and visualize charge power availability excluding SOE > 90%
        availability_excl = calculate_charge_availability(df, exclude_high_soe=True)

        if availability_excl is not None:
            # Store the availability data for later use
            availability_dict[f'Battery {i + 1}'] = availability_excl
            # Visualize the monthly availability for the current battery
            visualize_availability(availability_excl,
                                   f'Monthly Charge Power Availability for Battery {i + 1} (Excluding SOE > 90%)')
        else:
            print(f"No data available for charge power availability calculation for Battery {i + 1}.")

    # Combined analysis and visualizations
    # Calculate combined availability by averaging across all batteries
    combined_availability = pd.concat(availability_dict.values(), axis=1).mean(axis=1)
    visualize_availability(combined_availability,
                           'Combined Monthly Charge Power Availability for All Batteries (Excluding SOE > 90%)')

    # Additional visualizations
    # Heatmap showing the availability of all batteries
    visualize_combined_heatmap(availability_dict)
    # FacetGrid showing availability for each battery
    visualize_facetgrid(availability_dict)
    # Line plot showing availability trends for all batteries
    visualize_lineplot(availability_dict)
    # Distribution of State of Energy (SOE) across all batteries
    visualize_soe_distribution(df_list)
    # Box plot showing availability comparison across batteries
    visualize_boxplot(availability_dict)
