def validate_report(report):
    """
    Sistema de Guardrail para validar el reporte de la IA.
    """
    required_fields = ["Findings", "Impression", "Recommendations"]

    # 1. Verificar presencia de campos
    for field in required_fields:
        if field not in report or not report[field]:
            return False, f"Falta el campo requerido: {field}"

    # 2. Filtrar términos que sugieran falta de certeza excesiva o "alucinaciones" detectables
    forbidden_terms = ["alucinado", "no estoy seguro de nada", "puedo equivocarme drásticamente"]
    for term in forbidden_terms:
        if any(term in str(report[v]).lower() for v in report):
            return False, f"El reporte contiene términos prohibidos: {term}"

    return True, "Validación exitosa"
