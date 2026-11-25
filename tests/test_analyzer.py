import json
from pathlib import Path
from ops_assistant.analyzer import analyze
from ops_assistant.report import build_report

def test_detects_cluster_problems():
    snapshot = json.loads(Path("tests/fixtures/problem_snapshot.json").read_text())
    findings = analyze(snapshot)
    reasons = {f.reason for f in findings}
    assert "CrashLoopBackOff" in reasons
    assert "PodPending" in reasons
    assert "FailedScheduling" in reasons
    report = build_report(snapshot, findings)
    assert report["summary"]["status"] == "critical"
    assert report["summary"]["critical_findings"] >= 1

def test_healthy_snapshot():
    snapshot = {
        "namespace": "demo",
        "pods": [{"name": "api", "phase": "Running", "containers": [
            {"name": "api", "ready": True, "waiting_reason": None, "terminated_reason": None}
        ]}],
        "events": []
    }
    report = build_report(snapshot, analyze(snapshot))
    assert report["summary"]["status"] == "healthy"
