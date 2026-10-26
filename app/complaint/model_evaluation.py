
import os

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

from app.complaint.classifier import (
    model as saved_model,
    vectorizer as saved_vectorizer,
    preprocess_for_model,
)

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

DATASET_PATH = os.path.join(
    BASE_DIR, "dataset", "english_dataset.csv"
)

TEXT_COLUMN = "complaint"
LABEL_COLUMN = "category"

TEST_SIZE = 0.20
RANDOM_STATE = 42


def print_metrics(model_name, y_true, y_pred, labels):
    print("\n" + "=" * 70)
    print(f"MODEL: {model_name}")
    print("=" * 70)

    print(f"Accuracy          : {accuracy_score(y_true, y_pred):.4f}")
    print(
        "Precision (macro) : "
        f"{precision_score(y_true, y_pred, average='macro', zero_division=0):.4f}"
    )
    print(
        "Recall (macro)    : "
        f"{recall_score(y_true, y_pred, average='macro', zero_division=0):.4f}"
    )
    print(
        "F1-score (macro)  : "
        f"{f1_score(y_true, y_pred, average='macro', zero_division=0):.4f}"
    )

    print("\nClassification Report:")
    print(
        classification_report(
            y_true,
            y_pred,
            labels=labels,
            zero_division=0,
        )
    )

    print("Confusion Matrix:")
    print("Label order:", labels)
    print(confusion_matrix(y_true, y_pred, labels=labels))


def evaluate_models():
    print("\n" + "#" * 70)
    print("SAFETY COMPLAINT GENERATOR - MODEL COMPARISON")
    print("#" * 70)

    print("Existing saved model:", type(saved_model).__name__)
    print("Existing vectorizer :", type(saved_vectorizer).__name__)
    print("Dataset             :", DATASET_PATH)

    if not os.path.isfile(DATASET_PATH):
        print("\nERROR: Dataset file not found.")
        return

    df = pd.read_csv(DATASET_PATH)

    if TEXT_COLUMN not in df.columns or LABEL_COLUMN not in df.columns:
        print("\nERROR: Expected dataset columns were not found.")
        print("Available columns:", df.columns.tolist())
        return

    df = df[[TEXT_COLUMN, LABEL_COLUMN]].dropna().copy()
    df[TEXT_COLUMN] = df[TEXT_COLUMN].astype(str).str.strip()
    df[LABEL_COLUMN] = df[LABEL_COLUMN].astype(str).str.strip()

    df = df[
        (df[TEXT_COLUMN] != "") &
        (df[LABEL_COLUMN] != "")
    ].drop_duplicates()

    class_counts = df[LABEL_COLUMN].value_counts()

    if len(class_counts) < 2 or class_counts.min() < 2:
        print("\nERROR: Each category needs at least two examples.")
        print(class_counts)
        return

    X_train, X_test, y_train, y_test = train_test_split(
        df[TEXT_COLUMN],
        df[LABEL_COLUMN],
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=df[LABEL_COLUMN],
    )

    labels = sorted(df[LABEL_COLUMN].unique())

    print(f"\nTotal complaints : {len(df)}")
    print(f"Training samples : {len(X_train)}")
    print(f"Testing samples  : {len(X_test)}")
    print(f"Categories       : {len(labels)}")

    # Preprocess using the same function as the application.
    X_train_clean = [
        preprocess_for_model(text) for text in X_train
    ]
    X_test_clean = [
        preprocess_for_model(text) for text in X_test
    ]

    # Fit TF-IDF only on the training split.
    comparison_vectorizer = TfidfVectorizer()
    X_train_tfidf = comparison_vectorizer.fit_transform(X_train_clean)
    X_test_tfidf = comparison_vectorizer.transform(X_test_clean)

    if X_train_tfidf.shape[1] == 0:
        print("\nERROR: No vocabulary could be created from training data.")
        return

    results = []

    # MODEL 1: Multinomial Naive Bayes
    nb_model = MultinomialNB()
    nb_model.fit(X_train_tfidf, y_train)
    nb_predictions = nb_model.predict(X_test_tfidf)

    print_metrics(
        "Multinomial Naive Bayes",
        y_test,
        nb_predictions,
        labels,
    )

    results.append({
        "Model": "Multinomial Naive Bayes",
        "Accuracy": accuracy_score(y_test, nb_predictions),
        "Precision": precision_score(
            y_test, nb_predictions, average="macro", zero_division=0
        ),
        "Recall": recall_score(
            y_test, nb_predictions, average="macro", zero_division=0
        ),
        "F1-score": f1_score(
            y_test, nb_predictions, average="macro", zero_division=0
        ),
    })

    # MODEL 2: Logistic Regression
    lr_model = LogisticRegression(
        max_iter=2000,
        random_state=RANDOM_STATE,
    )
    lr_model.fit(X_train_tfidf, y_train)
    lr_predictions = lr_model.predict(X_test_tfidf)

    print_metrics(
        "Logistic Regression",
        y_test,
        lr_predictions,
        labels,
    )

    results.append({
        "Model": "Logistic Regression",
        "Accuracy": accuracy_score(y_test, lr_predictions),
        "Precision": precision_score(
            y_test, lr_predictions, average="macro", zero_division=0
        ),
        "Recall": recall_score(
            y_test, lr_predictions, average="macro", zero_division=0
        ),
        "F1-score": f1_score(
            y_test, lr_predictions, average="macro", zero_division=0
        ),
    })

    # Side-by-side comparison
    comparison = pd.DataFrame(results).set_index("Model")

    print("\n" + "#" * 70)
    print("FINAL MODEL COMPARISON")
    print("#" * 70)
    print(comparison.round(4).to_string())

    # Select the model with the higher macro F1-score.
    selected_model = comparison["F1-score"].idxmax()

    print("\nSelection based on macro F1-score:")
    print(f"Selected model: {selected_model}")

    if selected_model == "Multinomial Naive Bayes":
        print("Naive Bayes performed better on macro F1-score for this split.")
    else:
        print(
            "Logistic Regression performed better on macro F1-score "
            "for this split."
        )

    print("\nEvaluation completed.")
    print("#" * 70)


if __name__ == "__main__":
    evaluate_models()
