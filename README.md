# adata_plot

A package for plotting single-cell data with Altair and Scanpy.

## Installation

You can install the package using pip:

```bash
pip install adata_plot
```

## Usage

```bash
import scanpy as sc
import adata_plot as ap

adata = sc.datasets.pbmc3k()

# Generate a UMAP plot colored by cell type
plot = ap.int_plot(adata, "sc.pl.umap(target, color=['cell_type'])")
plot.show()
```
