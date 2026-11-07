# src/

## data_process.py

Builds and merges gene expression matrices from TCGA/GDC data.

- `load_file_to_sample_map(metadata_file, id_length=15)`: reads the GDC metadata JSON and returns a dictionary mapping each file name to its sample ID.
- `process_expression_data(data_dir, ...)`: reads all the TSV files in `data_dir`, keeps only genes (`ENSG` IDs), sums duplicated gene symbols, and returns two DataFrames (raw counts and TPM) with rows = samples and columns = genes. The metadata file defaults to `metadata.<suffix>.json` inside `data_dir`. Optionally saves the results as CSV files.
- `merge_cancer_control(cancer_file, control_file, ...)`: merges the cancer and control raw counts matrices into one and builds a metadata table with a `Condition` column (`Healthy` / `Cancer`). Optionally saves both as CSV files (`raw_merged.csv` and `metadata_merged.csv`).