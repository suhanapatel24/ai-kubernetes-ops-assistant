# Verification Evidence

Implemented in source:
- [x] deterministic incident analyzer
- [x] sanitized incident fixture
- [x] unit tests
- [x] container definition
- [x] namespace-scoped read-only RBAC
- [x] provider-neutral LLM explanation interface
- [x] CI definition

To verify later on a real cluster:
- [ ] CI run passes
- [ ] image published to a registry
- [ ] ServiceAccount permissions verified with kubectl auth can-i
- [ ] analyzer reads a real test namespace
- [ ] controlled failing workload is detected
- [ ] generated report matches observed Kubernetes state
- [ ] optional LLM explanation evaluated against deterministic evidence

Do not put API keys, kubeconfig credentials, tokens, or Kubernetes Secrets in this repository.
