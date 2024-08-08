import pandas as pd

def evaluation(data: pd.DataFrame, mdbf_columns: list, pss4_columns: list) -> pd.DataFrame:
    """
    Evaluates the data for the questionnaires MDBF and PSS4.
    
    Parameters:
    - data (pd.DataFrame): The input DataFrame containing the data.
    """
    # Calculate the PSS4 score for each row; values 0-16
    data['PSS4_Score'] = (
        data['PSS4_Control'] +                  
        (4 - data['PSS4_Stress']) +         
        (4 - data['PSS4_Taks']) +                
        data['PSS4_Obstacles']                 
    )

    # Calculate the mean MDBF score for each dimension for each participant
    data['MDBF_Valence_Score'] = (data['MDBF_Satisfied'] + data['MDBF_Unwell']) / 2
    data['MDBF_Arousal_Score'] = (data['MDBF_Awake'] + data['MDBF_Energy']) / 2
    data['MDBF_Calmness_Score'] = (data['MDBF_Calm'] + data['MDBF_Relaxed']) / 2

    return data