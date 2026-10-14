from dataclasses import dataclass, asdict

@dataclass
class Finding:
    severity: str
    resource: str
    reason: str
    evidence: str
    recommendation: str

    def to_dict(self):
        return asdict(self)

def analyze(snapshot):
    findings = []
    for pod in snapshot.get("pods", []):
        name = pod.get("name", "unknown")
        phase = pod.get("phase", "Unknown")
        if phase == "Pending":
            findings.append(Finding(
                "warning", f"pod/{name}", "PodPending",
                "Pod phase is Pending.",
                "Review scheduling events, resource requests, node capacity, selectors, and taints."
            ))
        for container in pod.get("containers", []):
            cname = container.get("name", "unknown")
            waiting = container.get("waiting_reason")
            terminated = container.get("terminated_reason")
            ready = container.get("ready", False)
            if waiting in {"CrashLoopBackOff", "ImagePullBackOff", "ErrImagePull"}:
                recommendation = (
                    "Inspect previous container logs, configuration, probes, and dependencies."
                    if waiting == "CrashLoopBackOff"
                    else "Verify the image name/tag and registry authentication."
                )
                findings.append(Finding(
                    "critical", f"pod/{name}:{cname}", waiting,
                    f"Container waiting reason is {waiting}.", recommendation
                ))
            if terminated == "OOMKilled":
                findings.append(Finding(
                    "critical", f"pod/{name}:{cname}", "OOMKilled",
                    "The previous container termination reason is OOMKilled.",
                    "Review memory usage and memory requests/limits before changing limits."
                ))
            if not ready and not waiting and phase == "Running":
                findings.append(Finding(
                    "warning", f"pod/{name}:{cname}", "NotReady",
                    "Container is running but not Ready.",
                    "Inspect readiness probes, application health, and dependent services."
                ))
    for event in snapshot.get("events", []):
        if event.get("type") == "Warning":
            findings.append(Finding(
                "warning",
                event.get("resource", "unknown"),
                event.get("reason", "KubernetesWarning"),
                event.get("message", "Kubernetes warning event."),
                "Correlate this event with pod state and recent deployment changes."
            ))
    return findings
