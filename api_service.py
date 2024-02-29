import subprocess


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
   return get_resources(flags,"","pod")
