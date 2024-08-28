import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import networkx as nx

def plot_pie_charts(data: pd.DataFrame, topics_columns: list, output_dir: str):
    """
    Creates pie charts for each participant, only displaying topics that were selected (value 2).
    
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
    Creates line graphs for each participant, showing average values for MDBF and PSS4 columns.
    
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
    
        # Create 2x2 subplots
        fig2, axes = plt.subplots(2, 2, figsize=(12, 10), facecolor='white')
        
        # Plot each score in a separate subplot
        axes[0, 0].plot(subset['STARTED'], subset['MDBF_Valence_Score'], marker='o', color='#005C6A', linewidth=2, markersize=8, alpha=0.8)
        axes[0, 0].axhline(4, color='black', linewidth=1)
        axes[0, 0].set_title('Gut-Schlechte Stimmung', fontsize=14)
        axes[0, 0].set_xlabel('Wochentag', fontsize=12)
        axes[0, 0].set_ylabel('Level', fontsize=12)
        axes[0, 0].set_ylim(1, 7)
        axes[0, 0].spines['bottom'].set_visible(False)
        axes[0, 0].grid(True, linestyle='--', alpha=0.6)
        
        axes[0, 1].plot(subset['STARTED'], subset['MDBF_Arousal_Score'], marker='o', color='#608E63', linewidth=2, markersize=8, alpha=0.8)
        axes[0, 1].axhline(4, color='black', linewidth=1)
        axes[0, 1].set_title('Wachheit-Müdigkeit', fontsize=14)
        axes[0, 1].set_xlabel('Wochentag', fontsize=12)
        axes[0, 1].set_ylabel('Level', fontsize=12)
        axes[0, 1].set_ylim(1, 7)
        axes[0, 1].spines['bottom'].set_visible(False)
        axes[0, 1].grid(True, linestyle='--', alpha=0.6)
        
        axes[1, 0].plot(subset['STARTED'], subset['MDBF_Calmness_Score'], marker='o', color='#3D7E6A', linewidth=2, markersize=8, alpha=0.8)
        axes[1, 0].axhline(4, color='black', linewidth=1)
        axes[1, 0].set_title('Ruhe-Unruhe', fontsize=14)
        axes[1, 0].set_xlabel('Wochentag', fontsize=12)
        axes[1, 0].set_ylabel('Level', fontsize=12)
        axes[1, 0].set_ylim(1, 7)
        axes[1, 0].spines['bottom'].set_visible(False)
        axes[1, 0].grid(True, linestyle='--', alpha=0.6)
        
        axes[1, 1].plot(subset['STARTED'], subset['PSS4_Score'], marker='o', color='#8A9A5B', linewidth=2, markersize=8, alpha=0.8)
        axes[1, 1].set_title('Stresslevel', fontsize=14)
        axes[1, 1].set_xlabel('Wochentag', fontsize=12)
        axes[1, 1].set_ylabel('Level', fontsize=12)
        axes[1, 1].set_ylim(0, 16) 
        axes[1, 1].grid(True, linestyle='--', alpha=0.6)
        
        # Customize x-axis labels to show only the day
        # Adjust for all subplots
        weekdays = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
        days = weekdays + weekdays
        
        for ax in axes.flat:
            ax.set_xticks(subset['STARTED'])
            ax.set_xticklabels(days, rotation=45, ha='right')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
        
        fig2.suptitle(f'Verlauf der Befindlichkeit und des Stresslevel', fontsize=18, fontweight='bold')
        plt.tight_layout(pad=3.0, rect=[0, 0, 1, 0.96]) 
        
        # Save the line graph
        file_path = os.path.join(output_dir, f'line_graph_{unique_id}.png')
        fig2.savefig(file_path, facecolor='white')
        plt.close(fig2) 

        break

def create_heatmap(data: pd.DataFrame, output_dir: str):
    """
    Creates and saves a heatmap for the MDBF values over time for every participant.
    
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
        plt.title(f'Ausprägung der Befindlichkeitswerte', fontsize=18)
        plt.xlabel('Wochentag', fontsize=14)
        plt.ylabel('Befindlichkeitswerte', fontsize=14)
        #days_months = subset['STARTED'].dt.strftime('%d-%m')
        weekdays = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
        days = weekdays + weekdays 
        midpoints_x = [i - 0.5 for i in range(1, len(days) + 1)]
        plt.xticks(ticks=midpoints_x, labels=days, rotation=45, ha='right')
        y_ticks = ['Gute Stimmung -\nSchlechte Stimmung', 'Wachheit -\nMüdigkeit', 'Ruhe -\nUnruhe']
        
        # Calculate the midpoints of each row
        midpoints_y = [i - 0.5 for i in range(1, len(y_ticks) + 1)]
        plt.yticks(ticks= midpoints_y, labels=y_ticks, rotation=0)

        # Add text next to the color bar to explain the extremas
        cbar = plt.gcf().axes[-1]  # Get the color bar axis
        cbar.text(2.8, 0.04, 'Schlecht Stimmung\nMüdigkeit\nUnruhe', ha='left', va='center', transform=cbar.transAxes, fontsize=12)
        cbar.text(2.8, 0.96, 'Gute Stimmung\nWachheit\nUnruhe', ha='left', va='center', transform=cbar.transAxes, fontsize=12)

        plt.tight_layout()

        # Save the heatmap
        file_path = os.path.join(output_dir, f'heatmap_{unique_id}.png')
        plt.savefig(file_path)
        plt.close()

        break

def create_diverging_bar_chart(data: pd.DataFrame, topics_columns: list, output_dir: str):
    """
    Creates and saves a diverging bar chart of the MDBF Valence score for the four most mentioned topics for every participant.
    
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
        fig.suptitle(f'Gute-Schlechte Stimmung für die 4 häufigsten Topics', fontsize=18, fontweight='bold')
        for i, topic in enumerate(top_topics):
            row = i // 2
            col = i % 2
            ax = axs[row, col]
            colors = [color_positive if value == 2 else color_negative for value in subset[topic]]
            centered_values = subset['MDBF_Valence_Score'] - 4 # MDBF can range from 1 to 7, so center around 4
            ax.bar(subset['STARTED'], centered_values , color=colors, edgecolor='black')
            ax.axhline(0, color='black', linewidth=1)
            ax.set_ylim(-3, 3)
            # change y-axis values to represent original MDBF values
            ax.set_yticks([-3, -2, -1, 0, 1, 2, 3])
            ax.set_yticklabels(['1', '2', '3', '4', '5', '6', '7'])
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
        # Create custom legend handles
        legend_handles = [
            mpatches.Patch(color=color_positive, label='Erwähnt'),
            mpatches.Patch(color=color_negative, label='Nicht erwähnt')
        ]

        # Add the custom legend to the plot
        fig.legend(handles=legend_handles, fontsize=12)
        plt.tight_layout(pad=3.0)
        plt.subplots_adjust(top=0.9)

        # Save the diverging bar chart
        file_path = os.path.join(output_dir, f'diverging_barchart_{unique_id}.png')
        plt.savefig(file_path, facecolor='white')
        plt.close()

        break

def calculate_mean_mdbf_scores(data: pd.DataFrame, topics_columns: list):
    """
    Calculates the mean MDBF scores for each topic.
    
    Parameters:
    - data (pd.DataFrame): The input DataFrame containing the data from one individual participant.
    - topics_columns (list): List of column names related to topics.
    
    Returns:
    - mean_scores (dict): Dictionary with topics as keys and a tuple of mean MDBF scores as values.

    """
    # calculate the mean scores for each topic for all MDBF scores  
    mean_scores = {}

    # Iterate through each topic
    for topic in topics_columns:
        # Filter the rows where the topic are mentioned
        topic_filtered_data = data[data[topic] == 2]
        
        # Calculate the mean scores for the MDBF columns
        if not topic_filtered_data.empty:
            mean_valence = topic_filtered_data['MDBF_Valence_Score'].mean()
            mean_arousal = topic_filtered_data['MDBF_Arousal_Score'].mean()
            mean_calmness = topic_filtered_data['MDBF_Calmness_Score'].mean()
            
            # Store the results in the dictionary
            mean_scores[topic] = (mean_valence, mean_arousal, mean_calmness)
        else:
            # If topic was not mentioned, store NaN values
            mean_scores[topic] = (float('nan'), float('nan'), float('nan'))

    return mean_scores

def plot_forcegraph(data: pd.DataFrame, topics_columns: list, output_dir: str):
    """
    Creates and saves a force-directed graph showing the relationships between topics und MDBF values for every participant.
    
    Parameters:
    - data (pd.DataFrame): The input DataFrame containing the data.
    - topics_columns (list): List of column names related to topics.
    - output_dir (str): Directory where the force-directed graph will be saved.
    """
    unique_ids = data['SERIAL'].unique()
    
    for unique_id in unique_ids:
        subset = data[data['SERIAL'] == unique_id]

        mean_scores = calculate_mean_mdbf_scores(subset, topics_columns)
    
        G = nx.Graph()
        
        # Add nodes for MDBF scores
        G.add_node('Gute Stimmung', color='lightcoral', size=4000)
        G.add_node('Wachheit', color='lightgreen', size=4000)
        G.add_node('Ruhe', color='lightblue', size=4000)
        
        # Add nodes and edges for each topic
        for topic in topics_columns:
            
            # Get the mean scores for this topic
            mean_valence, mean_arousal, mean_calmness = mean_scores[topic]

            # Check if any of the scores for this topic are non-NaN
            if pd.notna(mean_valence) or pd.notna(mean_arousal) or pd.notna(mean_calmness):
                # add topic node but remove 'Topics_' from the column names
                G.add_node(topic.split('_')[1], color='lightgray', size=2000)
            
                # Add edges between the topic and the MDBF scores
                if pd.notna(mean_valence):
                    G.add_edge('Gute Stimmung', topic.split('_')[1], weight=mean_valence)
                if pd.notna(mean_arousal):
                    G.add_edge('Wachheit', topic.split('_')[1], weight=mean_arousal)
                if pd.notna(mean_calmness):
                    G.add_edge('Ruhe', topic.split('_')[1], weight=mean_calmness)

        # Draw the graph using NetworkX's spring layout (force-directed)
        pos = nx.spring_layout(G, k=0.5, iterations=50)
        
        # Draw the graph
        plt.figure(figsize=(10, 8))
        node_colors = [G.nodes[node]['color'] for node in G.nodes()]
        node_sizes = [G.nodes[node]['size'] for node in G.nodes()]
        
        # Normalize edge weights for better visualization
        edge_weights = [G[u][v]['weight'] for u, v in G.edges()]
       
        nx.draw(
            G, pos, with_labels=True, node_color=node_colors, node_size=node_sizes,
            font_size=12, width=edge_weights, edge_color='gray', edge_cmap=plt.cm.Blues
        )
        
        # Save the graph
        plt.title(f"Topic und Befindlichkeits-Graph für ID {unique_id}")
        file_path = os.path.join(output_dir, f'forcegraph_{unique_id}.png')
        plt.savefig(file_path)
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
    plot_line_graphs(data, output_dir)
    #create_heatmap(data, output_dir)
    #create_diverging_bar_chart(data, topics_columns, output_dir)
    #plot_forcegraph(data, topics_columns, output_dir)