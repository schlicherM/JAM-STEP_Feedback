import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_pie_charts(data: pd.DataFrame, topics_columns: list, output_dir: str):
    """
    Creates pie charts for each unique ID in the 'SERIAL' column, only displaying topics that were selected (value 2).
    
    Parameters:
    - data (pd.DataFrame): The input DataFrame containing the data.
    - topics_columns (list): List of column names related to topics.
    - output_dir (str): Directory where the pie charts will be saved.
    """
    
    # Unique IDs in the SERIAL column
    unique_ids = data['SERIAL'].unique()
    
    for unique_id in unique_ids:
        # Filter data for the current ID
        subset = data[data['SERIAL'] == unique_id]
        
        # Aggregate the data for topics with value 2
        topics_data = subset[topics_columns].eq(2).sum()
        
        # Only keep topics with value 2
        selected_topics = topics_data[topics_data > 0]
        
        # If no topics selected, skip
        if selected_topics.empty:
            continue
        
        # Prepare data for pie chart
        partitions = selected_topics.values
        topics = selected_topics.index
        colors_pie = plt.cm.tab20.colors  # Use a colormap for pie chart colors
        
        # Create pie chart
        fig1, ax1 = plt.subplots(figsize=(7, 6), facecolor='white')
        wedges, texts, autotexts = ax1.pie(partitions, labels=topics, autopct='%1.0f%%', startangle=140, shadow=True, colors=colors_pie)
        ax1.set_title(f'Topics Distribution for ID {unique_id}', fontsize=18, fontweight='bold')
        for text in texts:
            text.set_fontsize(18)
        for autotext in autotexts:
            autotext.set_fontsize(18)
            autotext.set_color('white')
        plt.tight_layout(pad=3.0)
        
        # Save the pie chart
        file_path = os.path.join(output_dir, f'pie_chart_{unique_id}.png')
        fig1.savefig(file_path, facecolor='white')
        plt.close(fig1)  

def plot_line_graphs(data: pd.DataFrame, mdbf_columns: list, pss4_columns: list, output_dir: str):
    """
    Creates line graphs for each unique ID in the 'SERIAL' column, showing average values for MDBF and PSS4 columns.
    
    Parameters:
    - data (pd.DataFrame): The input DataFrame containing the data.
    - mdbf_columns (list): List of column names related to MDBF.
    - pss4_columns (list): List of column names related to PSS4.
    - output_dir (str): Directory where the line graphs will be saved.
    """
    
    # Unique IDs in the SERIAL column
    unique_ids = data['SERIAL'].unique()
    
    for unique_id in unique_ids:
        # Filter data for the current ID
        subset = data[data['SERIAL'] == unique_id]
       
        # Ensure the subset has more than one row for plotting
        if subset.shape[0] <= 1:
            continue
    
        # create line graph 
        fig2, ax2 = plt.subplots(figsize=(9, 6), facecolor='white')
        ax2.plot(subset['STARTED'], subset['MDBF_Valence_Score'], marker='o', label='Gut-Schlechte\nStimmung', color='#005C6A', linewidth=2, markersize=8, alpha=0.8) # -2 to generate zero centering
        ax2.plot(subset['STARTED'], subset['MDBF_Arousal_Score'], marker='o', label='Wachheit-Müdigkeit', color='#608E63', linewidth=2, markersize=8, alpha=0.8)
        ax2.plot(subset['STARTED'], subset['MDBF_Calmness_Score'], marker='o', label='Ruhe-Unruhe', color='#3D7E6A', linewidth=2, markersize=8, alpha=0.8)
        ax2.plot(subset['STARTED'], subset['PSS4_Score'], marker='o', label='Stresslevel', color='#8A9A5B', linewidth=2, markersize=8, alpha=0.8)
        ax2.set_title(f'Befindlichkeit und Stresslevel für ID {unique_id}', fontsize=18, fontweight='bold')
        ax2.set_xlabel('Datum', fontsize=18)
        ax2.set_ylabel('Level', fontsize=18)
        ax2.tick_params(axis='x', labelsize=16)
        ax2.tick_params(axis='y', labelsize=16)
        ax2.legend(fontsize=16, loc='center left', bbox_to_anchor=(1, 0.5))
        ax2.grid(True, linestyle='--', alpha=0.6)
        #ax2.fill_between(subset['STARTED'], subset[mdbf_columns].mean(axis=1), subset[pss4_columns].mean(axis=1), color='grey', alpha=0.1)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
   

        # Customize x-axis labels to show only the day
        days_months = subset['STARTED'].dt.strftime('%d-%m')
        ax2.set_xticks(subset['STARTED'])
        ax2.set_xticklabels(days_months, rotation=45, ha='right')

        plt.tight_layout(pad=3.0)
        
        # Save the line graph
        file_path = os.path.join(output_dir, f'line_graph_{unique_id}.png')
        fig2.savefig(file_path, facecolor='white')
        plt.close(fig2) 

        break

def create_heatmap(data: pd.DataFrame, output_dir: str):
    """
    Creates and saves a heatmap for the MDBF values over time.
    
    Parameters:
    - data (pd.DataFrame): The input DataFrame containing the data.
    - output_dir (str): Directory where the heatmap will be saved.
    """

    # Unique IDs in the SERIAL column
    unique_ids = data['SERIAL'].unique()
    
    for unique_id in unique_ids:
        # Filter data for the current ID
        subset = data[data['SERIAL'] == unique_id]
       
        # Ensure the subset has more than one row for plotting
        if subset.shape[0] <= 1:
            continue
    

        # Pivot the data so that each SERIAl becomes the columns and the three MDBF values become the rows
        pivot_data = subset.pivot(index='STARTED', columns='SERIAL', values=['MDBF_Valence_Score', 'MDBF_Arousal_Score', 'MDBF_Calmness_Score'])

        # Sort by date
        pivot_data = pivot_data.sort_index()

        # Create the heatmap
        plt.figure(figsize=(12, 6))
        sns.heatmap(pivot_data.T, cmap='RdYlGn', cbar_kws={'label': 'Wert'}, annot=True, fmt=".1f")

        # Set the title and labels
        plt.title(f'Befindlichkeit für ID {unique_id}', fontsize=18)
        plt.xlabel('Datum', fontsize=14)
        plt.ylabel('Befindlichkeitswerte', fontsize=14)
        days_months = subset['STARTED'].dt.strftime('%d-%m')
        plt.xticks(ticks=range(len(days_months)), labels=days_months, rotation=45, ha='right')
        y_ticks = ['Gute-Schlechte\nStimmung', 'Wachheit-Müdigkeit', 'Ruhe-Unruhe']
        plt.yticks(ticks=range(len(y_ticks)), labels=y_ticks, rotation=0)


        plt.tight_layout()

        # Save the heatmap
        file_path = os.path.join(output_dir, f'heatmap_{unique_id}.png')
        plt.savefig(file_path)
        plt.close()

        break


def create_visualizations(data: pd.DataFrame, mdbf_columns: list, pss4_columns: list, topics_columns: list, output_dir: str):
    """
    Creates all plots for the individual participants
    - pie charts 
    - line graphs
    
    Parameters:
    - data (pd.DataFrame): The input DataFrame containing the data.
    - mdbf_columns (list): List of column names related to MDBF.
    - pss4_columns (list): List of column names related to PSS-4.
    - output_dir (str): Directory where the plots will be saved.
    """

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    #plot_pie_charts(data, topics_columns, output_dir)
    #plot_line_graphs(data, mdbf_columns, pss4_columns, output_dir)
    create_heatmap(data, output_dir)