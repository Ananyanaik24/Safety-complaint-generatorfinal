
def get_safety_advice(
    category: str,
    language: str = "Hindi",
    complaint: str = ""
) -> str:
    """
    Return detailed, category-specific safety advice.

    The advice is based on the predicted complaint category.
    The original complaint is accepted for future contextual
    improvements without inventing incident details.
    """

    advice_english = {
        "Blackmail": (
            "SAFETY GUIDANCE — BLACKMAIL\n\n"
            "1. Do not make payments or agree to demands under pressure. "
            "Payment does not guarantee that the blackmail will stop.\n\n"
            "2. Preserve relevant evidence, including messages, emails, "
            "phone numbers, transaction details, links and screenshots. "
            "Avoid editing or deleting the original records.\n\n"
            "3. Avoid confronting the suspected person alone. If you are "
            "being threatened with physical harm, move to a safe place "
            "and seek immediate assistance.\n\n"
            "4. Report online financial fraud or cyber blackmail through "
            "the official Indian cybercrime portal at cybercrime.gov.in. "
            "For an immediate emergency in India, call 112."
        ),

        "Eve Teasing": (
            "SAFETY GUIDANCE — PUBLIC HARASSMENT\n\n"
            "1. If you feel unsafe, move towards a populated, well-lit "
            "place, a staffed shop or a security desk. Do not feel "
            "obligated to confront the person.\n\n"
            "2. Seek help from a trusted person, nearby security staff "
            "or bystanders if it is safe to do so.\n\n"
            "3. If the behaviour continues, record the date, time, "
            "location and a description of what happened. Keep any "
            "relevant messages or other evidence safely.\n\n"
            "4. Report the incident to the local police or the relevant "
            "authority. If you face immediate danger in India, call 112."
        ),

        "Harassment": (
            "SAFETY GUIDANCE — HARASSMENT\n\n"
            "1. Keep a record of each incident, including dates, times, "
            "locations, messages and the people involved, where known.\n\n"
            "2. Save relevant emails, screenshots and other evidence "
            "securely. Avoid responding aggressively if doing so could "
            "increase the risk to your safety.\n\n"
            "3. Consider reporting the matter to the appropriate "
            "authority. For workplace or educational harassment, you "
            "may also contact the designated complaints committee "
            "or responsible administrator, where applicable.\n\n"
            "4. Inform a trusted person if you need support. If there "
            "is an immediate threat of harm in India, call 112."
        ),

        "Domestic Violence": (
            "SAFETY GUIDANCE — DOMESTIC VIOLENCE\n\n"
            "1. Your immediate safety comes first. If violence is "
            "occurring or you believe harm is imminent, move to a "
            "safer place if you can do so without increasing danger.\n\n"
            "2. Contact a trusted person who can help you access "
            "safety and support. Avoid confronting the person if "
            "doing so could put you at greater risk.\n\n"
            "3. If safe to do so, keep important documents, essential "
            "medication and emergency contact details accessible. "
            "Only preserve evidence when doing so will not endanger you.\n\n"
            "4. In India, call 112 for an immediate emergency. Women "
            "may also seek assistance through the 181 women helpline "
            "where available."
        ),

        "Public Safety": (
            "SAFETY GUIDANCE — PUBLIC SAFETY\n\n"
            "1. Move away from the reported hazard if it is safe to "
            "do so. Avoid entering restricted, damaged or dangerous "
            "areas to investigate the problem yourself.\n\n"
            "2. Warn nearby people only when you can do so safely. "
            "Do not touch suspicious objects, exposed electrical "
            "wires or other potentially hazardous materials.\n\n"
            "3. Note the exact location, time and nature of the "
            "hazard. Share photographs or other evidence only if "
            "they can be collected without putting anyone at risk.\n\n"
            "4. Notify the appropriate local authority or emergency "
            "service. For an immediate emergency in India, call 112."
        ),

        "Threat": (
            "SAFETY GUIDANCE — THREATS\n\n"
            "1. Take a threat seriously if you believe harm may be "
            "imminent. Move to a safe location and contact trusted "
            "people who can assist you.\n\n"
            "2. Avoid meeting or confronting the person alone, "
            "particularly if weapons, violence or direct threats "
            "have been mentioned.\n\n"
            "3. Preserve relevant messages, call logs, emails and "
            "other evidence. Record when and where the incident "
            "occurred, if safe to do so.\n\n"
            "4. Report the threat to the local police. If you face "
            "immediate danger in India, call 112."
        ),

        "Stalking": (
            "SAFETY GUIDANCE — STALKING\n\n"
            "1. If you believe you are being followed, move towards "
            "a populated, secure place instead of going somewhere "
            "isolated or directly home if that could expose your "
            "address to the person.\n\n"
            "2. Contact a trusted person and tell them what is "
            "happening. Do not confront the suspected stalker alone.\n\n"
            "3. Keep a dated record of repeated incidents, unwanted "
            "communications and other relevant evidence, provided "
            "it is safe to do so.\n\n"
            "4. Report the matter to the local police. If you are "
            "in immediate danger in India, call 112."
        ),

        "Cyber Harassment": (
            "SAFETY GUIDANCE — CYBER HARASSMENT\n\n"
            "1. Avoid sharing further personal information with the "
            "person or engaging in exchanges that could increase "
            "the harassment.\n\n"
            "2. Save screenshots, profile details, URLs, timestamps "
            "and relevant messages before blocking or reporting "
            "the account, when it is safe to do so.\n\n"
            "3. Review your account privacy settings and strengthen "
            "your passwords. Enable two-factor authentication "
            "where available, especially if account access may "
            "have been compromised.\n\n"
            "4. Report the account to the relevant platform. In India, "
            "you can submit a cybercrime complaint at cybercrime.gov.in. "
            "For an immediate physical emergency, call 112."
        ),

        "Theft": (
            "SAFETY GUIDANCE — THEFT\n\n"
            "1. Move to a safe location if the incident is ongoing. "
            "Do not chase or confront a suspected offender if doing "
            "so could put you at risk.\n\n"
            "2. Report the incident to the local police and provide "
            "the known time, location, description of missing "
            "property and any relevant identifying details.\n\n"
            "3. Preserve receipts, serial numbers, photographs, "
            "tracking information and other proof of ownership "
            "where available.\n\n"
            "4. If a phone, bank card or account has been stolen, "
            "contact the relevant service provider or financial "
            "institution promptly to secure it."
        ),

        "Other": (
            "SAFETY GUIDANCE — GENERAL PRECAUTIONS\n\n"
            "1. If you believe there is an immediate risk to your "
            "safety, move to a safer place if possible and contact "
            "the appropriate emergency service.\n\n"
            "2. Keep a clear record of what happened, including "
            "the date, time, location and people involved, where known.\n\n"
            "3. Preserve relevant messages, documents, photographs "
            "and other evidence only when it is safe to do so.\n\n"
            "4. Report the incident to the authority responsible "
            "for the issue. For an immediate emergency in India, "
            "call 112."
        )
    }

    advice_hindi = {
        "Blackmail": (
            "सुरक्षा सलाह — ब्लैकमेल\n\n"
            "1. दबाव में आकर पैसे न दें और न ही किसी अनुचित मांग "
            "को स्वीकार करें। पैसे देने से ब्लैकमेल रुकने की गारंटी "
            "नहीं होती।\n\n"
            "2. संदेश, ईमेल, फोन नंबर, भुगतान का विवरण और स्क्रीनशॉट "
            "जैसे सबूत सुरक्षित रखें। मूल रिकॉर्ड को मिटाने या बदलने "
            "से बचें।\n\n"
            "3. संबंधित व्यक्ति का अकेले सामना करने से बचें। यदि "
            "शारीरिक नुकसान का खतरा हो, तो सुरक्षित स्थान पर जाएं "
            "और तुरंत सहायता लें।\n\n"
            "4. ऑनलाइन ब्लैकमेल या साइबर अपराध की शिकायत "
            "cybercrime.gov.in पर दर्ज करें। भारत में तत्काल "
            "आपातकालीन सहायता के लिए 112 पर कॉल करें।"
        ),

        "Eve Teasing": (
            "सुरक्षा सलाह — सार्वजनिक स्थान पर छेड़छाड़\n\n"
            "1. असुरक्षित महसूस होने पर भीड़भाड़ वाले, रोशनी वाले "
            "स्थान, दुकान या सुरक्षा डेस्क की ओर जाएं। संबंधित "
            "व्यक्ति का सामना करना आवश्यक नहीं है।\n\n"
            "2. सुरक्षित होने पर किसी विश्वसनीय व्यक्ति, सुरक्षा "
            "कर्मी या आसपास मौजूद लोगों से सहायता लें।\n\n"
            "3. घटना की तारीख, समय, स्थान और उससे संबंधित विवरण "
            "लिखकर रखें। संदेश या अन्य सबूत सुरक्षित रखें।\n\n"
            "4. स्थानीय पुलिस या संबंधित प्राधिकरण को सूचित करें। "
            "भारत में तत्काल खतरे की स्थिति में 112 पर कॉल करें।"
        ),

        "Harassment": (
            "सुरक्षा सलाह — उत्पीड़न\n\n"
            "1. प्रत्येक घटना की तारीख, समय, स्थान और संबंधित "
            "व्यक्तियों का विवरण, जहां ज्ञात हो, सुरक्षित रखें।\n\n"
            "2. संबंधित संदेश, ईमेल और स्क्रीनशॉट सुरक्षित रखें। "
            "यदि जवाब देने से खतरा बढ़ सकता है, तो आक्रामक "
            "प्रतिक्रिया देने से बचें।\n\n"
            "3. उचित प्राधिकरण को शिकायत दें। कार्यस्थल या "
            "शैक्षणिक संस्थान से संबंधित मामले में उपलब्ध "
            "शिकायत समिति या जिम्मेदार अधिकारी से भी संपर्क करें।\n\n"
            "4. जरूरत पड़ने पर किसी विश्वसनीय व्यक्ति से सहायता "
            "लें। भारत में तत्काल खतरे की स्थिति में 112 पर "
            "कॉल करें।"
        ),

        "Domestic Violence": (
            "सुरक्षा सलाह — घरेलू हिंसा\n\n"
            "1. अपनी सुरक्षा को प्राथमिकता दें। हिंसा हो रही हो "
            "या नुकसान का तत्काल खतरा हो, तो यदि सुरक्षित हो "
            "तो किसी सुरक्षित स्थान पर जाएं।\n\n"
            "2. किसी विश्वसनीय व्यक्ति से सहायता लें। यदि "
            "सामना करने से खतरा बढ़ सकता है, तो संबंधित व्यक्ति "
            "से अकेले सामना करने से बचें।\n\n"
            "3. सुरक्षित होने पर जरूरी दस्तावेज, आवश्यक दवाएं "
            "और आपातकालीन संपर्क विवरण उपलब्ध रखें। सबूत "
            "केवल तभी सुरक्षित करें जब इससे आपका खतरा न बढ़े।\n\n"
            "4. भारत में तत्काल आपातकालीन सहायता के लिए 112 "
            "पर कॉल करें। महिलाएं उपलब्ध होने पर 181 महिला "
            "हेल्पलाइन से भी सहायता मांग सकती हैं।"
        ),

        "Public Safety": (
            "सुरक्षा सलाह — सार्वजनिक सुरक्षा\n\n"
            "1. यदि सुरक्षित हो, तो बताए गए खतरे से दूर जाएं। "
            "जांच करने के लिए क्षतिग्रस्त या खतरनाक क्षेत्र में "
            "प्रवेश न करें।\n\n"
            "2. दूसरों को सावधान तभी करें जब ऐसा करना सुरक्षित "
            "हो। संदिग्ध वस्तुओं, खुले बिजली के तारों या "
            "खतरनाक पदार्थों को न छुएं।\n\n"
            "3. खतरे का स्थान, समय और प्रकार नोट करें। "
            "फोटो या अन्य सबूत केवल तभी जुटाएं जब इससे "
            "किसी की सुरक्षा को जोखिम न हो।\n\n"
            "4. संबंधित स्थानीय प्राधिकरण को सूचित करें। "
            "भारत में तत्काल आपातकालीन स्थिति में 112 "
            "पर कॉल करें।"
        ),

        "Threat": (
            "सुरक्षा सलाह — धमकी\n\n"
            "1. यदि नुकसान होने का तत्काल खतरा हो, तो धमकी "
            "को गंभीरता से लें, सुरक्षित स्थान पर जाएं और "
            "विश्वसनीय व्यक्ति से सहायता लें।\n\n"
            "2. संबंधित व्यक्ति से अकेले मिलने या उसका सामना "
            "करने से बचें, विशेषकर जब हिंसा या हथियारों की "
            "धमकी दी गई हो।\n\n"
            "3. संदेश, कॉल रिकॉर्ड, ईमेल और अन्य संबंधित "
            "सबूत सुरक्षित रखें। सुरक्षित होने पर घटना का "
            "समय और स्थान भी लिखें।\n\n"
            "4. स्थानीय पुलिस को शिकायत दें। भारत में तत्काल "
            "खतरे की स्थिति में 112 पर कॉल करें।"
        ),

        "Stalking": (
            "सुरक्षा सलाह — पीछा किया जाना\n\n"
            "1. यदि कोई आपका पीछा कर रहा है, तो सुरक्षित "
            "और भीड़भाड़ वाले स्थान की ओर जाएं। ऐसी जगह "
            "अकेले जाने से बचें जहां आप आसानी से असुरक्षित "
            "हो सकते हैं।\n\n"
            "2. किसी विश्वसनीय व्यक्ति को स्थिति बताएं। "
            "संदिग्ध व्यक्ति का अकेले सामना न करें।\n\n"
            "3. बार-बार होने वाली घटनाओं, अनचाहे संदेशों "
            "और संबंधित सबूतों का तारीख सहित रिकॉर्ड रखें, "
            "यदि ऐसा करना सुरक्षित हो।\n\n"
            "4. स्थानीय पुलिस को शिकायत दें। भारत में तत्काल "
            "खतरे की स्थिति में 112 पर कॉल करें।"
        ),

        "Cyber Harassment": (
            "सुरक्षा सलाह — साइबर उत्पीड़न\n\n"
            "1. संबंधित व्यक्ति के साथ बातचीत बढ़ाने या "
            "अतिरिक्त व्यक्तिगत जानकारी साझा करने से बचें।\n\n"
            "2. सुरक्षित होने पर स्क्रीनशॉट, प्रोफाइल विवरण, "
            "लिंक, समय और संदेशों का रिकॉर्ड रखें। इसके बाद "
            "संबंधित अकाउंट को ब्लॉक या रिपोर्ट कर सकते हैं।\n\n"
            "3. अपनी गोपनीयता सेटिंग जांचें, मजबूत पासवर्ड "
            "रखें और उपलब्ध होने पर दो-स्तरीय प्रमाणीकरण "
            "चालू करें।\n\n"
            "4. संबंधित प्लेटफॉर्म पर शिकायत करें। भारत में "
            "cybercrime.gov.in पर साइबर अपराध की शिकायत "
            "दर्ज कर सकते हैं। तत्काल शारीरिक खतरे में "
            "112 पर कॉल करें।"
        ),

        "Theft": (
            "सुरक्षा सलाह — चोरी\n\n"
            "1. यदि घटना जारी है, तो सुरक्षित स्थान पर जाएं। "
            "खुद को खतरे में डालकर संदिग्ध व्यक्ति का पीछा "
            "या सामना न करें।\n\n"
            "2. स्थानीय पुलिस को घटना की जानकारी दें। "
            "समय, स्थान, चोरी हुई वस्तु और उपलब्ध पहचान "
            "संबंधी विवरण साझा करें।\n\n"
            "3. रसीद, सीरियल नंबर, तस्वीरें और स्वामित्व "
            "से संबंधित अन्य सबूत उपलब्ध होने पर सुरक्षित रखें।\n\n"
            "4. यदि फोन, बैंक कार्ड या अकाउंट चोरी हुआ है, "
            "तो संबंधित सेवा प्रदाता या बैंक से जल्द संपर्क "
            "करके उसे सुरक्षित करें।"
        ),

        "Other": (
            "सुरक्षा सलाह — सामान्य सावधानियां\n\n"
            "1. यदि तत्काल खतरा महसूस हो, तो संभव होने पर "
            "सुरक्षित स्थान पर जाएं और उचित आपातकालीन "
            "सेवा से संपर्क करें।\n\n"
            "2. घटना की तारीख, समय, स्थान और संबंधित "
            "व्यक्तियों का विवरण, जहां ज्ञात हो, लिखकर रखें।\n\n"
            "3. संदेश, दस्तावेज, तस्वीरें और अन्य सबूत "
            "तभी सुरक्षित करें जब ऐसा करना सुरक्षित हो।\n\n"
            "4. घटना की प्रकृति के अनुसार संबंधित प्राधिकरण "
            "को शिकायत दें। भारत में तत्काल आपातकालीन "
            "स्थिति में 112 पर कॉल करें।"
        )
    }

    category = (category or "Other").strip()

    # Match category names without case sensitivity.
    advice_map = (
        advice_english if (language or "").strip().lower() == "english"
        else advice_hindi
    )

    normalized_categories = {
        key.lower(): key for key in advice_map
    }

    matched_category = normalized_categories.get(
        category.lower(), "Other"
    )

    return advice_map[matched_category]
