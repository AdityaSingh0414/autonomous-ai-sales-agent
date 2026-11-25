
# Customer lead qualify karne ka function.
def qualify_lead(message):

    # Customer message ko lowercase mein convert karna.
    text = message.lower()

    # Initial lead score aur details.
    score = 0
    details = []

    # Purchase intent check karna.
    if any(word in text for word in ["buy", "purchase", "buying"]):
        score += 30
        details.append("Purchase intent detected")

    # Budget ya pricing interest check karna.
    if any(word in text for word in ["price", "pricing", "cost", "budget"]):
        score += 20
        details.append("Budget interest detected")

    # Meeting ya demo interest check karna.
    if any(word in text for word in ["meeting", "demo", "appointment"]):
        score += 30
        details.append("Meeting interest detected")

    # Business requirement check karna.
    if any(word in text for word in ["business", "company", "enterprise"]):
        score += 20
        details.append("Business requirement detected")

    # Maximum score 100 rakhna.
    score = min(score, 100)

    # Score ke according lead category assign karna.
    if score >= 70:
        category = "Hot"
    elif score >= 40:
        category = "Warm"
    else:
        category = "Cold"

    # Lead qualification result return karna.
    return {
        "score": score,
        "category": category,
        "details": details
    }
