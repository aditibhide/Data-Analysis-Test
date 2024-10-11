import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Load the data for a given battery and convert timestamps
def load_battery_data(file_path):
    # Read CSV file into a DataFrame
    df = pd.read_csv(file_path)
    # Convert Unix epoch time in milliseconds to datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', errors='coerce')
    # Remove rows with invalid timestamps (e.g., NaT)
    df.dropna(subset=['timestamp'], inplace=True)
    # Set timestamp as the index for easy resampling
    df.set_index('timestamp', inplace=True)
    # Pivot the data to have signal names as columns and timestamps as index
    df = df.pivot(columns='signal_name', values='signal_value')
    # Forward fill to handle missing values due to irregular sampling
    df.ffill(inplace=True)
    # Backward fill to handle initial NaNs
    df.bfill(inplace=True)
    # Drop any remaining NaNs after filling
    df.dropna(inplace=True)
    return df


# Calculate State of Energy (SOE)
def calculate_soe(df):
    # Check if the necessary columns are present to calculate SOE
    if 'PW_EnergyRemaining' in df.columns and 'PW_FullPackEnergyAvailable' in df.columns:
        # Calculate SOE as the percentage of energy remaining relative to full capacity
        df['SOE'] = (df['PW_EnergyRemaining'] / df['PW_FullPackEnergyAvailable']) * 100
        # Forward fill to handle NaN values in SOE calculation
        df['SOE'] = df['SOE'].ffill()
        # Drop rows where SOE calculation failed (resulted in NaN)
        df.dropna(subset=['SOE'], inplace=True)
    return df


# Calculate monthly average charge power availability, with an option to exclude SOE > 90%
def calculate_charge_availability(df, rated_capacity=3300, exclude_high_soe=False):
    # Check if the PW_AvailableChargePower column is present
    if 'PW_AvailableChargePower' in df.columns:
        # If excluding high SOE values, filter out rows where SOE > 90%
        if exclude_high_soe and 'SOE' in df.columns:
            df = df[df['SOE'] <= 90].copy()
        # Determine if the available charge power is greater than or equal to the rated capacity
        df['is_available'] = (df['PW_AvailableChargePower'] >= rated_capacity)
        # Forward fill availability values to handle any gaps
        df['is_available'] = df['is_available'].ffill()
        # Drop rows where availability calculation resulted in NaN
        df.dropna(subset=['is_available'], inplace=True)
        # Resample to calculate the monthly average availability in percentage
        monthly_availability = df['is_available'].resample('ME').mean() * 100
        return monthly_availability
    return None


# Visualization function using seaborn
def visualize_availability(availability, title):
    # Set the theme for the plot
    sns.set_theme(style="whitegrid")
    # Create a bar plot to visualize charge power availability
    ax = sns.barplot(x=availability.index.strftime('%Y-%m'), y=availability.values, color='skyblue', errorbar=None)
    # Set plot title and labels
    ax.set_title(title)
    ax.set_xlabel('Month')
    ax.set_ylabel('Charge Power Availability (%)')
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Combined monthly availability heatmap
def visualize_combined_heatmap(availability_dict):
    # Create a DataFrame from the availability dictionary
    combined_df = pd.DataFrame(availability_dict)
    # Format index to only show year and month
    combined_df.index = combined_df.index.strftime('%Y-%m')
    # Create a heatmap to visualize availability across all batteries
    sns.heatmap(combined_df, annot=True, cmap='coolwarm', fmt=".1f", linewidths=0.5)
    plt.title('Combined Monthly Availability Heatmap for All Batteries')
    plt.xlabel('Battery')
    plt.ylabel('Month')
    plt.tight_layout()
    plt.show()


# Line plot with Seaborn
def visualize_lineplot(availability_dict):
    # Create a DataFrame from the availability dictionary
    combined_df = pd.DataFrame(availability_dict)
    # Ensure index is in datetime format for plotting
    combined_df.index = pd.to_datetime(combined_df.index, format='%Y-%m', errors='coerce')
    # Create a line plot to visualize trends over time
    sns.lineplot(data=combined_df, markers=True, dashes=False, linewidth=2)
    plt.title('Monthly Charge Power Availability for All Batteries')
    plt.xlabel('Month')
    plt.ylabel('Charge Power Availability (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Distribution plot of SOE values
def visualize_soe_distribution(df_list):
    # Combine SOE values from all dataframes into a single series
    combined_soe = pd.concat([df['SOE'] for df in df_list if 'SOE' in df.columns])
    # Create a histogram with KDE to visualize the distribution of SOE values
    sns.histplot(combined_soe, kde=True, bins=30, color='purple')
    plt.title('Distribution of State of Energy (SOE) Values')
    plt.xlabel('State of Energy (%)')
    plt.ylabel('Frequency')
    # Add a vertical line to indicate the median SOE value
    plt.axvline(combined_soe.median(), color='red', linestyle='--', linewidth=1.5, label='Median')
    plt.legend()
    plt.tight_layout()
    plt.show()


# Individual box plots for each battery
def visualize_individual_boxplots(availability_dict):
    # Create a DataFrame from the availability dictionary
    combined_df = pd.DataFrame(availability_dict)
    # Generate individual box plots for each battery
    for column in combined_df.columns:
        plt.figure(figsize=(6, 5))
        sns.boxplot(data=combined_df, y=column, width=0.5, color='lightblue')
        plt.title(f'{column}')
        plt.ylabel('Charge Power Availability (%)')
        plt.tight_layout()
        plt.show()


# Main program
if __name__ == "__main__":
    # List of file paths for each battery's data
    battery_files = ["/001.csv","/002.csv","/003.csv","/004.csv","/005.csv"]

    # Dictionary to store availability data for each battery
    availability_dict = {}
    # List to store DataFrames for each battery
    df_list = []

    # Process each battery file
    for i, file_path in enumerate(battery_files):
        # Load the battery data from CSV file
        df = load_battery_data(file_path)
        # Calculate State of Energy (SOE) for the battery
        df = calculate_soe(df)
        df_list.append(df)

        # Question 1: Calculate monthly charge power availability
        availability = calculate_charge_availability(df)
        # Visualize monthly charge power availability for the battery
        visualize_availability(availability, f'Monthly Charge Power Availability for Battery {i + 1}')

        # Question 2: Calculate and visualize charge power availability excluding SOE > 90%
        availability_excl = calculate_charge_availability(df, exclude_high_soe=True)
        visualize_availability(availability_excl, f'Monthly Charge Power Availability for Battery {i + 1} (Excluding SOE > 90%)')

        # Store the availability data for combined analysis
        availability_dict[f'Battery {i + 1}'] = availability_excl

    # Question 3: Combined analysis for all batteries
    # Calculate the combined monthly charge power availability across all batteries
    combined_availability = pd.concat(availability_dict.values(), axis=1).mean(axis=1)
    visualize_availability(combined_availability, 'Combined Monthly Charge Power Availability for All Batteries (Excluding SOE > 90%)')

    # Additional visualizations
    visualize_combined_heatmap(availability_dict)  # Heatmap for all batteries
    visualize_lineplot(availability_dict)  # Line plot to show trends over time
    visualize_soe_distribution(df_list)  # Distribution of SOE values
    visualize_individual_boxplots(availability_dict)  # Box plots for each battery
