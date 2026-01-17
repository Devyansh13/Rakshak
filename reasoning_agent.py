def reasoning_agent(matches, band):
    explanation_lines = []
    confidence = ""

    # Base explanation
    if not matches:
        explanation_lines.append(
            "The beneficiary name was screened against official UN and Indian MHA sanctions lists using exact and fuzzy matching."
        )
        explanation_lines.append(
            "No significant name similarity or alias overlap was detected with any sanctioned individual or organization."
        )
        confidence = "High confidence (low false-positive risk)."

    else:
        explanation_lines.append(
            "The beneficiary name was screened against official UN and Indian MHA sanctions lists."
        )

        for m in matches:
            explanation_lines.append(
                f"A potential similarity was detected with '{m['entity']}' "
                f"from the {m['source']} list (matching confidence: {round(m['score'],1)}%)."
            )

        if band == "AMBER":
            confidence = "Medium confidence (possible false positive due to partial name match)."
        elif band == "RED":
            confidence = "High confidence (strong similarity with sanctioned entity)."

    # Decision logic explanation
    if band == "GREEN":
        decision_rationale = (
            "Based on the absence of meaningful matches, the system classified this payment as LOW RISK."
        )
        recommended_actions = [
            "Proceed with payment.",
            "Store screening proof for audit purposes."
        ]

    elif band == "AMBER":
        decision_rationale = (
            "Due to partial name similarity and limited contextual information, the payment was classified as MEDIUM RISK."
        )
        recommended_actions = [
            "Request beneficiary verification documents (PAN/GST/Address).",
            "Re-screen after verification."
        ]

    else:  # RED
        decision_rationale = (
            "Due to strong similarity with sanctioned entities, the payment was classified as HIGH RISK."
        )
        recommended_actions = [
            "Hold payment immediately.",
            "Escalate case to compliance or legal review."
        ]

    # Counterfactual explanation (THIS IS AI FLEX)
    counterfactual = (
        "This decision could change if additional verified information "
        "demonstrates that the beneficiary is distinct from the sanctioned entity."
    )

    return {
        "risk_band": band,
        "confidence_assessment": confidence,
        "reasoning_summary": explanation_lines,
        "decision_rationale": decision_rationale,
        "recommended_actions": recommended_actions,
        "counterfactual_analysis": counterfactual
    }
