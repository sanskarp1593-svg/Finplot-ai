from app.agents.hindi import detect_hindi_intent, translate_item_name

def test_hindi_intent_detection():
    """Test Hindi / Hinglish question intent classification."""
    # Metric intent
    assert detect_hindi_intent("pichle mahine kitna kharcha hua?") == "metric"
    assert detect_hindi_intent("kul kamai kitni hui?") == "metric"

    # Budget intent
    assert detect_hindi_intent("kya humara budget paar ho gaya?") == "budget"

    # Compliance intent
    assert detect_hindi_intent("GST ke kya niyam hain?") == "compliance"
    assert detect_hindi_intent("TDS katna zaroori hai kya?") == "compliance"

    # Item price intent
    assert detect_hindi_intent("pyaaz ka bhav kya tha?") == "item_price"
    assert detect_hindi_intent("chawal ka daam kya tha?") == "item_price"


def test_hindi_item_translation():
    """Test translating common Hindi item terms to English."""
    assert translate_item_name("pyaaz") == "onion"
    assert translate_item_name("tamatar") == "tomato"
    assert translate_item_name("chawal") == "rice"
    assert translate_item_name("tel") == "oil"
