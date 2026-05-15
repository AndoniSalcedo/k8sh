import subprocess
import re
from prompt_toolkit.shortcuts import prompt, CompleteStyle
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from api_service import get_namespaces, get_contexts
from configuration import Configuration
from custom_completer import CustomCompleter
import os
from prompt_toolkit import HTML
from pyparsing import ParseResults, ParseException
from grammar import kubectlCommand, flagCommand
from language_processor import find_closest_input
from constants import k8s_flags
from highlighter import highlight_output




def main():
    history_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ".k8sh_history"
    )
    history = FileHistory(history_file)
    completer = CustomCompleter(history)

    style = Style.from_dict(Configuration().style_config)

    while True:
        try:
            prompt_text = HTML(
                f"<path>{Configuration().current_directory}</path> <symbol>(</symbol><context>{Configuration().current_context}</context><symbol>|</symbol><namespace>{Configuration().current_namespace}</namespace><symbol>)</symbol> <start>$</start> "
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

            input_parts = user_input.split(" ")
            if input_parts[0] in Configuration().aliases:
                user_input = Configuration().aliases[input_parts[0]] + " " + " ".join(input_parts[1:])
                user_input = user_input.strip()

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
                parts = user_input.split(" ")
                if len(parts) > 1:
                    new_namespace = parts[1]
                    if new_namespace in available_namespaces:
                        Configuration().set_namespace(new_namespace)

                        print(f"Namespace cambiado a '{Configuration().current_namespace}'")
                    else:
                        print(f"Namespace '{new_namespace}' no encontrado")
                else:
                    print("Por favor, especifica un namespace")
                continue
            
            if user_input.startswith("ctx ") or user_input.startswith("use-context "):
                available_contexts = get_contexts(Configuration().flags)
                parts = user_input.split(" ")
                if len(parts) > 1:
                    new_context = parts[1]
                    if new_context in available_contexts:
                        res = subprocess.run(f"kubectl config use-context {new_context}", shell=True, capture_output=True, text=True)
                        if res.returncode == 0:
                            Configuration().set_context(new_context)
                            print(f"Contexto cambiado a '{new_context}'")
                        else:
                            print(f"Error al cambiar contexto:\n{res.stderr}")
                    else:
                        print(f"Contexto '{new_context}' no encontrado")
                else:
                    print("Por favor, especifica un contexto")
                continue
            
            if user_input.startswith("watch"):
                command_args = user_input[5:].strip()
                final_user_input = f"watch kubectl {Configuration().flags} -n {Configuration().current_namespace} {command_args}"

                try:
                    subprocess.run(final_user_input, shell=True)
                except KeyboardInterrupt:
                    print("\nSaliendo del modo watch...")
                
                continue


            final_user_input = f"kubectl {Configuration().flags} -n {Configuration().current_namespace} {user_input}"
            

            result = subprocess.run(
                final_user_input,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            combined_output = result.stdout + result.stderr

            print(highlight_output(combined_output), end="")

            if result.returncode != 0:
                closest_input = find_closest_input(user_input)
                
                if(user_input == closest_input):
                    continue
                
                final_user_input = (
                f"kubectl {Configuration().flags} -n {Configuration().current_namespace} {closest_input}"
                )

                confirmation_prompt = HTML(
                    f'<path>{Configuration().current_directory}</path> <symbol>(</symbol><context>{Configuration().current_context}</context><symbol>|</symbol><namespace>{Configuration().current_namespace}</namespace><symbol>)</symbol> <start>$</start> Suggested: "{closest_input}" [Y/n] '
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
                    print(highlight_output(combined_output), end="")
                continue

            
            parsed = kubectlCommand.parse_string(user_input, parse_all=True)
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
        except ParseException:
            pass  # Ignoramos si el comando no está soportado por la gramática para el autocompletado de flags
        except Exception as e:
            print("Error inesperado:", e)



