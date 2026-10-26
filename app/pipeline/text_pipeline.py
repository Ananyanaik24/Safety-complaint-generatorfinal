import re
from app.preprocessing.english_preprocessing import preprocess_english
from app.preprocessing.hindi_preprocessing import (
    preprocess_hindi,
    preprocess_hindi_full,
)
from app.translation.translator import translate_hindi_to_english


def is_devanagari(text: str) -> bool:
    """Check if string contains Devanagari (Hindi) script."""
    if not text:
        return False
    return bool(re.search(r"[\u0900-\u097F]", str(text)))


def process_complaint(text, language):
    """
    Process a complaint based on the selected language.

    English: English preprocessing.
    Hindi:   Hindi preprocessing (lemmatization + stopword removal),
             then translation to English, then English preprocessing.
    """
    if not isinstance(text, str) or not text.strip():
        return {
            "original_text": "",
            "hindi_processed": "",
            "hindi_full_processed": "",
            "translated_text": "",
            "english_processed": ""
        }

    language = language.lower()

    # ---------------- English complaint ----------------
    if language == "english":
        english_processed = preprocess_english(text)
        return {
            "original_text": text,
            "hindi_processed": "",
            "hindi_full_processed": "",
            "translated_text": text,
            "english_processed": english_processed
        }

    # ---------------- Hindi complaint ----------------
    elif language == "hindi":

        # 1. Light cleaning (kept as before)
        hindi_processed = preprocess_hindi(text)

        # 2. Full Hindi preprocessing: lemmatization + stopword removal.
        # try/except so a Stanza problem never breaks the whole app.
        try:
            hindi_full_processed = preprocess_hindi_full(text)
        except Exception as e:
            print(f"[HINDI PREPROCESSING ERROR] {e}")
            hindi_full_processed = ""

        # 3. Translate the original Hindi text.
        # Used for entities, similarity and formal complaint drafts,
        # which need full natural sentences.
        translated_text = translate_hindi_to_english(text)

        # Safety fallback if translation returns empty or raw Hindi
        if not translated_text or is_devanagari(translated_text):
            translated_text = translate_hindi_to_english(hindi_processed) or text

        # 4. Classifier input: translate the heavily preprocessed Hindi text.
        # Falls back to the full translation if this step fails.
        classifier_text = translated_text
        if hindi_full_processed:
            candidate = translate_hindi_to_english(hindi_full_processed)
            if candidate and not is_devanagari(candidate):
                classifier_text = candidate

        # 5. English preprocessing on the text going to the classifier
        english_processed = preprocess_english(classifier_text)

        return {
            "original_text": text,
            "hindi_processed": hindi_processed,
            "hindi_full_processed": hindi_full_processed,
            "translated_text": translated_text,
            "english_processed": english_processed
        }

    else:
        raise ValueError("Language must be either 'Hindi' or 'English'.")