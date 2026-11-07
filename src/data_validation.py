
def validate_sample_alignment(counts_df, metadata):
    """Validate that count data and metadata contain the same samples."""
    assert counts_df.index.is_unique, "Duplicate sample IDs in counts."
    assert metadata.index.is_unique, "Duplicate sample IDs in metadata."

    missing_samples = counts_df.index.difference(metadata.index)
    extra_samples = metadata.index.difference(counts_df.index)

    assert len(missing_samples) == 0, (
        f"Samples missing from metadata: {len(missing_samples)}"
    )
    assert len(extra_samples) == 0, (
        f"Extra samples in metadata: {len(extra_samples)}"
    )

    metadata = metadata.loc[counts_df.index]

    assert counts_df.index.equals(metadata.index), (
        "Sample order mismatch."
    )

    return metadata


def validate_count_matrix(counts_df):
    """Validate the integrity of a gene expression count matrix."""
    assert counts_df.notna().all().all(), "Missing values in count matrix."
    assert (counts_df >= 0).all().all(), "Negative values found."
    assert (counts_df % 1 == 0).all().all(), (
        "Non-integer values found in count matrix."
    )


def validate_metadata(metadata, required_columns=None):
    """Validate metadata structure and required columns."""
    if required_columns is not None:
        missing_columns = set(required_columns) - set(metadata.columns)

        assert not missing_columns, (
            f"Missing metadata columns: {missing_columns}"
        )
