from prompt_toolkit.completion import Completer, Completion

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
    "reset"
]

class CustomCompleter(Completer):
    """Clase que proporciona autocompletado personalizado para comandos de Kubernetes."""

    def __init__(self):
        """Inicializa la instancia del autocompletador."""
        self.options = set(default_options)
    
    def get_completions(self, document, complete_event):
        """Obtiene las opciones de autocompletado para el comando actual."""
        word = document.get_word_before_cursor()

        if document.char_before_cursor == ' ':
            return

        for option in self.options:
            if option.startswith(word):
                yield Completion(option, start_position=-len(word))
    
    def add_options(self, new_options):
        """Añade nuevas opciones al conjunto de opciones de autocompletado."""
        self.options.update(new_options)
    
    def reset_options(self):
        """Restablece las opciones de autocompletado a su estado inicial."""
        initial_options = set(default_options)
        self.options = initial_options
