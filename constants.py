from api_service import get_api_resources
k8s_verbs = [
    "clear",
    "apply",
    "exit",
]

k8s_verbs_name = [
    "logs",
]

k8s_verbs_resource_name = [
    "get",
    "create",
    "describe",
    "edit",
    "delete",
    "use",
    "exec",
]

k8s_all_verbs = list(
    set(
        [
            # TODO position
            "scale",
            "rollout",
            "expose",
            "attach",
            "port-forward",
            "proxy",
            "auth",
            "api-resources",
            "top",
            "config",
            "version",
        ]
        + k8s_verbs
        + k8s_verbs_name
        + k8s_verbs_resource_name
    )
)



k8s_resources = get_api_resources()
