# Vendor Performance and Invoice Intelligence

## Overview

This project is a data science and machine learning workspace focused on vendor performance analysis and invoice intelligence. It combines:

- Freight cost prediction for vendor invoices
- Invoice risk flagging for manual approval workflows
- Vendor performance analysis using purchase, sales, and inventory data
- A Streamlit-based analytics portal for business users

The solution is designed to support finance, procurement, and operations teams by helping them identify unusually expensive invoices, estimate freight costs, and understand vendor behavior.

---

## Business Problem

Organizations often face two recurring problems in their vendor invoice workflows:

1. Freight cost is not always obvious from invoice value alone.
2. Some invoices should be reviewed manually because they look risky or inconsistent.

This project addresses both problems by training predictive models that can:

- Estimate freight cost from invoice-related features
- Flag invoices that may require manual approval

It also includes deeper vendor-level analysis to inspect purchasing behavior, profitability, inventory efficiency, and concentration risk.

---

## Project Goals

The project aims to:

- Predict approximate freight cost for incoming invoices
- Detect invoices that may be abnormal or high-risk
- Reduce manual review effort in finance operations
- Support procurement strategy with vendor and product performance insights
- Provide a lightweight dashboard for business users

---

## Solution Architecture

The repository is organized into four main areas:

1. Data ingestion and preparation
2. Machine learning model training and evaluation
3. Inference scripts for production-style prediction
4. A Streamlit app for end-user interaction

### High-level workflow

- Raw source data is stored in the data folder as CSV files
- Data is loaded into an SQLite database for analysis and modeling
- Machine learning models are trained and saved into the models folder
- Inference scripts load the trained models and generate predictions
- The Streamlit app provides a simple interface for business users

---

## Repository Structure

```text
.
├── app.py
├── EDA.md
├── assets/
├── data/
│   ├── begin_inventory.csv
│   ├── end_inventory.csv
│   ├── purchase_prices.csv
│   ├── purchases.csv
│   ├── sales.csv
│   ├── vendor_invoice.csv
│   └── inventory.db
├── logs/
├── models/
│   ├── predict_freight_model.pkl
│   ├── predict_flag_invoice.pkl
│   └── scaler.pkl
├── notebook/
│   ├── eda.ipynb
│   ├── ingest.ipynb
│   ├── invoice_flagging.ipynb
│   ├── predicting_freight_cost.ipynb
│   └── vendor_performance_analysis.ipynb
└── scripts/
    ├── data_analysis/
    │   ├── get_vendor_summary.py
    │   └── ingestion_db.py
    ├── freight_cost_prediction/
    │   ├── data_preprocessing.py
    │   ├── modeling_evaluation.py
    │   └── train.py
    ├── inference/
    │   ├── predict_freight.py
    │   └── predict_invoice_flag.py
    └── invoice_flagging/
        ├── data_processing.py
        ├── modeling_evaluation.py
        └── train.py
```

---

## Main Components

### 1. Streamlit Application

The main application entry point is [app.py](app.py).

It provides a dashboard with two prediction modules:

- Freight Cost Prediction
- Invoice Manual Approval Flag

The interface allows a user to input invoice information and receive a prediction instantly.

### 2. Freight Cost Prediction

The freight prediction workflow is implemented under [scripts/freight_cost_prediction](scripts/freight_cost_prediction).

It trains a regression model using invoice dollar values and predicts freight cost.

### 3. Invoice Flagging

The invoice risk workflow is implemented under [scripts/invoice_flagging](scripts/invoice_flagging).

It trains a classifier to label invoices as either safe or needing manual review based on invoice and purchase characteristics.

### 4. Vendor Performance Analysis

The vendor performance analysis pipeline is implemented under [scripts/data_analysis](scripts/data_analysis).

It creates a vendor sales summary table and performs exploratory analysis around:

- Sales contribution by vendor
- Purchase behavior
- Profitability
- Inventory turnover
- Working capital pressure from slow-moving stock

### 5. Notebooks

The notebooks in [notebook](notebook) are useful for exploration, experimentation, and iterative analysis:

- eda.ipynb: exploratory analysis
- ingest.ipynb: ingestion and DB preparation
- invoice_flagging.ipynb: invoice-risk modeling experiments
- predicting_freight_cost.ipynb: freight prediction experiments
- vendor_performance_analysis.ipynb: vendor analysis and reporting

---

## Data Sources

The project works with data stored in the data folder and the generated SQLite database.

### Raw CSV files

- begin_inventory.csv
- end_inventory.csv
- purchase_prices.csv
- purchases.csv
- sales.csv
- vendor_invoice.csv

### Relational database

The repository includes a generated SQLite database file at [data/inventory.db](data/inventory.db).

The main analytical tables used by the scripts include:

- vendor_invoice
- purchases
- purchase_prices

### Key input features used by the model

#### Freight prediction

The freight model uses the following feature:

- Dollars

#### Invoice flagging

The invoice flagging model uses the following features:

- invoice_quantity
- invoice_dollars
- Freight
- total_item_quantity
- total_item_dollars

---

## Environment Setup

### Prerequisites

- Python 3.11 or newer
- pip
- A terminal or command prompt

### Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Install dependencies

Install the following packages:

```bash
pip install pandas numpy scikit-learn joblib plotly streamlit sqlalchemy
```

If you prefer to manage dependencies in a requirements file, you can also add them there and install from that file.

---

## Running the Streamlit App

From the project root, run:

```bash
streamlit run app.py
```

This will launch the dashboard in your browser.

### App capabilities

Once the app is running, you can:

- Choose the Freight Cost Prediction module
- Enter invoice data and obtain a freight estimate
- Choose the Invoice Manual Approval Flag module
- Input invoice features and view whether the invoice should be flagged

---

## Training the Models

### Freight prediction model

Run the training script from the project root:

```bash
python scripts/freight_cost_prediction/train.py
```

This script:

- Loads vendor invoice data from the SQLite database
- Prepares features and target variables
- Trains multiple regression models
- Evaluates model performance
- Saves the best model as [models/predict_freight_model.pkl](models/predict_freight_model.pkl)

### Invoice flagging model

Run:

```bash
python scripts/invoice_flagging/train.py
```

This script:

- Loads invoice-related data from the SQLite database
- Creates the target label for invoice risk
- Splits data into training and test sets
- Scales features
- Trains a random forest classifier
- Saves the trained model as [models/predict_flag_invoice.pkl](models/predict_flag_invoice.pkl)

---

## Running Inference

### Predict freight cost

```bash
python scripts/inference/predict_freight.py
```

### Predict invoice flag

```bash
python scripts/inference/predict_invoice_flag.py
```

These scripts load the saved model artifacts from the models folder and return predictions for sample input.

---

## Vendor Summary and Analysis Pipeline

The vendor performance analysis pipeline creates a summary dataset for deeper analysis.

### Build vendor summary

The script [scripts/data_analysis/get_vendor_summary.py](scripts/data_analysis/get_vendor_summary.py) prepares a consolidated dataset that includes:

- Vendor number and name
- Brand and description
- Purchase quantity and purchase dollars
- Sales quantity and sales dollars
- Freight cost
- Gross profit
- Profit margin
- Stock turnover
- Sales-to-purchase ratio

### Database ingestion

The ingestion script [scripts/data_analysis/ingestion_db.py](scripts/data_analysis/ingestion_db.py) is used to load raw CSV files into the SQLite database.

If you need to rebuild the database or modify the ingestion logic, make sure the paths are aligned with your local working directory.

---

## Model Artifacts

Trained model files are stored in [models](models):

- [models/predict_freight_model.pkl](models/predict_freight_model.pkl): trained model for freight prediction
- [models/predict_flag_invoice.pkl](models/predict_flag_invoice.pkl): trained model for invoice flagging
- [models/scaler.pkl](models/scaler.pkl): scaler used for invoice flagging features

These files are used by the inference scripts and the Streamlit app.

---

## Logging and Outputs

The project writes logs into the [logs](logs) directory during training and data processing. These logs help with troubleshooting and auditability.

Typical log files include:

- train_freight_cost_prediction.log
- train_invoice_flagging.log
- vendor_sales_summary.log
- ingestion_db.log

---

## Example Use Cases

### Use case 1: Freight estimation

A finance team can input invoice amount and quantity to estimate freight without manually reviewing historical invoices.

### Use case 2: Invoice review automation

A procurement team can use the invoice-flagging model to rapidly identify invoices that may require secondary review.

### Use case 3: Vendor analytics

A procurement analyst can inspect vendor-level profitability, purchase concentration, and turnover to spot risk or improvement opportunities.

---

## Notes and Recommendations

- The project is currently structured around a local SQLite workflow, which makes it easy to run and experiment with.
- If the data changes significantly, retraining the models is recommended.
- The Streamlit app depends on the trained model files being present in the models folder.
- The notebooks are a good starting point for exploratory analysis and experimentation.

---

## Future Enhancements

Potential next steps for this project include:

- Adding more features to improve model accuracy
- Deploying the app as a web service or cloud-hosted dashboard
- Supporting automated retraining on new data
- Adding SHAP or feature-importance analysis for explainability
- Building a full production pipeline with CI/CD and monitoring

---

## Summary

This repository provides a practical end-to-end solution for:

- Freight cost prediction
- Invoice risk flagging
- Vendor performance analysis
- Interactive business-facing analytics

It is suitable for both exploratory analysis and lightweight operational use inside a finance or procurement function.
