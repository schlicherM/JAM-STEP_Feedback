import pandas as pd
import os

def load_data(filepath: str) -> pd.DataFrame:
    """
    Loads a dataset from a specified file path.

    Parameters:
    - filepath (str): The path to the data file.

    Returns:
    - pd.DataFrame: The loaded data as a pandas DataFrame.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file at {filepath} was not found.")

    try:
        data = pd.read_csv(
            filepath,
            encoding='ISO-8859-1',  
            delimiter=',',          
            decimal='.',            
            quotechar='"',          
            header=0,               # First row contains column names
            na_values=['']          # Specify additional NA values 
        )

        # Convert the 'STARTED' column to datetime with a specified format
        data['STARTED'] = pd.to_datetime(data['STARTED'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

        return data
    except Exception as e:
        raise Exception(f"Error loading data from {filepath}: {e}")