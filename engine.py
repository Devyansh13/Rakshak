from rapidfuzz import fuzz
from sanctions_data import SANCTIONS

def screening_agent(beneficiary_name, country):
    matches = []

    for entity in SANCTIONS:
        score_name = fuzz.partial_ratio(beneficiary_name.lower(), entity["name"].lower())
        score_alias = max(
            [fuzz.partial_ratio(beneficiary_name.lower(), a.lower()) for a in entity["aliases"]],
            default=0
        )

        score = max(score_name, score_alias)

        if country.lower() != entity["country"].lower() and entity["country"] != "Global":
            score -= 10

        if score > 60:
            matches.append({
                "entity": entity["name"],
                "source": entity["source"],
                "score": score
            })

    return matches


def risk_band_agent(matches):
    if not matches:
        return "GREEN", 20

    top_score = max(m["score"] for m in matches)

    if top_score >= 80:
        return "RED", top_score
    elif top_score >= 60:
        return "AMBER", top_score
    else:
        return "GREEN", top_score
