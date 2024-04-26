import shutil
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit import HTML
from configuration import Configuration
from grammar import kubectlCommand, typeCommand
from constants import k8s_all_verbs, k8s_flags, k8s_api_resources
from api_service import get_resources
from pyparsing import ParseException

class CustomCompleter(Completer):
    def __init__(self, history):
        self.history = history

    def get_completions(self, document, _):
        line, word, last_word = self.handle_line(document)
        try:
            parsed = kubectlCommand.parseString(line,parseAll=True)

            next = list(parsed.keys()).pop()
            parts = next.split(" ")

            for part in parts:
                if part == "flags":
                    verb = line.split()[0]
                    yield from self.handle_flags(word, last_word, verb)
                if part == "name":
                    yield from self.handle_name(line, word)
                if part == "resource":
                    yield from self.handle_resource(word)

            yield from self.handle_prev_command(line, word)

        except ParseException as pe:
            if "verb" == str(pe.parserElement) and not last_word:
                yield from self.handle_verb(word)
            if "resource" == str(pe.parserElement):
                yield from self.handle_resource(word)
            if "name" == str(pe.parserElement):
                yield from self.handle_name(line, word)        

    def handle_line(self, document):
        line = document.current_line_before_cursor
        word = line.split(" ")[-1]
        if len(line.split(" ")) > 1:
            last_word = line.split(" ")[-2]
        else:
            last_word = ""
        if line.endswith(" ") or " " not in line:
            line = line.strip()
        else:
            line = line[: line.rfind(" ")].strip()
        return line, word, last_word

    def handle_verb(self, word):
        for verb in k8s_all_verbs:
            if verb.startswith(word):
                yield self.create_completion(verb, len(word))
        
    def handle_flags(self, word, last_word, verb):
        if verb not in k8s_flags:
            return
        k8s_verb_flags = k8s_flags[verb]
        if word:
            for key, values in k8s_verb_flags.items():
                if key.startswith(word):
                    if not values:
                        yield self.create_completion(key, len(word))
                    else:
                        for value in values:
                            completion_key = f"{key} {value}"
                            yield self.create_completion(completion_key, len(word))
        else:
            if last_word and last_word in k8s_verb_flags:
                values = k8s_verb_flags[last_word]
                if values:
                    for value in values:
                        if value.startswith(word):
                            yield self.create_completion(value, len(word))
            else:
                for key, values in k8s_verb_flags.items():
                    if not values:
                        yield self.create_completion(key, len(word))
                    else:
                        for value in values:
                            completion_key = f"{key} {value}"
                            yield self.create_completion(completion_key, len(word))

    def handle_name(self, line, word):
        type = "pods" if not line.startswith("use") else "namespaces"
        for w in line.split(" "):
            if typeCommand.matches(w):
                type = w

        resources = get_resources(
            Configuration().flags, Configuration().current_namespace, type
        )

        for resource in resources:
            if resource.startswith(word):
                yield self.create_completion(resource, len(word))

    def handle_resource(self, word):
        for resource in k8s_api_resources:
            if resource.startswith(word):
                yield self.create_completion(resource, len(word))

    def handle_prev_command(self, line, word):
        for prev_command in reversed(list(set(self.history.get_strings()))):
            if prev_command.startswith(line) and len(line.split(" ")) > 2:
                length = len(line) - len(word) + 1
                yield self.create_completion(prev_command, length)

    def create_completion(self, display_key, word_length):
        terminal_width, _ = shutil.get_terminal_size()
        display_width = (terminal_width // 3) - 2
        formatted_display = HTML("<b>%s</b>") % display_key.ljust(display_width)
        return Completion(
            display_key, start_position=-word_length, display=formatted_display
        )
