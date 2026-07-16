"""Train and evaluate a KNN classifier on the Iris dataset.

Run from this folder with: python main.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


RANDOM_STATE = 42
TEST_SIZE = 0.20
OUTPUT_DIR = Path("results")


def load_data() -> tuple[pd.DataFrame, pd.Series, list[str]]:
    """Load Iris data and return features, labels, and readable class names."""
    iris = load_iris()
    features = pd.DataFrame(iris.data, columns=iris.feature_names)
    labels = pd.Series(iris.target, name="species")
    return features, labels, list(iris.target_names)


def build_model() -> GridSearchCV:
    """Create a leakage-safe pipeline and tune K using stratified CV."""
    pipeline = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("knn", KNeighborsClassifier()),
        ]
    )
    return GridSearchCV(
        estimator=pipeline,
        param_grid={"knn__n_neighbors": list(range(1, 16, 2)), "knn__weights": ["uniform", "distance"]},
        scoring="f1_macro",
        cv=5,
        n_jobs=-1,
    )


def save_confusion_matrix(y_true: pd.Series, y_pred, class_names: list[str]) -> None:
    """Save a labelled confusion-matrix image for the project submission."""
    matrix = confusion_matrix(y_true, y_pred)
    figure, axis = plt.subplots(figsize=(7, 5))
    display = ConfusionMatrixDisplay(confusion_matrix=matrix, display_labels=class_names)
    display.plot(ax=axis, cmap="Blues", colorbar=False)
    axis.set_title("Iris KNN Confusion Matrix")
    figure.tight_layout()
    figure.savefig(OUTPUT_DIR / "confusion_matrix.png", dpi=200)
    plt.close(figure)


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    x, y, class_names = load_data()
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )

    model = build_model()
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision_macro": precision_score(y_test, predictions, average="macro", zero_division=0),
        "recall_macro": recall_score(y_test, predictions, average="macro", zero_division=0),
        "f1_macro": f1_score(y_test, predictions, average="macro", zero_division=0),
        "best_parameters": model.best_params_,
        "training_rows": len(x_train),
        "test_rows": len(x_test),
    }
    pd.DataFrame([metrics]).to_csv(OUTPUT_DIR / "metrics.csv", index=False)
    save_confusion_matrix(y_test, predictions, class_names)

    print("Iris KNN classifier completed")
    print(f"Training/test rows: {len(x_train)}/{len(x_test)}")
    print(f"Best parameters: {model.best_params_}")
    print(f"Accuracy: {metrics['accuracy']:.3f}")
    print(f"Macro F1: {metrics['f1_macro']:.3f}\n")
    print(classification_report(y_test, predictions, target_names=class_names, zero_division=0))
    print("Saved results/metrics.csv and results/confusion_matrix.png")


if __name__ == "__main__":
    main()
