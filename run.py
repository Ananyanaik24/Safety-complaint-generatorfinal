
from datetime import date as today_date, datetime
import re
from flask import Flask, render_template, request

from app.pipeline.complaint_pipeline import run_complaint_pipeline

app = Flask(
    __name__,
    template_folder="frontend/templates",
    static_folder="frontend/static",
)


def is_hindi_text(text: str) -> bool:
    """Detect if the input string contains Devanagari (Hindi) characters."""
    return bool(re.search(r"[\u0900-\u097F]", text))


@app.route("/")
def home():
    return render_template(
        "index.html",
        today=today_date.today().isoformat()
    )


@app.route("/submit", methods=["POST"])
def submit_complaint():
    complaint = request.form.get("complaint", "").strip()
    selected_language = request.form.get("language", "").strip()
    date = request.form.get("date", "").strip()
    time = request.form.get("time", "").strip()
    location = request.form.get("location", "").strip()

    # 1. Date validation
    if date:
        try:
            selected_date = datetime.strptime(date, "%Y-%m-%d").date()

            if selected_date > today_date.today():
                return render_template(
                    "index.html",
                    error="Please select today or an earlier date.",
                    today=today_date.today().isoformat(),
                )

        except ValueError:
            return render_template(
                "index.html",
                error="Please enter a valid date.",
                today=today_date.today().isoformat(),
            )

    # 2. Complaint empty check
    if not complaint:
        return render_template(
            "index.html",
            error="Please enter a complaint before submitting.",
            today=today_date.today().isoformat(),
        )

    # 3. Resolve complaint language
    if is_hindi_text(complaint):
        active_language = "Hindi"
    elif selected_language in ["English", "Hindi"]:
        active_language = selected_language
    else:
        active_language = "English"

    # 4. Run complaint processing pipeline
    try:
        result = run_complaint_pipeline(
            complaint=complaint,
            language=active_language,
            date=date,
            time=time,
            location=location,
        )

        return render_template(
            "index.html",
            result=result,
            today=today_date.today().isoformat(),
        )

    except Exception as e:
        print(f"\n[PIPELINE ERROR] {e}", flush=True)

        return render_template(
            "index.html",
            error="Something went wrong while processing the complaint.",
            today=today_date.today().isoformat(),
        )


def print_model_details():
    """Print details of the saved complaint classification model."""
    print("\n" + "=" * 60, flush=True)
    print("SAFETY COMPLAINT GENERATOR - MODEL DETAILS", flush=True)
    print("=" * 60, flush=True)

    try:
        from app.complaint.classifier import model, vectorizer

        print(
            f"Saved classification model: {type(model).__name__}",
            flush=True,
        )
        print(
            f"Saved text vectorizer: {type(vectorizer).__name__}",
            flush=True,
        )
        print(
            f"Model classes: {getattr(model, 'classes_', 'Not available')}",
            flush=True,
        )

        print("\nModel files:", flush=True)
        print("  models/complaint_model.pkl", flush=True)
        print("  models/tfidf_vectorizer.pkl", flush=True)

    except Exception as e:
        print(
            f"[MODEL DETAILS ERROR] Could not load model details: {e}",
            flush=True,
        )

    print("=" * 60, flush=True)


def print_evaluation_metrics():
    """Run the saved-model and Naive Bayes evaluation, if configured."""
    print("\n" + "=" * 60, flush=True)
    print("MODEL EVALUATION", flush=True)
    print("=" * 60, flush=True)

    try:
        from app.complaint.model_evaluation import evaluate_models

        evaluate_models()

    except ImportError as e:
        print(
            "[EVALUATION ERROR] Could not import model_evaluation.py.",
            flush=True,
        )
        print(f"Details: {e}", flush=True)

    except Exception as e:
        print(
            "[EVALUATION ERROR] Evaluation could not be completed.",
            flush=True,
        )
        print(f"Details: {e}", flush=True)


if __name__ == "__main__":
    print_model_details()
    print_evaluation_metrics()

    print("\nStarting Flask website...", flush=True)
    app.run(debug=True, use_reloader=False)
