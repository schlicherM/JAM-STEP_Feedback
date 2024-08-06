import os
import pandas as pd
from fpdf import FPDF
import matplotlib.pyplot as plt

def create_pdf(output_dir: str):
    """
    Creates a PDF report containing all the graphs generated for each unique ID.
    
    Parameters:
    - output_dir (str): Directory where the graphs and PDFs are saved.
    """
    
    # Get the list of files in the output directory
    files = os.listdir(output_dir)
    
     # Find all unique IDs from the filenames
    unique_ids = set()
    for file in files:
        if file.endswith('.png'):
            # Extract ID from the filename (assuming it is the part before '.png')
            parts = file.split('_')
            if len(parts) > 2:
                id_part = parts[-1].split('.')[0]
                unique_ids.add(id_part)
    
    # Create a PDF for each unique ID
    for unique_id in unique_ids:
        pdf = FPDF()
        
        # Add a title page
        pdf.add_page()
        pdf.set_font("Arial", style='B', size=16)
        pdf.cell(200, 10, f"Data Visualization Report for ID {unique_id}", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, "This report contains visualizations for this specific ID.", ln=True, align='C')
        pdf.ln(10)
        
        # Add plots for this unique ID
        pie_chart_file = os.path.join(output_dir, f'pie_chart_{unique_id}.png')
        line_graph_file = os.path.join(output_dir, f'line_graph_{unique_id}.png')
        
        if os.path.exists(pie_chart_file):
            pdf.add_page()
            pdf.set_font("Arial", style='B', size=14)
            pdf.cell(200, 10, "Pie Chart", ln=True, align='C')
            pdf.ln(10)
            pdf.image(pie_chart_file, x=10, y=30, w=180)
        
        if os.path.exists(line_graph_file):
            pdf.add_page()
            pdf.set_font("Arial", style='B', size=14)
            pdf.cell(200, 10, "Line Graph", ln=True, align='C')
            pdf.ln(10)
            pdf.image(line_graph_file, x=10, y=30, w=180)
        
        # Save the PDF report in a subdirectory
        subdirectory = 'PDFs'
        subdirectory_path = os.path.join(output_dir, subdirectory)
        os.makedirs(subdirectory_path, exist_ok=True)
        pdf_output_path = os.path.join(subdirectory_path, f'report_{unique_id}.pdf')
        pdf.output(pdf_output_path)
        print(f"PDF report for ID {unique_id} saved to: {pdf_output_path}")
