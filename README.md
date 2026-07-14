# Evaluating Spatial Feature Engineering in CatBoost for UK Traffic Accident Severity Prediction

This repository contains the LaTeX source code, data processing scripts, and Jupyter notebooks for the paper "Evaluating Spatial Feature Engineering in CatBoost for UK Traffic Accident Severity Prediction". The project investigates whether explicit spatial features (like coordinate clusters and distances to major cities) improve the predictive performance of CatBoost models on highly imbalanced UK traffic accident data.

## Key Features

- **Machine Learning Pipeline**: Complete CatBoost classification pipeline handling high-cardinality categorical variables natively.
- **Spatial Feature Engineering**: Integration of KMeans spatial clustering and proximity metrics to urban centers.
- **LaTeX Manuscript**: Springer LLNCS formatted manuscript with automated generation scripts.
- **Data Visualization**: Generation of performance metrics, feature importance charts, and SHAP summary plots.

## Tech Stack

- **Language**: Python 3.9+, LaTeX
- **Machine Learning**: CatBoost, Scikit-Learn
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn, SHAP
- **Paper Formatting**: Springer LLNCS (Lecture Notes in Computer Science)

## Prerequisites

- Python 3.9 or higher
- TeX Live (or equivalent LaTeX distribution) with `pdflatex`
- Jupyter Notebook or JupyterLab

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/uk-traffic-accidents-catboost.git
cd uk-traffic-accidents-catboost
```

### 2. Install Python Dependencies

```bash
pip install pandas numpy scikit-learn catboost matplotlib seaborn shap jupyter
```

### 3. Dataset Setup

The raw accident dataset should be placed in the `dataset/` directory. (Note: Due to size constraints, the dataset is not included in the repository). 

### 4. Running the Notebooks

Launch Jupyter to explore the main analysis pipeline:

```bash
jupyter notebook UK_accidents.ipynb
```

Alternatively, run the local version:

```bash
jupyter notebook UK_accidents_local.ipynb
```

### 5. Compiling the Paper

To compile the LaTeX manuscript (`paper.tex`) into a PDF using `pdflatex`:

```bash
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex
```

## Architecture

### Directory Structure

```
├── dataset/                  # Raw and processed datasets (ignored in git)
├── draft_en/                 # Drafts and review notes
├── figures/                  # Generated figures and plots
├── llncs.cls                 # Springer LLNCS document class
├── paper.tex                 # Main LaTeX manuscript
├── references.bib            # BibTeX references
├── UK_accidents.ipynb        # Main analysis notebook
├── UK_accidents_local.ipynb  # Local analysis notebook
├── generate_tex.py           # Script to generate/update TeX tables/figures
├── generate_figures.py       # Script to generate visualizations
├── check_ai.py               # Utility to audit text for AI patterns
└── .agents/                  # Automation and pipeline agents
```

### Academic Pipeline Integration

This project is integrated with an automated academic research pipeline (`/ars-pipeline`), leveraging multi-agent workflows (`/scientific-writing`) to structure, draft, and refine the manuscript. The pipeline ensures formatting compliance, citation integrity, and rigorous review simulations.
