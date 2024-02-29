import shutil
from exceptiongroup import catch
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit import HTML
from api_service import get_resources
from configuration import Configuration

from grammar import kubectlCommand, typeCommand
from constants import k8s_resources, k8s_all_verbs
from pyparsing import ParseException


class CustomCompleter(Completer):
    """Clase que proporciona autocompletado personalizado para comandos de Kubernetes."""

    def __init__(self, history):
        """Inicializa la instancia del autocompletador."""

        self.history = history

    def get_completions(self, document, complete_event):
        """Obtiene las opciones de autocompletado para el comando actual."""
        word = document.get_word_before_cursor()
        line = document.current_line_before_cursor

        if line.endswith(" ") or " " not in line:
            line = line.strip()
        else:
            line = line[: line.rfind(" ")].strip()

        terminal_width, _ = shutil.get_terminal_size()

        try:
            parsed = kubectlCommand.parseString(line, parseAll=True)

            next = list(parsed.keys()).pop()

            parts = next.split(" ")

            for part in parts:

                if part == "flags":
                    """"""
                if part == "name":
                    type = "pods"

                    for w in line.split(" "):
                        parsed = typeCommand.parseString(w, parseAll=True)
                        for key in parsed.keys():
                            if key == "resource":
                                type = parsed[key]
                    resources = get_resources(
                        Configuration().flags, Configuration().current_namespace, type
                    )

                    for resource in resources:
                        if resource.startswith(word):
                            display_width = (terminal_width // 3) - 2
                            display = HTML("<b>%s</b>") % resource.ljust(display_width)
                            yield Completion(
                                resource, start_position=-len(word), display=display
                            )

                if part == "resource":
                    for resource in k8s_resources:
                        if resource.startswith(word):
                            display_width = (terminal_width // 3) - 2
                            display = HTML("<b>%s</b>") % resource.ljust(display_width)
                            yield Completion(
                                resource, start_position=-len(word), display=display
                            )

        except ParseException:
            if line:
                for verb in k8s_all_verbs:
                    if verb.startswith(word):
                        display_width = (terminal_width // 3) - 2
                        display = HTML("<b>%s</b>") % verb.ljust(display_width)
                        yield Completion(
                            verb, start_position=-len(word), display=display
                        )
        return
        """Autocompletar con comando anterior"""
        for prev_command in reversed(list(set(self.history.get_strings()))):
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

    def reset_options(self):
        """Restablece las opciones de autocompletado a su estado inicial."""
