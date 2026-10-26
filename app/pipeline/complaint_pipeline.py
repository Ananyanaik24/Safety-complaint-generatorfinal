
from datetime import datetime

from app.complaint.classifier import predict_category
from app.pipeline.text_pipeline import process_complaint
from app.ner.entity_extraction import extract_entities
from app.complaint.advice import get_safety_advice
from app.complaint.generator import generate_formal_complaint
from app.similarity.complaint_similarity import find_similar_complaints
from app.database.mongodb import save_complaint


def run_complaint_pipeline(
    complaint,
    language,
    date="",
    time="",
    location="",
):
    """
    Run the complete complaint processing pipeline.

    Returns the complaint record with its predicted category,
    safety advice, similar complaints and formal complaint drafts.
    """

    # 1. Process complaint text.
    processed = process_complaint(complaint, language)

    # 2. Obtain English text for classification and entity extraction.
    english_text = processed["translated_text"]

    # 3. Extract entities from English text.
    entities = extract_entities(english_text)

    # 4. Predict the complaint category.
    prediction = predict_category(
        processed["english_processed"]
    )

    category = prediction["category"]
    print("DEBUG - Classifier prediction:", prediction)
    print("DEBUG - Category passed to generator:", category)
    confidence = prediction["confidence"]

    # 5. Retrieve similar historical complaints.
    similar_complaints = find_similar_complaints(
        english_text,
        category=category,
        top_n=5,
    )

    # 6. Generate detailed safety advice in the selected language.
    safety_advice = get_safety_advice(
        category=category,
        language=language,
        complaint=complaint,
    )

    # 7. Generate detailed formal complaints in both languages.
    formal_complaints = generate_formal_complaint(
        original_complaint=complaint,
        category=category,
        entities=entities,
        language=language,
        date=date,
        time=time,
        location=location,
        translated_complaint=english_text,
    )

    # 8. Build the database record.
    complaint_record = {
        "original_complaint": complaint,
        "language": language,
        "hindi_processed": processed["hindi_processed"],
        "hindi_full_processed": processed["hindi_full_processed"],
        "translated_complaint": english_text,
        "english_processed": processed["english_processed"],
        "date": date,
        "time": time,
        "location": location,
        "category": category,
        "confidence": confidence,
        "entities": entities,
        "similar_complaints": similar_complaints,
        "safety_advice": safety_advice,
        "formal_english": formal_complaints["formal_english"],
        "formal_hindi": formal_complaints["formal_hindi"],
        "created_at": datetime.now(),
    }

    # 9. Save the record and return it to the frontend.
    document_id = save_complaint(complaint_record)
    complaint_record["document_id"] = document_id

    return complaint_record
