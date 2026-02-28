def validate_report(report):
    """
    Guardrail system to validate the AI-generated report.
    """
    required_fields = ["Findings", "Impression", "Recommendations"]

    # 1. Check for presence of required fields
    for field in required_fields:
        if field not in report or not report[field]:
            return False, f"Missing required field: {field}"

    # 2. Filter terms that suggest excessive lack of certainty or detectable "hallucinations"
    forbidden_terms = ["hallucinated", "I am not sure of anything", "I could be drastically wrong"]
    for term in forbidden_terms:
        if any(term in str(report[v]).lower() for v in report):
            return False, f"Report contains forbidden terms: {term}"

    return True, "Validation successful"
