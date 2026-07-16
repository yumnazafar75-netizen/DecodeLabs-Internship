# Iris data classification using KNN

This is a complete implementation of the Project 2 brief. It uses the built-in Iris dataset (150 samples, 3 balanced species, and 4 flower measurements) to predict the species from its measurements.

## What it does

1. Loads and inspects the Iris dataset.
2. Uses a stratified 80/20 training-test split, with a fixed random seed for reproducibility.
3. Applies `StandardScaler` inside a pipeline. This prevents test-data leakage and is important for distance-based KNN.
4. Uses 5-fold cross-validation on the training set to select the best odd value of K (1 through 15) and weighting strategy.
5. Evaluates the held-out test set with accuracy, macro precision, macro recall, macro F1, a classification report, and a confusion matrix.

## Run it

In a terminal opened in this folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

The `results` folder will contain:

- `metrics.csv` - concise submission-ready metric summary.
- `confusion_matrix.png` - visual model evaluation.

## Explain it in your submission

"I trained a K-Nearest Neighbors classifier to classify Iris flowers. I split the data into 80% training and 20% test data with stratification, standardized the feature values, and chose K through five-fold cross-validation. I then evaluated the final model only on the unseen test data using accuracy, precision, recall, F1 score, and a confusion matrix."

## Important concepts

- **Scaling**: KNN measures distance. Measurements with a larger numeric range would otherwise dominate the result.
- **Stratification**: keeps each species represented in both training and testing data.
- **Macro F1**: gives every species equal importance, making it more informative than accuracy alone.
- **Pipeline**: fits the scaler only on training folds, avoiding leakage into testing data.
