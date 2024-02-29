import resource
import subprocess
import re
from matplotlib.pyplot import flag
from prompt_toolkit.shortcuts import prompt, CompleteStyle
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from api_service import get_namespaces
from configuration import Configuration
from custom_completer import CustomCompleter
import os
from prompt_toolkit import HTML
import argparse

style = Style.from_dict(
    {
        "path": "#33E0FF bold",
        "symbol": "#1848FF bold",
        "namespace": "#FF1818 bold",
        "start": "#FFFF00 bold",
    }
)


def main():
    """
    Función principal que ejecuta el bucle principal de la aplicación.
    Permite al usuario ingresar comandos, administrar namespaces y mostrar resultados.
    """

    history_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ".k8sh_history"
    )

    history = FileHistory(history_file)
    completer = CustomCompleter(history)

    while True:
        try:
            prompt_text = HTML(
                f"<path>{Configuration().current_directory}</path> <symbol>(</symbol><namespace>{Configuration().current_namespace}</namespace><symbol>)</symbol> <start>$</start> "
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

            if user_input.startswith("clear"):
                result = subprocess.run(
                    "clear",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                combined_output = result.stdout + result.stderr

                print(combined_output, end="")
                continue

            if user_input.startswith("use"):
                available_namespaces = get_namespaces(Configuration().flags)
                new_namespace = user_input.split(" ")[1]
                if new_namespace in available_namespaces:
                    current_namespace = new_namespace
                    print(f"Namespace cambiado a '{Configuration().current_namespace}'")
                else:
                    print(f"Namespace '{new_namespace}' no encontrado")
                continue

            if user_input.startswith("reset"):
                completer.reset_options()
                continue

            user_input = f"kubectl {flags} -n {current_namespace} {user_input}"

            result = subprocess.run(
                user_input,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            combined_output = result.stdout + result.stderr

            print(combined_output, end="")

        except KeyboardInterrupt:
            print("\nPara salir del programa, escribe 'exit'")
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
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

    Configuration().set_flags(flags)
    main()
