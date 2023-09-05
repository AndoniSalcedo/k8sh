import shutil
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit import HTML
from pathlib import Path
import os

# Lista de opciones por defecto que se incluirán en el autocompletado.
k8s_options = [
    "create",
    "apply",
    "get",
    "describe",
    "edit",
    "delete",
    "logs",
    "exec",
    "scale",
    "rollout",
    "expose",
    "attach",
    "port-forward",
    "proxy",
    "auth",
    "api-resources",
    "top",
    "config",
    "version",
    # Custom verbs
    "use",
    "exit",
    "reset",
]


def print_files():
    current_directory = Path(os.getcwd())
    for entry in current_directory.iterdir():
        if entry.is_dir():
            display = HTML("<b>%s/</b>") % entry.name
        else:
            display = HTML("<i>%s</i>") % entry.name
        yield Completion(entry.name, start_position=-len(entry.name), display=display)


def print_directories(command):
    current_directory = Path(os.getcwd())
    user_input = (
        command.split(maxsplit=1)[-1] if len(command.split(maxsplit=1)) > 1 else ""
    )

    parts = user_input.split("/")

    if parts[-1] == "":
        parts.pop()
        base_directory = current_directory / "/".join(parts)
        for entry in base_directory.iterdir():
            if entry.is_dir():
                yield Completion(
                    entry.name,
                    start_position=0,
                    display=entry.name,
                )
        yield Completion(
            "..",
            start_position=0,
            display="..",
        )
    else:
        base_directory = current_directory / "/".join(parts[:-1])
        for entry in base_directory.iterdir():
            if entry.is_dir() and entry.name.startswith(parts[-1]):
                yield Completion(
                    entry.name,
                    start_position=-len(parts[-1]),
                    display=entry.name,
                )


def none_func():
    return []


linux_options = {
    "ls": none_func,
    "cd": print_directories,
    "pwd": none_func,
    "mkdir": none_func,
    "touch": none_func,
    "cp": none_func,
    "mv": none_func,
    "rm": none_func,
    "cat": none_func,
    "echo": none_func,
    "nano": none_func,
    "vim": none_func,
    "grep": none_func,
    "find": none_func,
    "chmod": none_func,
    "chown": none_func,
    "ps": none_func,
    "top": none_func,
    "htop": none_func,
    "kill": none_func,
    "sudo": none_func,
    "df": none_func,
    "du": none_func,
    "history": none_func,
    "tar": none_func,
    "wget": none_func,
    "curl": none_func,
}


class CustomCompleter(Completer):
    """Clase que proporciona autocompletado personalizado para comandos de Kubernetes."""

    def __init__(self, history):
        """Inicializa la instancia del autocompletador."""
        self.k8s_options = set(k8s_options)
        self.linux_options = linux_options
        self.history = history

    def get_completions(self, document, complete_event):
        """Obtiene las opciones de autocompletado para el comando actual."""
        word = document.get_word_before_cursor()
        line = document.current_line_before_cursor

        terminal_width, _ = shutil.get_terminal_size()

        for option in self.linux_options:
            if line.startswith(option + " "):
                for completion in self.linux_options[option](line):
                    yield completion
                return

        if document.char_before_cursor == " ":
            return

        for prev_command in reversed(self.history.get_strings()):
            if prev_command.startswith(line) and len(line.split(" ")) > 2:
                yield Completion(
                    prev_command,
                    start_position=-len(line),
                    display=HTML("<b>%s</b>") % prev_command,
                )

        for option in self.k8s_options:
            if option.startswith(word):
                display_width = (terminal_width // 3) - 2
                display = HTML("<b>%s</b>") % option.ljust(display_width)

                yield Completion(option, start_position=-len(word), display=display)

    def add_options(self, new_options):
        """Añade nuevas opciones al conjunto de opciones de autocompletado."""
        self.k8s_options.update(new_options)

    def reset_options(self):
        """Restablece las opciones de autocompletado a su estado inicial."""
        self.k8s_options = set(k8s_options)
