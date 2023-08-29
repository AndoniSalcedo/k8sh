import shutil
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit import HTML

# Lista de opciones por defecto que se incluirán en el autocompletado.
default_options = [
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


class CustomCompleter(Completer):
    """Clase que proporciona autocompletado personalizado para comandos de Kubernetes."""

    def __init__(self, history):
        """Inicializa la instancia del autocompletador."""
        self.options = set(default_options)
        self.history = history

    def get_completions(self, document, complete_event):
        """Obtiene las opciones de autocompletado para el comando actual."""
        word = document.get_word_before_cursor()
        line = document.current_line_before_cursor


        terminal_width, _ = shutil.get_terminal_size()

        if document.char_before_cursor == " ":
            return

        for prev_command in reversed(self.history.get_strings()):
            if prev_command.startswith(line) and len(line.split(" ")) > 2:
                yield Completion(prev_command, start_position=-len(line),display= HTML("<b>%s</b>") % prev_command)

        for option in self.options:
            if option.startswith(word):
                display_width = terminal_width // 3
                
                display = HTML("<b>%s</b>") % option.ljust(display_width)

                yield Completion(option, start_position=-len(word),display=display)
    
    def add_options(self, new_options):
        """Añade nuevas opciones al conjunto de opciones de autocompletado."""
        self.options.update(new_options)

    def reset_options(self):
        """Restablece las opciones de autocompletado a su estado inicial."""
        initial_options = set(default_options)
        self.options = initial_options
