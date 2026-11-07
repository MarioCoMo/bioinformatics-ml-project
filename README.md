# Transcription Factors and Gene Expression

## Overview

Breast cancer (TCGA-BRCA) gene expression analysis: cancer vs. healthy samples.


## Objectives

- Explore gene expression data and identify relevant patterns.
- Investigate associations between transcription factors and gene expression.
- Develop baseline machine learning models.
- Evaluate model performance and interpret the results.

## Technologies

- Python
- pandas and NumPy
- SciPy
- Matplotlib and Seaborn
- scikit-learn
- Jupyter Notebooks
- Visual Studio Code

## Project Structure

├── data/processed/     # Generated CSV files (not tracked in git)
├── docs/               # Technical Knowledge Base
├── notebooks/          # Analysis pipeline, run in order
├── reports/            # Figures
├── src/                # Reusable functions (see src/README.md)
└── tests/              # automated tests.

## Pipeline

`01_data_processing.ipynb` | Builds raw counts and TPM matrices from the GDC TSV files, merges cancer and control samples | `src/data_process.py` |
`02_data_qc.ipynb`         | Performs quality control on the merged count matrix and metadata, filters low-expression genes, applies variance 
                            stabilizing transformation (VST), and assesses sample-level expression patterns and correlations |  `src/data_validation.py` 
                            `src/visualization.py`|



## Getting Started

1. Clone this repository.
2. Create and activate a Python virtual environment.
3. Install the dependencies from `requirements.txt`.
4. Open the notebooks in VS Code.

## Data

Raw data is downloaded from the [GDC portal](https://portal.gdc.cancer.gov/projects/TCGA-BRCA) and is not included in the repo. Expected folders: `DATOS_CANCER` and `DATOS_CONTROL`, each with its TSV files and metadata JSON.


## Methodology

The analysis will include data inspection, exploratory analysis,
preprocessing, baseline modeling, and model evaluation.
