import pandas as pd
import os
from datetime import datetime

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
        dateparser = lambda x: datetime.strptime(x, '%d.%m.%Y %H:%M')
        data = pd.read_csv(
            filepath,
            encoding='ISO-8859-1',  
            delimiter=';',          
            decimal='.',            
            quotechar='"',   
            parse_dates=['STARTED'], 
            date_parser=dateparser,      
            header=0,   # First row contains column names          
            na_values=['']
        )

        return data
    except Exception as e:
        raise Exception(f"Error loading data from {filepath}: {e}")