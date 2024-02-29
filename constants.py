k8s_verbs = [
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

# TODO: obtain doing api-resources

k8s_resources = [
    "configmap",
    "cm",
    "cronjob",
    "cj",
    "daemonset",
    "ds",
    "deployment",
    "deploy",
    "endpoint",
    "ep",
    "event",
    "ev",
    "horizontalpodautoscaler",
    "hpa",
    "ingress",
    "ing",
    "job",
    "limitrange",
    "lr",
    "namespace",
    "ns",
    "networkpolicy",
    "netpol",
    "node",
    "no",
    "persistentvolume",
    "pv",
    "persistentvolumeclaim",
    "pvc",
    "pod",
    "po",
    "poddisruptionbudget",
    "pdb",
    "podsecuritypolicy",
    "psp",
    "replicaset",
    "rs",
    "replicationcontroller",
    "rc",
    "resourcequota",
    "quota",
    "role",
    "rolebinding",
    "secret",
    "service",
    "svc",
    "serviceaccount",
    "sa",
    "statefulset",
    "sts",
    "storageclass",
    "sc",
    "volumeattachment",
    "customresourcedefinition",
    "crd",
]
