import os
import pandas as pd
from data_loader import load_data
from preprocessing import preprocess_data
from visualization import create_visualizations
from pdf_generator import create_pdf

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

    except Exception as e:
        print(e)


    # Process the data using the preprocessing module
    try:
        processed_data = preprocess_data(data)
    except Exception as e:
        print(f"Error during preprocessing: {e}")
        return

    #print head of processed data
    print("Data loaded and processed successfully!")
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.max_rows', 10)       
    #print(processed_data.head())  


    # Plot graphs for each unique ID
    topics_columns = [col for col in processed_data.columns if 'Topics' in col]
    mdbf_columns = [col for col in processed_data.columns if 'MDBF' in col]
    pss4_columns = [col for col in processed_data.columns if 'PSS4' in col]
    create_visualizations(processed_data, topics_columns, mdbf_columns, pss4_columns, output_dir)

    # Generate a PDF report
    create_pdf(output_dir)

if __name__ == '__main__':
    main()