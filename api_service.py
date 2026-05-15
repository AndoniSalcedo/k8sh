import subprocess
import time

CACHE = {}
CACHE_TTL = 10  # Cache time-to-live in seconds

def get_api_resources(flags):
    # API resources usually don't change often, could cache this as well but keeping it simple
    result = subprocess.run(
        f"kubectl {flags} api-resources --no-headers",
        shell=True,
        capture_output=True,
        text=True,
    )
    all_resources = ["all"]
    if result.stdout:
        resources_spec = result.stdout.strip().split("\n")
        for resource_scpec in resources_spec:
            parts = resource_scpec.split()
            if not parts:
                continue
            all_resources.append(parts[0])
            all_resources.append(parts[-1].lower())
            if len(parts) > 1 and "/" not in parts[1]:
                all_resources.append(parts[1])
    
    return list(set(all_resources))

def get_resources(flags, namespace, resource):
    cache_key = f"{flags}_{namespace}_{resource}"
    current_time = time.time()
    
    if cache_key in CACHE and current_time - CACHE[cache_key]['time'] < CACHE_TTL:
        return CACHE[cache_key]['data']

    ns_flag = f"-n {namespace}" if namespace else ""
    result = subprocess.run(
        f"kubectl {flags} {ns_flag} get {resource} --no-headers -o custom-columns=NAME:.metadata.name",
        shell=True,
        capture_output=True,
        text=True,
    )

    resources = [r for r in result.stdout.strip().split("\n") if r]
    CACHE[cache_key] = {'time': current_time, 'data': resources}
    return resources

def get_pods(flags, namespace):
    return get_resources(flags, namespace, "pod")

def get_namespaces(flags):
    return get_resources(flags, "", "namespace")

def get_contexts(flags):
    result = subprocess.run(
        f"kubectl config get-contexts -o name",
        shell=True,
        capture_output=True,
        text=True,
    )
    return [c for c in result.stdout.strip().split("\n") if c]

