import os
import subprocess
from prompt_toolkit.shortcuts import prompt, CompleteStyle
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from prompt_toolkit import HTML
from custom_completer import CustomCompleter

style = Style.from_dict(
    {
        "path": "#33E0FF bold",
        "symbol": "#1848FF bold",
        "namespace": "#FF1818 bold",
        "start": "#FFFF00 bold",
    }
)

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
    "kubectl",
]


def get_available_namespaces():
    try:
        result = subprocess.run(
            "kubectl get namespaces --no-headers",
            shell=True,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print("No kubernetes cluster found")
            return None

        namespace_lines = result.stdout.strip().split("\n")
        return [line.split()[0] for line in namespace_lines]
    except Exception as e:
        print(f"Error fetching namespaces: {e}")
        return None


def handle_special_command(user_input):
    if user_input.startswith("cd "):
        try:
            directory = user_input.split(" ", 1)[1]
            os.chdir(directory)
            return True
        except Exception as e:
            print(f"Error changing directory: {e}")
    return False


def main():
    current_namespace = "default"
    history_file = os.path.join(os.path.dirname(__file__), ".k8sh_history")
    available_namespaces = get_available_namespaces()

    if available_namespaces is None:
        return

    history = FileHistory(history_file)
    completer = CustomCompleter(history)

    while True:
        try:
            current_directory = os.path.basename(os.getcwd())
            prompt_text = HTML(
                f"<path>{current_directory}</path> <symbol>(</symbol><namespace>{current_namespace}</namespace><symbol>)</symbol> <start>$</start> "
            )
            user_input = prompt(
                prompt_text,
                completer=completer,
                history=history,
                complete_style=CompleteStyle.MULTI_COLUMN,
                style=style,
            ).strip()

            if not user_input:
                continue

            if user_input == "exit":
                return

            if user_input.startswith("use "):
                namespace = user_input.split(" ")[1]
                if namespace in available_namespaces:
                    current_namespace = namespace
                    print(f"Switched to namespace '{current_namespace}'")
                else:
                    print(f"Namespace '{namespace}' not found")
                continue

            if user_input == "reset":
                completer.reset_options()
                continue

            if handle_special_command(user_input):
                continue

            if not any(user_input.startswith(cmd) for cmd in linux_commands):
                user_input = f"kubectl {user_input} -n {current_namespace}"

            result = subprocess.run(
                user_input,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            print(result.stdout)
            print(result.stderr, end="")

            if result.returncode == 0 and user_input.startswith("kubectl"):
                completer.add_options(user_input.split(" ")[1:])

        except KeyboardInterrupt:
            print("\nTo exit, type 'exit'")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
