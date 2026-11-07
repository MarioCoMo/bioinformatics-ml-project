
# Variance Stabilizing Transformation (VST)

## 1. Overview

**Full name:** Variance Stabilizing Transformation

**Domain:** Bioinformatics / RNA-seq

**Library:** DESeq2 (R / Bioconductor)

**Purpose:** Transform RNA-seq count data to reduce the dependence between mean expression and variance.

## 2. Why is it needed?

RNA-seq count data typically exhibits a mean-variance relationship.

Genes with higher expression levels tend to have higher variance, meaning that highly expressed genes can disproportionately influence downstream analyses.

This can affect:
- PCA
- Clustering
- Distance calculations
- Data visualization
- Machine Learning models

VST helps make variance more homogeneous across different expression levels.

## 3. Mathematical intuition

VST uses information about the estimated dispersion-mean relationship to stabilize variance.

It behaves approximately like a logarithmic transformation at higher expression levels.

Unlike a simple log transformation, VST accounts for the mean-variance relationship characteristic of RNA-seq count data.

## 4. When should it be used?

Typical applications:
- PCA and dimensionality reduction.
- Sample clustering.
- Heatmaps.
- Exploratory data analysis.
- Machine Learning preprocessing.
- Gene expression classification (e.g., cancer vs. healthy tissue).

## 5. Why is it useful for Machine Learning?

VST is useful as a preprocessing step for machine learning tasks involving RNA-seq data, including cancer vs. healthy tissue classification.

It helps by:
- Reducing mean-dependent variance across genes.
- Making gene expression features more comparable.
- Reducing the influence of highly expressed genes.
- Providing more appropriate input for distance-based algorithms (e.g., KNN and SVM).
- Supporting downstream dimensionality reduction and feature selection.

**Important:** VST does not guarantee better model performance. Its impact should be evaluated experimentally.

## 6. When should it NOT be used?

- VST-transformed values should not replace raw counts as input to DESeq2 differential expression statistical testing.
- VST does not eliminate batch effects.
- VST does not replace normalization.
- VST does not guarantee normally distributed data.
- VST is not necessarily required for every ML algorithm.

## 7. Implementation

```r
library(DESeq2)

# Apply variance stabilizing transformation
vsd <- vst(dds, blind = FALSE)

# Extract transformed expression matrix
vst_matrix <- assay(vsd)
```

The resulting matrix can be used for exploratory analysis and downstream machine learning.

## 8. Advantages

- Reduces mean-dependent variance.
- Facilitates exploratory analysis.
- Makes expression values more suitable for distance-based analysis.
- Helps prevent highly expressed genes from dominating certain analyses.
- Useful for downstream ML preprocessing.

## 9. Limitations

- Does not eliminate batch effects.
- Does not replace normalization.
- Does not guarantee improved predictive performance.
- Does not perform feature selection.
- Does not eliminate the need for appropriate feature scaling when required by the ML algorithm.

**Data leakage warning:** If VST or other preprocessing steps estimate parameters from the dataset, consider fitting them within each training fold during cross-validation. Never use information from the test fold to train or select your model.

## 10. References

- Love et al. (2014): Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2.
  https://doi.org/10.1186/s13059-014-0550-8

- DESeq2 documentation:
  https://bioconductor.org/packages/DESeq2/

## 11. Related concepts

- Size Factor Normalization
- Negative Binomial Distribution
- Gene Expression
- Batch Effects
- PCA
- Feature Selection
- Machine Learning Preprocessing
- Cross-Validation