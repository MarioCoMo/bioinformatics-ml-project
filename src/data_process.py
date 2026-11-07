"""Utilities for processing TCGA/GDC gene expression data."""

import json
from pathlib import Path

import pandas as pd


def load_file_to_sample_map(metadata_file, id_length=15):
    """Read the GDC metadata JSON and return {file_name: sample_id}."""
    with open(metadata_file, "r") as f:
        metadata = json.load(f)

    return {
        item["file_name"]: item["associated_entities"][0]["entity_submitter_id"][:id_length]
        for item in metadata
    }


def process_expression_data(
    data_dir,
    metadata_file=None,
    output_dir="../data/processed",
    output_prefix="tcga_brca",
    suffix="CANCER",
    id_length=15,
    count_col="unstranded",
    tpm_col="tpm_unstranded",
    save=True,
):
    """
    Process GDC gene expression TSV files and build raw counts and TPM
    matrices (rows = samples, columns = genes).

    Parameters
    ----------
    data_dir : str | Path
        Root folder containing the TSV files (searched recursively).
    metadata_file : str | Path, optional
        Metadata JSON file. Defaults to data_dir / f"metadata.{suffix.lower()}.json".
    output_dir : str | Path
        Folder where the output CSV files are saved.
    output_prefix : str
        Prefix for the output file names.
    suffix : str
        Suffix for the output file names (e.g. "CANCER", "NORMAL").
    id_length : int
        Number of characters of the submitter id to keep: 15 -> sample
        (TCGA-XX-XXXX-01A), 12 -> patient (TCGA-XX-XXXX).
    count_col, tpm_col : str
        Names of the raw counts and TPM columns in the TSV files.
    save : bool
        If True, save the CSV files in output_dir.

    Returns
    -------
    (df_counts, df_tpm) : tuple[pd.DataFrame, pd.DataFrame]
    """
    data_dir = Path(data_dir)
    metadata_file = (
        Path(metadata_file)
        if metadata_file
        else data_dir / f"metadata.{suffix.lower()}.json"
    )
    file_to_sample = load_file_to_sample_map(metadata_file, id_length)

    counts_data = {}
    tpm_data = {}

    tsv_files = list(data_dir.rglob("*.tsv"))
    print(f"Found {len(tsv_files)} TSV files. Processing...")

    for tsv_path in tsv_files:
        sample_id = file_to_sample.get(tsv_path.name)
        if sample_id is None:  # TSV file not listed in the metadata
            continue

        df = pd.read_csv(tsv_path, sep="\t", comment="#")

        # Drop sequencer summary rows (N_unmapped, N_multimapping, etc.)
        df = df[df["gene_id"].str.startswith("ENSG", na=False)]

        # Sum counts for duplicated gene symbols (several Ensembl IDs -> same HGNC symbol)
        df_grouped = df.groupby("gene_name")[[count_col, tpm_col]].sum()

        counts_data[sample_id] = df_grouped[count_col]
        tpm_data[sample_id] = df_grouped[tpm_col]

    # Rows = samples, columns = genes; fill missing genes with 0
    df_counts = pd.DataFrame(counts_data).T.fillna(0).astype(int)
    df_tpm = pd.DataFrame(tpm_data).T.fillna(0.0)

    if save:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        df_counts.to_csv(output_dir / f"{output_prefix}_raw_counts_{suffix}.csv")
        df_tpm.to_csv(output_dir / f"{output_prefix}_tpm_{suffix}.csv")

    print(f"Done: {df_counts.shape[0]} samples x {df_counts.shape[1]} genes.")
    return df_counts, df_tpm


def merge_cancer_control(
    cancer_file,
    control_file,
    output_dir="../data/processed",
    cancer_label="Cancer",
    control_label="Healthy",
    save=True,
):
    """
    Merge the raw counts of cancer and control samples into a single matrix
    and build the matching metadata table with a 'Condition' column.

    Parameters
    ----------
    cancer_file : str | Path
        CSV with the raw counts of cancer samples (rows = samples).
    control_file : str | Path
        CSV with the raw counts of control samples (rows = samples).
    output_dir : str | Path
        Folder where the output CSV files are saved.
    cancer_label, control_label : str
        Values used in the 'Condition' column.
    save : bool
        If True, save the CSV files in output_dir.

    Returns
    -------
    (df_raw_merged, df_metadata) : tuple[pd.DataFrame, pd.DataFrame]
    """
    df_cancer = pd.read_csv(cancer_file, index_col=0)
    df_control = pd.read_csv(control_file, index_col=0)

    # Merged counts matrix (control first, then cancer)
    df_raw_merged = pd.concat([df_control, df_cancer], axis=0)

    # Metadata: one 'Condition' value per sample
    df_metadata = pd.DataFrame(
        {"Condition": [control_label] * len(df_control) + [cancer_label] * len(df_cancer)},
        index=df_raw_merged.index,
    )

    if save:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        df_raw_merged.to_csv(output_dir / "raw_merged.csv")
        df_metadata.to_csv(output_dir / "metadata_merged.csv")

    print(f"Merged: {len(df_control)} control + {len(df_cancer)} cancer samples.")
    return df_raw_merged, df_metadata