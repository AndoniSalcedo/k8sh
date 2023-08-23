import subprocess
import re
import signal
import readline

current_namespace = "default"

def handle_interrupt(signum, frame):
    print("\nPara salir del programa, escribe 'exit'")
    print(f"({current_namespace}) $ ", end='',flush=True)
    signal.signal(signal.SIGINT, handle_interrupt)


def get_available_namespaces():
    result = subprocess.run("kubectl get namespaces --no-headers", shell=True, capture_output=True, text=True)
    namespace_lines = result.stdout.strip().split("\n")
    namespaces = [line.split()[0] for line in namespace_lines]
    return namespaces

def main():
    global current_namespace

    signal.signal(signal.SIGINT, handle_interrupt)
    
    available_namespaces = get_available_namespaces()

    while True:
        user_input = input(f"({current_namespace}) $ ")
        user_input = re.sub(r'\s+', ' ', user_input).strip().lower()  

        if user_input == "exit":
            break
        
        if user_input.startswith("use "):
            new_namespace = user_input.split(" ")[1]
            if new_namespace in available_namespaces:
                current_namespace = new_namespace
                print(f"Namespace cambiado a '{current_namespace}'")
            else:
                print(f"Namespace '{current_namespace}' no encontrado")
            continue

        user_input = f"{user_input} -n {current_namespace}"

        if not user_input.startswith("kubectl"):
            user_input = "kubectl " + user_input

        try:
            result = subprocess.run(user_input, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            combined_output = result.stdout + result.stderr
            print(combined_output)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
