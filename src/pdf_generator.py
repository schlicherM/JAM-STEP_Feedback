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
    
    # Initialize PDF document
    pdf = FPDF()
    
    # Add a title page
    pdf.add_page()
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, "Data Visualization Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "This report contains visualizations for unique IDs.", ln=True, align='C')
    pdf.ln(10)

    # Loop through the files in the output directory
    for file in files:
        if file.endswith('.png'):
            pdf.add_page()
            pdf.set_font("Arial", style='B', size=14)
            pdf.cell(200, 10, f"Visualization for {file}", ln=True, align='C')
            pdf.ln(10)
            pdf.image(os.path.join(output_dir, file), x=10, y=30, w=180)

    # Save the PDF report
    pdf.output(os.path.join(output_dir, 'visualization_report.pdf'))
