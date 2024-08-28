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
        'MB01_01': 'MDBF_Awake', # 1 (Sehr müde) - 7 (Sehr wach), -9 not answered
        'MB01_02': 'MDBF_Satisfied', # 1 (Sehr unzufrieden) - 7 (Sehr zufrieden), -9 not answered
        'MB01_03': 'MDBF_Calm', # 1 (Sehr unruhig) - 7 (Sehr ruhig), -9 not answered
        'MB01_04': 'MDBF_Energy', # 1 (Sehr ernergielos) - 7 (Sehr energiegeladen), -9 not answered
        'MB01_05': 'MDBF_Unwell', # 1 (Sehr unwohl) - 7 (Sehr wohl), -9 not answered
        'MB01_06': 'MDBF_Relaxed', # 1 (Sehr entspannt) - 7 (Sehr angespannt), -9 not answered
        'PS01_01': 'PSS4_Control', # 1 (Nie) - 7 (Sehr oft), -9 not answered
        'PS01_02': 'PSS4_Stress', # 1 (Nie) - 5 (Sehr oft), -9 not answered
        'PS01_03': 'PSS4_Taks', # 1 (Nie) - 5 (Sehr oft), -9 not answered
        'PS01_04': 'PSS4_Obstacles', # 1 (Nie) - 5 (Sehr oft), -9 not answered
        'SC01_01': 'SSCCS_Giveup', #  1 (Stimme überhaupt nicht zu) - 7 (Stimme völlig zu), -9 not answered
        'SC01_02': 'SSCCS_Resist',  # 1 (Stimme überhaupt nicht zu) - 7 (Stimme völlig zu), -9 not answered
        'TP01': 'Topics_None', # negative or number selected
        'TP01_01': 'Topics_Bewegung', # 1 (not selected) or 2 (selected)
        'TP01_02': 'Topics_Familie', # 1 or 2
        'TP01_03': 'Topics_Essen', # 1 or 2
        'TP01_04': 'Topics_Freunde', # 1 or 2
        'TP01_05': 'Topics_Religion/Spiritualität', # 1 or 2
        'TP01_06': 'Topics_Gesundheit', # 1 or 2
        'TP01_07': 'Topics_Liebe', # 1 or 2
        'TP01_08': 'Topics_Freizeit', # 1 or 2
        'TP01_09': 'Topics_Universität', # 1 or 2
        'TP01_10': 'Topcis_Schlaf', # 1 or 2
        'TP01_11': 'Topics_Arbeit' # 1 or 2
    }

    # Rename columns
    data = data.rename(columns=column_rename_dict)

    data['SERIAL'] = data['SERIAL'].astype(str)
    data['REF'] = data['REF'].astype(str)
    data['QUESTNNR'] = data['QUESTNNR'].astype(str)
    data['MODE'] = data['MODE'].astype(str)

    #print(data.dtypes)

    return data