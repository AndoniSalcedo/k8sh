import subprocess
import re
from prompt_toolkit.shortcuts import prompt, CompleteStyle
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style

from custom_completer import CustomCompleter
import os
from prompt_toolkit import HTML
import argparse


def change_directory(user_input):
    new_directory = user_input[3:].strip()
    os.chdir(new_directory)


special_commands = {
    "cd": change_directory,
}

linux_commands = [
    "ls",
    "cd",
    "pwd",
    "mkdir",
    "touch",
    "cp",
    "mv",
    "rm",
    "cat",
    "echo",
    "nano",
    "vim",
    "grep",
    "find",
    "chmod",
    "chown",
    "ps",
    "top",
    "htop",
    "kill",
    "sudo",
    "df",
    "du",
    "history",
    "tar",
    "wget",
    "curl",
    "clear",
    "watch",
    # Extra commands
    "kubectl",
]

style = Style.from_dict(
    {
        "path": "#33E0FF bold",
        "symbol": "#1848FF bold",
        "namespace": "#FF1818 bold",
        "start": "#FFFF00 bold",
    }
)


def get_available_namespaces(flags):
    """
    Obtiene una lista de los nombres de los namespaces disponibles en Kubernetes.
    Utiliza el comando 'kubectl get namespaces --no-headers' para obtener la lista.
    """
    result = subprocess.run(
        f"kubectl {flags} get namespaces --no-headers",
        shell=True,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("No kubernetes cluster found")
        return None

    namespace_lines = result.stdout.strip().split("\n")
    namespaces = [line.split()[0] for line in namespace_lines]
    return namespaces


def main():
    parser = argparse.ArgumentParser(description="Kubernetes CLI Tool.")

    parser.add_argument(
        "--kubeconfig", type=str, help="ruta al archivo kubeconfig", default=None
    )
    args = parser.parse_args()

    # Verifica si args.kubeconfig es None
    if args.kubeconfig is None:
        flags = ""
    else:
        flags = f"--kubeconfig {args.kubeconfig}"

    """
    Función principal que ejecuta el bucle principal de la aplicación.
    Permite al usuario ingresar comandos, administrar namespaces y mostrar resultados.
    """
    current_namespace = "default"
    current_directory = os.path.basename(os.getcwd())

    history_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ".k8sh_history"
    )

    available_namespaces = get_available_namespaces(flags)

    if available_namespaces == None:
        return

    history = FileHistory(history_file)

    completer = CustomCompleter(history)

    while True:
        try:
            prompt_text = HTML(
                f"<path>{current_directory}</path> <symbol>(</symbol><namespace>{current_namespace}</namespace><symbol>)</symbol> <start>$</start> "
            )
            user_input = prompt(
                prompt_text,
                completer=completer,
                history=history,
                complete_style=CompleteStyle.MULTI_COLUMN,
                style=style,
            )

            user_input = re.sub(r"\s+", " ", user_input).strip()

            if user_input == "":
                continue

            if user_input == "exit":
                return

            if user_input.startswith("use"):
                available_namespaces = get_available_namespaces(flags)
                new_namespace = user_input.split(" ")[1]
                if new_namespace in available_namespaces:
                    current_namespace = new_namespace
                    print(f"Namespace cambiado a '{current_namespace}'")
                else:
                    print(f"Namespace '{new_namespace}' no encontrado")
                continue

            if user_input.startswith("reset"):
                completer.reset_options()
                continue

            continue_outer_loop = False

            for command in special_commands.keys():
                if user_input.startswith(command):
                    special_commands[command](user_input)
                    continue_outer_loop = True
                    current_directory = os.path.basename(os.getcwd())
                    break

            if continue_outer_loop:
                continue

            if not any(user_input.startswith(commands) for commands in linux_commands):
                user_input = f"kubectl {flags}  -n {current_namespace} {user_input}"

            result = subprocess.run(
                user_input,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            combined_output = result.stdout + result.stderr

            print(combined_output, end="")

            if result.returncode == 0 and user_input.startswith("kubectl"):
                completer.add_options(user_input.split(" "))

        except KeyboardInterrupt:
            print("\nPara salir del programa, escribe 'exit'")
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    main()
