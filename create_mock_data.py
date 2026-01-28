#!/usr/bin/env python3
"""Create mock training data for State"""

import numpy as np
import anndata as ad
import pandas as pd
from pathlib import Path

# Set random seed for reproducibility
np.random.seed(42)

# Parameters
n_cells = 1000
n_genes = 2000
n_hvg = 500

# Create mock expression data
X = np.random.negative_binomial(5, 0.3, size=(n_cells, n_genes))

# Create cell metadata
cell_types = np.random.choice(['CT1', 'CT2', 'CT3', 'CT4'], n_cells)
targets = np.random.choice(
    ['TARGET1', 'TARGET2', 'TARGET3', 'TARGET4', 'TARGET5', 'DMSO_TF'], 
    n_cells, 
    p=[0.15, 0.15, 0.15, 0.15, 0.15, 0.25]
)
gem_groups = np.random.choice(['batch1', 'batch2', 'batch3'], n_cells)

obs = pd.DataFrame({
    'cell_type': pd.Categorical(cell_types),
    'target_gene': pd.Categorical(targets),
    'gem_group': pd.Categorical(gem_groups),
})

# Create gene metadata
var = pd.DataFrame({
    'gene_name': [f'GENE_{i}' for i in range(n_genes)],
    'highly_variable': [i < n_hvg for i in range(n_genes)],
})
var.index = var['gene_name']

# Create AnnData object
adata = ad.AnnData(X=X, obs=obs, var=var)

# Normalize and log-transform (simulate preprocessing)
from scipy.sparse import csr_matrix
adata.layers['counts'] = adata.X.copy()

# Simple normalization
size_factors = adata.X.sum(axis=1)
X_norm = adata.X / size_factors[:, None] * 1e4
X_log = np.log1p(X_norm)
adata.X = X_log

# Add HVG matrix
adata.obsm['X_hvg'] = adata[:, adata.var['highly_variable']].X

# Save dataset by split
output_dir = Path('examples')
output_dir.mkdir(exist_ok=True)

# Create train directory
train_dir = output_dir / 'train'
train_dir.mkdir(exist_ok=True)

# Save as random.h5ad for compatibility
adata.write_h5ad(output_dir / 'random.h5ad')
print(f"Created mock dataset: {output_dir / 'random.h5ad'}")
print(f"Shape: {adata.shape}")
print(f"Cell types: {adata.obs['cell_type'].unique()}")
print(f"Targets: {adata.obs['target_gene'].unique()}")
print(f"Batches: {adata.obs['gem_group'].unique()}")
