import logging
import os
from pathlib import Path

import joblib

from data_preprocessing import (
    load_vendor_invoice_data, 
    prepare_features, 
    split_data
)

from modeling_evaluation import (
    train_decision_tree,
    train_linear_regression,
    train_random_forest,
    evaluate_model
)

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/train_freight_cost_prediction.log",
    level=logging.DEBUG,
    force=True,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode="w",
)

def main():
    db_path = "data/inventory.db"
    model_dir = Path("models")
    model_dir.mkdir(exist_ok=True)

    # Load data 
    df = load_vendor_invoice_data(db_path)

    # Prepare data
    X, y = prepare_features(df)
    X_train, X_test, y_train, y_test = split_data(X, y)

    # Train models
    lr_model = train_linear_regression(X_train, y_train)
    dt_model = train_decision_tree(X_train, y_train)
    rf_model = train_random_forest(X_train, y_train)

    # Evaluate models
    results = []
    results.append(evaluate_model(lr_model, X_test, y_test, "Linear Regression"))
    results.append(evaluate_model(dt_model, X_test, y_test, "Decision Tree"))
    results.append(evaluate_model(rf_model, X_test, y_test, "Random Forest"))

    # Select best model based on low "mae"
    best_model_info = min(results, key=lambda x : x['mae'])
    best_model_name = best_model_info["model_name"]

    best_model = {
        "Linear Regression" : lr_model,
        "Decision Tree" : dt_model,
        "Random Forest": rf_model
    }[best_model_name]

    # Save best model
    model_path = model_dir / "predict_freight_model.pkl"
    joblib.dump(best_model, model_path)

    logging.info(f"\nBest model saved: {best_model_name}")
    logging.info(f"Model path: {model_path}")

if __name__ == "__main__":
    main()
