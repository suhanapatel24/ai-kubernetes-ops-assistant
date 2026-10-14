from ops_assistant.explainer import build_explanation_prompt

def test_prompt_contains_evidence_and_safety():
    report = {"summary": {"status": "critical"}, "findings": [{"reason": "OOMKilled"}]}
    prompt = build_explanation_prompt(report)
    assert "OOMKilled" in prompt
    assert "Do not claim" in prompt
    assert "operator review" in prompt
