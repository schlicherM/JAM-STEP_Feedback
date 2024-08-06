# Feedback Generation for the Projekt JAM-STEP 

## Overview

This project generates PDF files containing different visualisations from the JAM-STEP study data. It includes functionality for:
- Loading and preprocessing data.
- Creating visualizations such as pie charts and line graphs.
- Generating individual PDF reports for each participant.

## Project Structure

- `data_loader.py`: Contains functions for loading data.
- `preprocessing.py`: Handles data preprocessing tasks.
- `visualization.py`: Contains functions for creating differnt graphs.
- `pdf_generator.py`: Creates PDF reports for each participant.
- `main.py`: Main file executing all functions.
- `README.md`: This file.

## Notes
Make sure to update file paths and column names in the scripts as per your dataset.
Ensure all directories and files exist before running the scripts.

### Prerequisites

Ensure you have Python installed and the following Python packages:
- `pandas`
- `matplotlib`
- `fpdf`

You can install the necessary packages using pip:

```bash
pip install pandas matplotlib fpdf

