from prompt_toolkit.completion import Completer, Completion

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
    def __init__(self):
        self.options = set(default_options)
    
    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor()

        if document.char_before_cursor == ' ':
            return

        for option in self.options:
            if option.startswith(word):
                yield Completion(option, start_position=-len(word))
    
    def add_options(self, new_options):
        self.options.update(new_options)
    
    def reset_options(self):
        initial_options = set(default_options)
        self.options = initial_options