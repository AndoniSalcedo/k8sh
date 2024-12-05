from api_service import get_api_resources
from configuration import Configuration

k8s_verbs = [
    "clear",
    "apply",
    "exit",
    "version",
    "api-resources",
    "proxy",
]

k8s_verbs_name = [
    "logs",
    "use",
    "scale",
    "attach",
]

k8s_verbs_resource_name = [
    "get",
    "create",
    "describe",
    "edit",
    "delete",
    "exec",
    "top",
    "expose",
]

k8s_all_verbs = list(
    set(
        [
            # TODO position
            "rollout",
            "port-forward",
            "auth",
            "config", 
        ]
        + k8s_verbs
        + k8s_verbs_name
        + k8s_verbs_resource_name
    )
)

k8s_api_resources = get_api_resources(Configuration().flags)

k8s_flags = {key: {} for key in k8s_all_verbs}

