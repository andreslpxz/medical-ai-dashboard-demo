def validate_report(report):
    """
    Guardrail system to validate the AI-generated report against a basic "schema" and content rules.
    """
    required_fields = ["Findings", "Impression", "Recommendations"]

    # 1. JSON Schema-like validation
    for field in required_fields:
        if field not in report:
            return False, f"Missing required field: {field}"
        if not isinstance(report[field], str) or len(report[field].strip()) < 10:
            return False, f"Field '{field}' is too short or invalid."

    # 2. Hallucination / Uncertainty detection
    forbidden_terms = ["hallucinated", "i am not sure of anything", "i could be drastically wrong"]
    for term in forbidden_terms:
        if any(term in str(report[v]).lower() for v in report):
            return False, f"Report contains forbidden terms indicating high uncertainty: {term}"

    # 3. Internal consistency (Minimal check: Impression should not contradict Findings if they mention 'normal')
    # This is a placeholder for more complex logic
    findings_lower = report["Findings"].lower()
    impression_lower = report["Impression"].lower()

    if "normal" in findings_lower and "severe pathology" in impression_lower:
        return False, "Internal inconsistency detected between Findings and Impression."

    return True, "Validation successful"
