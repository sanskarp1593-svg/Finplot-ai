"""Hindi / Hinglish language support for the agent workflow."""

from __future__ import annotations

import re

# ── Hindi keyword → intent mapping ───────────────────────────────────────────

HINDI_KEYWORDS: dict[str, list[str]] = {
    "metric": [
        "kitna", "kamai", "kharcha", "munafa", "nuksan",
        "aay", "amdani", "total", "is mahine", "pichle mahine",
        "bikri", "bechna", "revenue", "profit",
        "कितना", "कमाई", "खर्चा", "मुनाफा", "नुकसान",
        "आय", "आमदनी", "बिक्री",
    ],
    "budget": [
        "bajet", "budget", "limit", "zyada kharcha",
        "बजट", "ज़्यादा खर्चा", "सीमा",
    ],
    "compliance": [
        "gst", "tax", "tds", "kar", "return",
        "जीएसटी", "कर", "टैक्स", "टीडीएस",
    ],
    "item_price": [
        "daam", "bhav", "rate", "keemat", "kimat",
        "khareedna", "kharidna", "pyaaz", "pyaaj", "chawal",
        "दाम", "भाव", "कीमत", "खरीदना", "प्याज़", "चावल",
    ],
}

# ── Common Hindi item names → English ────────────────────────────────────────

HINDI_ITEM_MAP: dict[str, str] = {
    "pyaaz": "onion", "pyaaj": "onion", "प्याज़": "onion", "प्याज": "onion",
    "tamatar": "tomato", "टमाटर": "tomato",
    "aalu": "potato", "aloo": "potato", "आलू": "potato",
    "chawal": "rice", "चावल": "rice",
    "dal": "dal", "daal": "dal", "दाल": "dal",
    "aata": "flour", "atta": "flour", "आटा": "flour",
    "cheeni": "sugar", "चीनी": "sugar",
    "tel": "oil", "तेल": "oil",
    "namak": "salt", "नमक": "salt",
    "mirch": "chilli", "मिर्च": "chilli",
    "haldi": "turmeric", "हल्दी": "turmeric",
    "doodh": "milk", "दूध": "milk",
    "ghee": "ghee", "घी": "ghee",
    "sabun": "soap", "साबुन": "soap",
}



def detect_hindi_intent(question: str) -> str | None:
    """Check if the question matches any Hindi keyword patterns."""
    q = question.lower()
    scores: dict[str, int] = {}
    for intent, keywords in HINDI_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in q)
        if score > 0:
            scores[intent] = score
    if scores:
        return max(scores, key=scores.get)  # type: ignore
    return None


def translate_item_name(name: str) -> str:
    """Map a Hindi item name to English if known."""
    lower = name.lower().strip()
    return HINDI_ITEM_MAP.get(lower, name)


# ── Response templates ───────────────────────────────────────────────────────

HINDI_TEMPLATES = {
    "metric_summary": (
        "{month} में:\n"
        "• आय (Revenue): ₹{revenue:,.0f}\n"
        "• खर्चा (Expenses): ₹{expenses:,.0f}\n"
        "• मुनाफ़ा (Profit): ₹{profit:,.0f}\n"
        "• मार्जिन: {margin:.1f}%"
    ),
    "budget_ok": "✅ {category} का खर्चा ₹{spent:,.0f} है, बजट ₹{limit:,.0f} – सीमा के अंदर है।",
    "budget_over": "⚠️ {category} में बजट से ₹{over:,.0f} ज़्यादा खर्चा हो गया! (खर्चा ₹{spent:,.0f}, बजट ₹{limit:,.0f})",
    "no_data": "इस अवधि के लिए कोई डेटा नहीं मिला।",
    "ca_review": "\n\n⚖️ यह जानकारी केवल संदर्भ के लिए है। कृपया अपने चार्टर्ड अकाउंटेंट से पुष्टि करें।",
    "item_last_price": "📦 {item} का आख़िरी भाव ₹{price:,.0f} ({date} को {vendor} से) था।",
    "item_no_record": "📦 {item} का कोई रिकॉर्ड नहीं मिला। (केवल पुष्टि किए गए बिलों के आइटम दिखते हैं।)",
    "general_fallback": "माफ़ कीजिए, मैं इस सवाल का जवाब नहीं दे पा रहा। कृपया अपना सवाल दोबारा लिखें।",
    "compliance_source": "📖 स्रोत: {title}",
}

ENGLISH_TEMPLATES = {
    "metric_summary": (
        "For {month}:\n"
        "• Revenue: ₹{revenue:,.0f}\n"
        "• Expenses: ₹{expenses:,.0f}\n"
        "• Profit: ₹{profit:,.0f}\n"
        "• Margin: {margin:.1f}%"
    ),
    "budget_ok": "✅ {category} spending is ₹{spent:,.0f} against a budget of ₹{limit:,.0f} – within limits.",
    "budget_over": "⚠️ {category} is over budget by ₹{over:,.0f}! (Spent ₹{spent:,.0f}, Budget ₹{limit:,.0f})",
    "no_data": "No data found for this period.",
    "ca_review": "\n\n⚖️ This information is for reference only. Please consult your Chartered Accountant for confirmation.",
    "item_last_price": "📦 Last price for {item}: ₹{price:,.0f} (on {date} from {vendor}).",
    "item_no_record": "📦 No record found for {item}. (Only items from confirmed invoices are tracked.)",
    "general_fallback": "I'm not sure how to answer that. Could you rephrase your question?",
    "compliance_source": "📖 Source: {title}",
}


def get_templates(language: str) -> dict[str, str]:
    """Return the template dict for the given language."""
    return HINDI_TEMPLATES if language == "hi" else ENGLISH_TEMPLATES
