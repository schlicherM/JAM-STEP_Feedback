import pandas as pd
import os

def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses the data by renaming columns and converting data types.

    Parameters:
    - data (pd.DataFrame): The input data to preprocess.

    Returns:
    - pd.DataFrame: The preprocessed data.
    """
    column_rename_dict = {
        'C101_01': 'MDBF_Awake', # 1 (Sehr müde) - 101 (Sehr wach), -9 not answered
        'C101_02': 'MDBF_Satisfied', # 1 (Sehr unzufrieden) - 101 (Sehr zufrieden), -9 not answered
        'C101_03': 'MDBF_Calm', # 1 (Sehr unruhig) - 101 (Sehr ruhig), -9 not answered
        'C101_04': 'MDBF_Energy', # 1 (Sehr ernergielos) - 101 (Sehr energiegeladen), -9 not answered
        'C101_05': 'MDBF_Unwell', # 1 (Sehr unwohl) - 101 (Sehr wohl), -9 not answered
        'C101_06': 'MDBF_Relaxed', # 1 (Sehr entspannt) - 101 (Sehr angespannt), -9 not answered
        'C201_01': 'PSS4_Control', # 1 (Nie) - 101 (Sehr oft), -9 not answered
        'C201_02': 'PSS4_Stress', # 1 (Nie) - 101 (Sehr oft), -9 not answered
        'C201_03': 'PSS4_Taks', # 1 (Nie) - 101 (Sehr oft), -9 not answered
        'C201_04': 'PSS4_Obstacles', # 1 (Nie) - 101 (Sehr oft), -9 not answered
        'C301_01': 'SSCCS_Giveup', #  1 (Stimme überhaupt nicht zu) - 7 (Stimme völlig zu), -9 not answered
        'C301_02': 'SSCCS_Resist',  # 1 (Stimme überhaupt nicht zu) - 7 (Stimme völlig zu), -9 not answered
        'C401': 'Topics_None', # negative or number selected
        'C401_01': 'Topics_Movement', # 1 (not selected) or 2 (selected)
        'C401_02': 'Topics_Family', # 1 or 2
        'C401_03': 'Topics_Food', # 1 or 2
        'C401_04': 'Topics_Friends', # 1 or 2
        'C401_05': 'Topics_Religion', # 1 or 2
        'C401_06': 'Topics_Health', # 1 or 2
        'C401_07': 'Topics_Love', # 1 or 2
        'C401_08': 'Topics_Recreation', # 1 or 2
        'C401_09': 'Topics_School', # 1 or 2
        'C401_10': 'Topcis_Sleep', # 1 or 2
        'C401_11': 'Topics_Work' # 1 or 2
    }

    # Rename columns
    data = data.rename(columns=column_rename_dict)

    data['SERIAL'] = data['SERIAL'].astype(str)
    data['REF'] = data['REF'].astype(str)
    data['QUESTNNR'] = data['QUESTNNR'].astype(str)
    data['MODE'] = data['MODE'].astype(str)

    #print(data.dtypes)

    return data