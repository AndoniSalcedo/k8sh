import subprocess
import re

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from custom_completer import CustomCompleter



def get_available_namespaces():
    result = subprocess.run("kubectl get namespaces --no-headers", shell=True, capture_output=True, text=True)
    namespace_lines = result.stdout.strip().split("\n")
    namespaces = [line.split()[0] for line in namespace_lines]
    return namespaces

def main():
    current_namespace = "default"
    history_file = ".k8sh_history"

    available_namespaces = get_available_namespaces()

    completer = CustomCompleter()
    history = FileHistory(history_file)

    while True:

        try:
            #prompt_text = f"\033[1;32m\033[1m({current_namespace}) $\033[0m "
            prompt_text = f"({current_namespace}) $ "
            user_input = prompt(prompt_text, completer=completer,history=history)

            user_input = re.sub(r'\s+', ' ', user_input).strip().lower()  

            if user_input == "exit":
                break
            
            if user_input.startswith("use"):
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
                
            user_input = f"{user_input} -n {current_namespace}"

            if not user_input.startswith("kubectl"):
                user_input = "kubectl " + user_input


            result = subprocess.run(user_input, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            combined_output = result.stdout + result.stderr
            print(combined_output)

            if result.returncode == 0:
                completer.add_options(user_input.split(" "))

        except KeyboardInterrupt:
            print("\nPara salir del programa, escribe 'exit'")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()
