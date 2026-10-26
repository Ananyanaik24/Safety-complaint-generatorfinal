import re
import unicodedata


# ---------------------------------------------------------------
# Hindi stopwords
# ---------------------------------------------------------------
# Common function words that carry no complaint meaning
_HINDI_STOPWORDS = {
    "का", "की", "के", "को", "से", "में", "पर", "और", "या", "भी", "ही",
    "तो", "कि", "है", "हैं", "था", "थी", "थे", "हो", "होता", "होती",
    "होते", "हुआ", "हुई", "हुए", "रहा", "रही", "रहे", "गया", "गई",
    "गए", "गयी", "गये", "कर", "करके", "करना", "करने", "किया",
    "करता", "करती", "करते", "वाला", "वाली", "वाले", "यह", "ये", "वह",
    "वे", "इस", "इन", "उस", "उन", "इसके", "उसके", "इसमें", "उसमें",
    "एक", "कोई", "कुछ", "सब", "सभी", "बहुत", "अपना", "अपनी", "अपने",
    "मैं", "मैंने", "मुझे", "मुझसे", "मेरा", "मेरी", "मेरे", "हम",
    "हमें", "हमारा", "हमारी", "हमारे", "तुम", "आप", "उसने", "उन्होंने",
    "जो", "जब", "तब", "जहाँ", "वहाँ", "यहाँ", "क्या", "क्यों", "कैसे",
    "कब", "कहाँ", "लिए", "साथ", "द्वारा", "तक", "अब", "फिर", "सकता",
    "सकती", "सकते", "पास", "ऊपर", "नीचे", "बाद", "पहले", "लेकिन",
    "परंतु", "अगर", "तथा", "एवं", "जैसे", "जैसा", "इसलिए",
}

# Negations change the meaning of a complaint, so they must NEVER be removed
# ("धमकी नहीं दी" and "धमकी दी" mean opposite things).
_NEGATIONS = {"नहीं", "नही", "न", "ना", "मत", "बिना", "नहि"}

HINDI_STOPWORDS = _HINDI_STOPWORDS - _NEGATIONS


# ---------------------------------------------------------------
# Hindi lemmatizer (Stanza), loaded only when first needed
# ---------------------------------------------------------------
_nlp = None
_stanza_failed = False


def _get_stanza():
    """Load the Stanza Hindi pipeline once (downloads the model on first use)."""
    global _nlp, _stanza_failed

    if _nlp is not None or _stanza_failed:
        return _nlp

    try:
        import stanza

        try:
            _nlp = stanza.Pipeline(
                "hi",
                processors="tokenize,pos,lemma",
                tokenize_pretokenized=True,
                verbose=False
            )
        except Exception:
            stanza.download("hi", verbose=False)
            _nlp = stanza.Pipeline(
                "hi",
                processors="tokenize,pos,lemma",
                tokenize_pretokenized=True,
                verbose=False
            )

    except Exception as e:
        print(f"[HINDI PREPROCESSING WARNING] Stanza unavailable, using fallback stemmer: {e}")
        _stanza_failed = True
        _nlp = None

    return _nlp


# Rough suffix stripping, used ONLY if Stanza cannot load
_SUFFIXES = ["ियों", "ियाँ", "ियां", "ाएँ", "ाएं", "ाओं", "ों", "ें", "ा", "ी", "े"]


def _simple_stem(word):
    for suffix in _SUFFIXES:
        if word.endswith(suffix) and len(word) - len(suffix) >= 2:
            return word[: -len(suffix)]
    return word


def lemmatize_hindi(tokens):
    """Return one lemma per token (same length as the input list)."""
    if not tokens:
        return []

    nlp = _get_stanza()

    if nlp is None:
        return [_simple_stem(token) for token in tokens]

    # Input is already tokenized, so pass it as one sentence
    doc = nlp([tokens])

    lemmas = []
    for word in doc.sentences[0].words:
        lemmas.append(word.lemma if word.lemma else word.text)

    return lemmas


# ---------------------------------------------------------------
# 1. LIGHT preprocessing (your existing function, unchanged)
#    Used before translation to English.
# ---------------------------------------------------------------
def preprocess_hindi(text):
    """
    Perform light preprocessing on Hindi complaint text.

    Hindi text is only lightly cleaned because it will
    be translated into English later.

    Steps:
    1. Normalize Unicode
    2. Remove unnecessary punctuation/symbols
    3. Normalize whitespace
    4. Return cleaned Hindi text
    """

    # Make sure input is a string
    if not isinstance(text, str):
        return ""

    # 1. Unicode normalization
    text = unicodedata.normalize("NFC", text)

    # 2. Remove unnecessary punctuation and symbols
    # Keep Hindi characters, English characters, numbers and spaces
    text = re.sub(
        r"[^\u0900-\u097F a-zA-Z0-9]",
        " ",
        text
    )

    # 3. Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ---------------------------------------------------------------
# 2. FULL preprocessing (new): mirrors preprocess_english()
# ---------------------------------------------------------------
def preprocess_hindi_full(text):
    """
    Full Hindi preprocessing, matching the English pipeline.

    Steps:
    1. Normalize Unicode
    2. Remove unnecessary characters
    3. Tokenize
    4. Lemmatize words
    5. Remove stopwords (negations are kept)
    6. Return cleaned text
    """

    # Make sure input is a string
    if not isinstance(text, str):
        return ""

    # 1. Unicode normalization
    text = unicodedata.normalize("NFC", text)

    # Remove invisible joiner characters
    text = text.replace("\u200c", "").replace("\u200d", "")

    # 2. Remove danda marks, punctuation and symbols.
    # Keep Hindi characters, English characters, numbers and spaces
    text = text.replace("\u0964", " ").replace("\u0965", " ")
    text = re.sub(r"[^\u0900-\u097F a-zA-Z0-9]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    # 3. Tokenization (Hindi words are separated by spaces)
    tokens = text.split()

    if not tokens:
        return ""

    # 4. Lemmatization (done BEFORE stopword removal because the
    # lemmatizer needs the full sentence context)
    lemmas = lemmatize_hindi(tokens)

    # 5. Remove stopwords (check both the original word and its lemma)
    cleaned_tokens = []
    for original, lemma in zip(tokens, lemmas):
        if original in HINDI_STOPWORDS or lemma in HINDI_STOPWORDS:
            continue
        cleaned_tokens.append(lemma)

    # 6. Convert tokens back to text
    return " ".join(cleaned_tokens)


# Quick test: python <this_file_name>.py
if __name__ == "__main__":
    samples = [
        "एक अजनबी मुझे मेरी निजी तस्वीरें वायरल करने की धमकी देकर पैसे मांग रहा है।",
        "उसने मुझे पैसे नहीं दिए और मुझे सोमवार सुबह 10 बजे अंधेरी स्टेशन पर परेशान किया।",
    ]

    for sample in samples:
        print("Original :", sample)
        print("Light    :", preprocess_hindi(sample))
        print("Full     :", preprocess_hindi_full(sample))
        print()