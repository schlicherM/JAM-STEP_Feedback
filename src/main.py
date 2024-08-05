import os
import pandas as pd
from data_loader import load_data

def main():
    # Set file paths
    input_data_path = 'data/data.csv'
    output_dir = 'outputs'
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load the data
    try:
        data = load_data(input_data_path)

        # Set display options to show all columns and print head
        pd.set_option('display.max_columns', None)  # Show all columns
        pd.set_option('display.max_rows', 10)       # Show only the first 10 rows
        print("First few rows of the dataset:")
        print(data.head())  # Use data.head() to get the first few rows

    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()