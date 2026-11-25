def analyze_sentiment(message):

    text = message.lower()

    positive_words = [
        "good", "great", "interested",
        "excellent", "love", "amazing"
    ]

    negative_words = [
        "bad", "expensive", "angry",
        "disappointed", "poor", "problem"
    ]

    positive = sum(word in text for word in positive_words)
    negative = sum(word in text for word in negative_words)

    if positive > negative:
        return "Positive"

    elif negative > positive:
        return "Negative"

    return "Neutral"