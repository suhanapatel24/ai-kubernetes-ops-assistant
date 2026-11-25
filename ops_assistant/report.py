from datetime import datetime, timezone

def build_report(snapshot, findings):
    critical = sum(f.severity == "critical" for f in findings)
    warning = sum(f.severity == "warning" for f in findings)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "namespace": snapshot.get("namespace", "unknown"),
        "summary": {
            "pods_observed": len(snapshot.get("pods", [])),
            "critical_findings": critical,
            "warning_findings": warning,
            "status": "critical" if critical else ("warning" if warning else "healthy"),
        },
        "findings": [f.to_dict() for f in findings],
    }
