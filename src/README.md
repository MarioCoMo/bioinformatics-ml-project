# src/

## data_process.py

Builds and merges gene expression matrices from TCGA/GDC data.

- `load_file_to_sample_map(metadata_file, id_length=15)`: reads the GDC metadata JSON and returns a dictionary mapping each file name to its sample ID.
- `process_expression_data(data_dir, ...)`: reads all the TSV files in `data_dir`, keeps only genes (`ENSG` IDs), sums duplicated gene symbols, and returns two DataFrames (raw counts and TPM) with rows = samples and columns = genes. The metadata file defaults to `metadata.<suffix>.json` inside `data_dir`. Optionally saves the results as CSV files.
- `merge_cancer_control(cancer_file, control_file, ...)`: merges the cancer and control raw counts matrices into one and builds a metadata table with a `Condition` column (`Healthy` / `Cancer`). Optionally saves both as CSV files (`raw_merged.csv` and `metadata_merged.csv`).

## data_validation.py

Provides validation functions to ensure the integrity and consistency of gene expression data and sample metadata.

- `validate_sample_alignment(counts_df, metadata)`: checks for duplicate sample IDs, verifies that both DataFrames contain exactly the same samples, and aligns metadata rows with the count matrix sample order.
- `validate_count_matrix(counts_df)`: checks that the count matrix contains no missing values, negative values, or non-integer counts.
- `validate_metadata(metadata, required_columns=None)`: checks that the metadata contains all specified required columns.

## visualization.py

Provides utilities for saving analysis figures in a centralized project directory.

- `save_figure(name, dpi=300)`: saves the current Matplotlib figure as a PNG file in `reports/figures/`, creating the directory if it does not exist. Uses 300 DPI by default and automatically adjusts the bounding box to fit the figure content.