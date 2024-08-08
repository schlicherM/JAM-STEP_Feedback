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
        topics_data = data[topics_columns].eq(2).sum()

        # Only keep topics with value 2
        selected_topics = topics_data[topics_data > 0]
        
        # If no topics selected, skip
        if selected_topics.empty:
            continue
        
        # Prepare data for pie chart
        partitions = selected_topics.values 
        # use topics as labels but remove 'Topics_' from the column names
        topics = [col.split('_')[1] for col in selected_topics.index]
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

        break

def plot_line_graphs(data: pd.DataFrame, output_dir: str):
    """
    Creates line graphs for each unique ID in the 'SERIAL' column, showing average values for MDBF and PSS4 columns.
    
    Parameters:
    - data (pd.DataFrame): The input DataFrame containing the data.
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

def create_diverging_bar_chart(data: pd.DataFrame, topics_columns: list, output_dir: str):
    """
    Creates and saves a diverging bar chart of the MDBF Valence score for the four most mentioned topics.
    
    Parameters:
    - data (pd.DataFrame): The input DataFrame containing the data.
    - topics_columns (list): List of column names related to topics.
    - output_dir (str): Directory where the diverging bar chart will be saved.
    """
    # Unique IDs in the SERIAL column
    unique_ids = data['SERIAL'].unique()
    
    for unique_id in unique_ids:
        # Filter data for the current ID
        subset = data[data['SERIAL'] == unique_id]
        # Get the four most mentioned topics
        # TODO: what if several topics have same count?
        topics_data = subset[topics_columns].eq(2).sum()
        top_topics = topics_data.sort_values(ascending=False).head(4).index


        # Filter the data for the top topics
        subset = subset[['STARTED', 'MDBF_Valence_Score'] + list(top_topics)]

        color_positive = '#1f77b4'  # if topic was used
        color_negative = '#A9A9A9'  
        

        # create four subplots with barchart for every topic in top_topics, if the value is 2 plot the Valence score, else use zero
        fig, axs = plt.subplots(2, 2, figsize=(12, 8), facecolor='white')
        fig.suptitle(f'Gute-Schlechte Stimmung für die 4 häufigsten Topics für ID {unique_id}', fontsize=18, fontweight='bold')
        for i, topic in enumerate(top_topics):
            row = i // 2
            col = i % 2
            ax = axs[row, col]
            colors = [color_positive if value == 2 else color_negative for value in subset[topic]]
            ax.bar(subset['STARTED'], subset['MDBF_Valence_Score'] , color=colors, edgecolor='black')
            ax.set_xlabel('Datum', fontsize=12)
            ax.set_ylabel('Stimmung', fontsize=12)
            ax.tick_params(axis='x', labelsize=10)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(True, linestyle='--', alpha=0.6)
            days_months = subset['STARTED'].dt.strftime('%d-%m')
            ax.set_xticks(subset['STARTED'])
            ax.set_xticklabels(days_months, rotation=45, ha='right')
            ax.set_title(f'{topic.split("_")[1]}', fontsize=14, fontweight='bold')
        fig.legend(['Topic used', 'Topic not used'], fontsize=12)
        plt.tight_layout(pad=3.0)
        plt.subplots_adjust(top=0.9)

        # Save the diverging bar chart
        file_path = os.path.join(output_dir, f'diverging_bar_chart_{unique_id}.png')
        plt.savefig(file_path, facecolor='white')
        plt.close()

        break


def create_visualizations(data: pd.DataFrame, topics_columns: list, output_dir: str):
    """
    Creates all plots for the individual participants
    - pie charts 
    - line graphs
    
    Parameters:
    - data (pd.DataFrame): The input DataFrame containing the data.
    - topics_columns (list): List of column names related to topics.
    - output_dir (str): Directory where the plots will be saved.
    """

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    #plot_pie_charts(data, topics_columns, output_dir)
    #plot_line_graphs(data, output_dir)
    #create_heatmap(data, output_dir)
    create_diverging_bar_chart(data, topics_columns, output_dir)