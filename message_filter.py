import re

# TODO: refine words/phrases to filter, improve combinations
SCAM_CATEGORIES = {
    "giveaway": [
        r"\bgiving (away|out)\b",
        r"\bfor free\b",
        r"\bfree (macbook|iphone|ps5|tickets?)\b",
    ],
    "selling": [
        r"\bselling\b",
        r"\bi'?m selling\b",
        # TODO: add filters for "for sale", "sell" (e.g. looking to sell)
    ],
    "concert": [
        r"\b(concert|festival|tour|tickets?)\b",
    ],
    "job": [
        r"\b(assistant|remote|from home|weekly salary|\$\d+)\b",
    ],
}

def is_scam(text: str) -> bool:
    text = text.lower()
    matches = {cat: False for cat in SCAM_CATEGORIES}

    for category, patterns in SCAM_CATEGORIES.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                matches[category] = True
                break   # stop once one pattern in the category matches

    if matches["selling"] and matches["concert"]:   # selling concert tickets
        return True
    # Giveaways and job adverts always banned
    if matches["giveaway"]:
        return True 
    if matches["job"]:
        return True

    return False
