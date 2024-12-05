import subprocess
import re
from prompt_toolkit.shortcuts import prompt, CompleteStyle
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from api_service import get_namespaces
from configuration import Configuration
from custom_completer import CustomCompleter
import os
from prompt_toolkit import HTML
from pyparsing import ParseResults
from grammar import kubectlCommand, flagCommand
from language_processor import find_closest_input
from constants import k8s_flags

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
                    Configuration().set_namespace(new_namespace)

                    print(f"Namespace cambiado a '{Configuration().current_namespace}'")
                else:
                    print(f"Namespace '{new_namespace}' no encontrado")
                continue

            final_user_input = (
                f"kubectl {Configuration().flags} -n {Configuration().current_namespace} {user_input}"
            )

            result = subprocess.run(
                final_user_input,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            combined_output = result.stdout + result.stderr

            print(combined_output, end="")

            if result.returncode != 0:
                closest_input = find_closest_input(user_input)
                
                if(user_input == closest_input):
                    continue
                
                final_user_input = (
                f"kubectl {Configuration().flags} -n {Configuration().current_namespace} {closest_input}"
            ) 
                confirmation_prompt = HTML(
                    f'<path>{Configuration().current_directory}</path> <symbol>(</symbol><namespace>{Configuration().current_namespace}</namespace><symbol>)</symbol> <start>$</start> Suggested: "{closest_input}" [Y/n] '
                )
                user_input = (
                    prompt(
                        confirmation_prompt,
                        style=style,
                    )
                    .strip()
                    .lower()
                )

                if user_input != "n":
                    result = subprocess.run(
                        final_user_input,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                    )
                    combined_output = result.stdout + result.stderr
                    print(combined_output, end="")
                continue

            parsed = kubectlCommand.parseString(user_input, parseAll=True)
            verb = parsed.pop(0)
            for value in parsed:
                if isinstance(value, ParseResults):
                    if len(value) == 1 and isinstance(value[0], str):
                        value_to_process = value[0]
                    else:
                        value_to_process = " ".join(list(value))
                else:
                    value_to_process = value
                if flagCommand.matches(value_to_process) and verb in k8s_flags:
                    flag = value_to_process.split(" ")
                    if len(flag) > 1:
                        key, val = flag
                        if key not in k8s_flags[verb]:
                            k8s_flags[verb][key] = set()
                        k8s_flags[verb][key].add(val)
                    else:
                        key = flag.pop()
                        k8s_flags[verb][key] = []

        except KeyboardInterrupt:
            print("\nPara salir del programa, escribe 'exit'")
        except Exception as e:
            print("Error: aqui", e)



