# Architecture

## Analysis pipeline
1. Collector reads pod status and warning events through the Kubernetes API.
2. The collector intentionally does not retrieve Kubernetes Secret objects.
3. The deterministic analyzer maps observable failure states to findings.
4. The report layer preserves evidence, severity, and recommendations as structured JSON.
5. An optional provider-neutral LLM adapter receives the structured report and can explain it in operator-friendly language.

## Safety boundary
The Kubernetes ServiceAccount receives only get/list/watch permissions for pods and events in its namespace. It has no create, patch, update, delete, exec, Secret, or cluster-admin permissions.

The LLM is not an autonomous remediation agent. Recommendations require operator review.

## Portfolio value
This architecture demonstrates Kubernetes API integration, RBAC/least privilege, incident-analysis logic, testing, containerization, CI, and responsible AI integration.
