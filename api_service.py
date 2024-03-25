import subprocess


def get_api_resources():
    ''''''
    result = subprocess.run(
        f"kubectl api-resources --no-headers",
        shell=True,
        capture_output=True,
        text=True,
    )
    all_resources = []
    resources_spec = result.stdout.strip().split("\n")
    for resource_scpec in resources_spec:
        parts = resource_scpec.split()
        all_resources.append(parts[0])
        all_resources.append(parts[-1].lower())
        if len(parts) > 1 and "/" not in parts[1]:
            all_resources.append(parts[1])
    return all_resources

def get_resources(flags, namespace, resource):
    """
    Obtiene una lista de los nombres de los namespaces disponibles en Kubernetes.
    Utiliza el comando 'kubectl get namespaces --no-headers' para obtener la lista.
    """

    if namespace:
        namespace = f"-n {namespace}"
    result = subprocess.run(
        f"kubectl {flags} {namespace} get {resource} --no-headers -o custom-columns=NAME:.metadata.name",
        shell=True,
        capture_output=True,
        text=True,
    )

    resources = result.stdout.strip().split("\n")
    return resources

def get_pods(flags, namespace):
    return get_resources(flags,namespace, "pod")


def get_namespaces(flags):
   return get_resources(flags,"","namespace")

