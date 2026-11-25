from kubernetes import client, config

def _load_config():
    try:
        config.load_incluster_config()
    except config.ConfigException:
        config.load_kube_config()

def collect(namespace="default"):
    _load_config()
    core = client.CoreV1Api()
    pods = []
    for pod in core.list_namespaced_pod(namespace).items:
        containers = []
        statuses = pod.status.container_statuses or []
        for status in statuses:
            waiting = status.state.waiting.reason if status.state and status.state.waiting else None
            terminated = (
                status.last_state.terminated.reason
                if status.last_state and status.last_state.terminated
                else None
            )
            containers.append({
                "name": status.name,
                "ready": status.ready,
                "waiting_reason": waiting,
                "terminated_reason": terminated,
            })
        pods.append({
            "name": pod.metadata.name,
            "phase": pod.status.phase,
            "containers": containers,
        })

    events = []
    for event in core.list_namespaced_event(namespace).items:
        if event.type == "Warning":
            events.append({
                "type": event.type,
                "reason": event.reason,
                "message": event.message,
                "resource": f"{event.involved_object.kind}/{event.involved_object.name}",
            })
    return {"namespace": namespace, "pods": pods, "events": events}
