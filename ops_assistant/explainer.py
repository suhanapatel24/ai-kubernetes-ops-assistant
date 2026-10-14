import json

SYSTEM_GUIDANCE = """You are a Kubernetes incident explanation assistant.
Use only the supplied deterministic incident report as evidence.
Do not claim that a command was executed or that remediation succeeded.
Do not request or expose secrets.
Provide: likely interpretation, evidence, safe verification steps, and remediation options requiring operator review.
"""

def build_explanation_prompt(report):
    return (
        SYSTEM_GUIDANCE
        + "\nIncident report:\n"
        + json.dumps(report, indent=2)
    )

def explain_with_client(report, client):
    """Provider-neutral hook. The caller supplies an LLM client implementing generate(prompt)."""
    return client.generate(build_explanation_prompt(report))
