
from datetime import datetime
import re

from app.translation.translator import (
    translate_hindi_to_english,
    translate_english_to_hindi,
)


def is_devanagari(text: str) -> bool:
    """Check whether a string contains Devanagari (Hindi) characters."""
    if not text:
        return False
    return bool(re.search(r"[\u0900-\u097F]", str(text)))


def safe_translate_hindi_to_english(text: str) -> str:
    """Translate Hindi text; retain original text if translation fails."""
    try:
        translated = translate_hindi_to_english(text)
        if translated and not is_devanagari(translated):
            return translated.strip()
    except Exception as exc:
        print(f"[WARNING] Hindi-to-English translation failed: {exc}")

    return text


def safe_translate_english_to_hindi(text: str) -> str:
    """Translate English text; retain original text if translation fails."""
    try:
        translated = translate_english_to_hindi(text)
        if translated:
            return translated.strip()
    except Exception as exc:
        print(f"[WARNING] English-to-Hindi translation failed: {exc}")

    return text


def format_date(date_str: str) -> str:
    if not date_str:
        return ""

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d %B %Y").lstrip("0")
    except ValueError:
        return date_str


def format_time(time_str: str) -> str:
    if not time_str:
        return ""

    try:
        time_obj = datetime.strptime(time_str, "%H:%M")
        return time_obj.strftime("%I:%M %p").lstrip("0")
    except ValueError:
        return time_str


def generate_formal_complaint(
    original_complaint: str,
    category: str,
    entities: dict,
    language: str = "English",
    date: str = "",
    time: str = "",
    location: str = "",
    translated_complaint: str = "",
) -> dict:
    """
    Generate detailed formal complaint drafts in English and Hindi.

    Only supplied or extracted information is used. The function does
    not invent facts about suspects, injuries or other incident details.
    """

    entities = entities or {}

    persons = entities.get("persons", []) or []
    locations = entities.get("locations", []) or []
    dates = entities.get("dates", []) or []
    times = entities.get("times", []) or []

    final_date = date or (dates[0] if dates else "")
    final_time = time or (times[0] if times else "")
    final_location = location or (locations[0] if locations else "")
    person = persons[0] if persons else ""

    readable_date = format_date(final_date)
    readable_time = format_time(final_time)

    # Get the English incident description.
    if translated_complaint and not is_devanagari(translated_complaint):
        english_details = translated_complaint.strip()
    elif is_devanagari(original_complaint):
        english_details = safe_translate_hindi_to_english(
            original_complaint
        )
    else:
        english_details = original_complaint.strip()

    # Get the Hindi incident description.
    if is_devanagari(original_complaint):
        hindi_details = original_complaint.strip()
    else:
        hindi_details = safe_translate_english_to_hindi(
            original_complaint
        )

    hindi_categories = {
        "Blackmail": "ब्लैकमेल",
        "Eve Teasing": "छेड़छाड़",
        "Harassment": "उत्पीड़न",
        "Domestic Violence": "घरेलू हिंसा",
        "Public Safety": "सार्वजनिक सुरक्षा",
        "Threat": "धमकी",
        "Stalking": "पीछा किए जाने",
        "Cyber Harassment": "साइबर उत्पीड़न",
        "Theft": "चोरी",
        "Uncategorized": "अज्ञात/अन्य",
        "Other": "अन्य",
    }

    category = (category or "Other").strip()

    hindi_category = hindi_categories.get(category, "अन्य")

    display_category_en = (
        "an unspecified incident"
        if category.lower() in {"uncategorized", "other"}
        else category.lower()
    )

    # Translate the location based on its actual script.
    english_location = final_location
    hindi_location = final_location

    if final_location:
        if is_devanagari(final_location):
            english_location = safe_translate_hindi_to_english(
                final_location
            )
            hindi_location = final_location
        else:
            hindi_location = safe_translate_english_to_hindi(
                final_location
            )

    person_en = (
        person if person and not is_devanagari(person) else ""
    )

    person_hi = (
        person if person and is_devanagari(person) else ""
    )

    # --------------------------------------------------
    # Formal English complaint
    # --------------------------------------------------

    english_parts = [
        f"Subject: Formal Complaint Regarding "
        f"{display_category_en.title()}",
        "",
        "Respected Sir/Madam,",
        "",
        (
            "I am writing to formally report an incident involving "
            f"{display_category_en}. "
        ),
    ]

    if readable_date:
        english_parts.append(
            f"The reported date of the incident is {readable_date}. "
        )

    if readable_time:
        english_parts.append(
            f"The reported time is {readable_time}. "
        )

    if english_location:
        english_parts.append(
            f"The reported location is {english_location}. "
        )

    if person_en:
        english_parts.append(
            f"The complaint identifies {person_en} as a person "
            "involved in the reported incident. "
        )

    english_parts.extend([
        "",
        "Incident Description:",
        (
            english_details.strip()
            or "No incident description was provided."
        ),
        "",
        (
            "I request that the concerned authority review the "
            "information provided, investigate the reported incident "
            "as appropriate, and take suitable action in accordance "
            "with applicable rules and procedures."
        ),
        "",
        (
            "I am willing to provide additional information or "
            "supporting evidence if required."
        ),
        "",
        "Thank you for your attention to this matter.",
        "",
        "Yours faithfully,",
        "Complainant",
    ])

    english_complaint = "\n".join(english_parts)

    # --------------------------------------------------
    # Format date and time for Hindi
    # --------------------------------------------------

    hindi_date = readable_date

    hindi_months = {
        "January": "जनवरी",
        "February": "फरवरी",
        "March": "मार्च",
        "April": "अप्रैल",
        "May": "मई",
        "June": "जून",
        "July": "जुलाई",
        "August": "अगस्त",
        "September": "सितंबर",
        "October": "अक्टूबर",
        "November": "नवंबर",
        "December": "दिसंबर",
    }

    for english_month, hindi_month in hindi_months.items():
        hindi_date = hindi_date.replace(
            english_month,
            hindi_month
        )

    hindi_time = (
        readable_time
        .replace("AM", "पूर्वाह्न")
        .replace("PM", "अपराह्न")
    )

    # --------------------------------------------------
    # Formal Hindi complaint
    # --------------------------------------------------

    hindi_parts = [
        f"विषय: {hindi_category} के संबंध में औपचारिक शिकायत",
        "",
        "महोदय/महोदया,",
        "",
        (
            f"मैं {hindi_category} की रिपोर्ट की गई घटना के संबंध में "
            "औपचारिक शिकायत दर्ज करना चाहता/चाहती हूँ। "
        ),
    ]

    if hindi_date:
        hindi_parts.append(
            f"घटना की बताई गई तारीख {hindi_date} है। "
        )

    if hindi_time:
        hindi_parts.append(
            f"घटना का बताया गया समय {hindi_time} है। "
        )

    if hindi_location:
        hindi_parts.append(
            f"घटना का बताया गया स्थान {hindi_location} है। "
        )

    if person_hi:
        hindi_parts.append(
            f"शिकायत में {person_hi} का उल्लेख घटना से संबंधित "
            "व्यक्ति के रूप में है। "
        )

    hindi_parts.extend([
        "",
        "घटना का विवरण:",
        (
            hindi_details.strip()
            or "घटना का विवरण उपलब्ध नहीं कराया गया।"
        ),
        "",
        (
            "अतः मेरा अनुरोध है कि संबंधित प्राधिकरण उपलब्ध जानकारी "
            "की समीक्षा करे, घटना की उचित जांच करे और लागू नियमों "
            "के अनुसार आवश्यक कार्रवाई करे।"
        ),
        "",
        (
            "आवश्यकता होने पर मैं अतिरिक्त जानकारी या उपलब्ध "
            "संबंधित सबूत प्रदान करने के लिए तैयार हूँ।"
        ),
        "",
        "इस मामले पर ध्यान देने के लिए धन्यवाद।",
        "",
        "सादर,",
        "शिकायतकर्ता",
    ])

    hindi_complaint = "\n".join(hindi_parts)

    return {
        "formal_english": english_complaint.strip(),
        "formal_hindi": hindi_complaint.strip(),
    }
