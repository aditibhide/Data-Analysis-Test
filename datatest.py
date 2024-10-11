import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Load the data for a given battery and convert timestamps
def load_battery_data(file_path):
    df = pd.read_csv(file_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', errors='coerce')  # Convert Unix epoch to datetime
    df.dropna(subset=['timestamp'], inplace=True)  # Remove rows with invalid timestamps
    df.set_index('timestamp', inplace=True)  # Set timestamp as index
    df = df.pivot(columns='signal_name', values='signal_value')  # Pivot to reshape data
    df.ffill(inplace=True)  # Forward fill to handle missing values
    df.bfill(inplace=True)  # Backward fill to handle initial NaNs
    df.dropna(inplace=True)  # Drop any remaining NaNs after filling
    return df


# Calculate State of Energy (SOE)
def calculate_soe(df):
    if 'PW_EnergyRemaining' in df.columns and 'PW_FullPackEnergyAvailable' in df.columns:
        df['SOE'] = (df['PW_EnergyRemaining'] / df['PW_FullPackEnergyAvailable']) * 100
        df['SOE'] = df['SOE'].ffill()  # Forward fill to handle NaN values in SOE calculation
        df.dropna(subset=['SOE'], inplace=True)  # Drop rows where SOE calculation failed (resulted in NaN)
    return df


# Calculate monthly average charge power availability, with an option to exclude SOE > 90%
def calculate_charge_availability(df, rated_capacity=3300, exclude_high_soe=False):
    if 'PW_AvailableChargePower' in df.columns:
        if exclude_high_soe and 'SOE' in df.columns:
            df = df[df['SOE'] <= 90].copy()  # Exclude data points where SOE > 90%
        df['is_available'] = (df['PW_AvailableChargePower'] >= rated_capacity)
        df['is_available'] = df['is_available'].ffill()  # Forward fill availability values
        df.dropna(subset=['is_available'], inplace=True)  # Drop rows where availability calculation resulted in NaN
        monthly_availability = df['is_available'].resample('ME').mean() * 100
        return monthly_availability
    return None


# Visualization function using seaborn
def visualize_availability(availability, title):
    sns.set_theme(style="whitegrid")
    ax = sns.barplot(x=availability.index.strftime('%Y-%m'), y=availability.values, color='skyblue', errorbar=None)
    ax.set_title(title)
    ax.set_xlabel('Month')
    ax.set_ylabel('Charge Power Availability (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Combined monthly availability heatmap
def visualize_combined_heatmap(availability_dict):
    combined_df = pd.DataFrame(availability_dict)
    combined_df.index = combined_df.index.strftime('%Y-%m')  # Format index to only show year and month
    sns.heatmap(combined_df, annot=True, cmap='coolwarm', fmt=".1f", linewidths=0.5)  # Use diverging color palette for better differentiation
    plt.title('Combined Monthly Availability Heatmap for All Batteries')
    plt.xlabel('Battery')
    plt.ylabel('Month')
    plt.tight_layout()
    plt.show()


# Line plot with Seaborn
def visualize_lineplot(availability_dict):
    combined_df = pd.DataFrame(availability_dict)
    combined_df.index = pd.to_datetime(combined_df.index, format='%Y-%m', errors='coerce')  # Ensure index is in datetime format
    sns.lineplot(data=combined_df, markers=True, dashes=False, linewidth=2)
    plt.title('Monthly Charge Power Availability for All Batteries')
    plt.xlabel('Month')
    plt.ylabel('Charge Power Availability (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# Distribution plot of SOE values
def visualize_soe_distribution(df_list):
    combined_soe = pd.concat([df['SOE'] for df in df_list if 'SOE' in df.columns])
    sns.histplot(combined_soe, kde=True, bins=30, color='purple')
    plt.title('Distribution of State of Energy (SOE) Values')
    plt.xlabel('State of Energy (%)')
    plt.ylabel('Frequency')
    plt.axvline(combined_soe.median(), color='red', linestyle='--', linewidth=1.5, label='Median')  # Add median line for clarity
    plt.legend()
    plt.tight_layout()
    plt.show()


# Individual box plots for each battery
def visualize_individual_boxplots(availability_dict):
    combined_df = pd.DataFrame(availability_dict)
    for column in combined_df.columns:
        plt.figure(figsize=(6, 5))
        sns.boxplot(data=combined_df, y=column, width=0.5, color='lightblue')  # Use consistent color palette
        plt.title(f'{column}')
        plt.ylabel('Charge Power Availability (%)')
        plt.tight_layout()
        plt.show()


# Main program
if __name__ == "__main__":
    battery_files = ["/001.csv","/002.csv","/003.csv","/004.csv","/005.csv"]

    availability_dict = {}
    df_list = []

    # Process each battery
    for i, file_path in enumerate(battery_files):
        df = load_battery_data(file_path)
        df = calculate_soe(df)
        df_list.append(df)

        # Question 1: Calculate monthly charge power availability
        availability = calculate_charge_availability(df)
        visualize_availability(availability, f'Monthly Charge Power Availability for Battery {i + 1}')

        # Question 2: Calculate and visualize charge power availability excluding SOE > 90%
        availability_excl = calculate_charge_availability(df, exclude_high_soe=True)
        visualize_availability(availability_excl, f'Monthly Charge Power Availability for Battery {i + 1} (Excluding SOE > 90%)')

        availability_dict[f'Battery {i + 1}'] = availability_excl

    # Question 3: Combined analysis for all batteries
    combined_availability = pd.concat(availability_dict.values(), axis=1).mean(axis=1)
    visualize_availability(combined_availability, 'Combined Monthly Charge Power Availability for All Batteries (Excluding SOE > 90%)')

    # Additional visualizations
    visualize_combined_heatmap(availability_dict)
    visualize_lineplot(availability_dict)
    visualize_soe_distribution(df_list)
    visualize_individual_boxplots(availability_dict)
