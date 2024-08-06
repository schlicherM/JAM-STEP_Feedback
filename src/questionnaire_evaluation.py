import pandas as pd

# Function to map 100 scale to 0-4 scale
def map_to_0_4_scale(value):
    if value == -9:  # Handling 'not answered' cases
        return None
    elif value < 21:
        return 0
    elif value < 41:
        return 1
    elif value < 61:
        return 2
    elif value < 81:
        return 3
    else:
        return 4

def evaluation(data: pd.DataFrame, mdbf_columns: list, pss4_columns: list) -> pd.DataFrame:
    """
    Evaluates the data for the questionnaires MDBF and PSS4.
    
    Parameters:
    - data (pd.DataFrame): The input DataFrame containing the data.
    """
    # Map the original PSS4 values to the 0-4 scale
    data['PSS4_Control'] = data['PSS4_Control'].apply(map_to_0_4_scale)
    data['PSS4_Stress'] = data['PSS4_Stress'].apply(map_to_0_4_scale)
    data['PSS4_Taks'] = data['PSS4_Taks'].apply(map_to_0_4_scale)
    data['PSS4_Obstacles'] = data['PSS4_Obstacles'].apply(map_to_0_4_scale)

    # Calculate the PSS4 score for each row; values 0-16
    data['PSS4_Score'] = (
        data['PSS4_Control'] +                  
        (4 - data['PSS4_Stress']) +         
        (4 - data['PSS4_Taks']) +                
        data['PSS4_Obstacles']                 
    )

    # Map the original MDBF values to the 0-4 scale
    data['MDBF_Awake'] = data['MDBF_Awake'].apply(map_to_0_4_scale)
    data['MDBF_Satisfied'] = data['MDBF_Satisfied'].apply(map_to_0_4_scale)
    data['MDBF_Calm'] = data['MDBF_Calm'].apply(map_to_0_4_scale)
    data['MDBF_Energy'] = data['MDBF_Energy'].apply(map_to_0_4_scale)
    data['MDBF_Unwell'] = data['MDBF_Unwell'].apply(map_to_0_4_scale)
    data['MDBF_Relaxed'] = data['MDBF_Relaxed'].apply(map_to_0_4_scale)

    # Calculate the mean MDBF score for each row
    data['MDBF_Score'] = data[mdbf_columns].mean(axis=1)
    
    return data