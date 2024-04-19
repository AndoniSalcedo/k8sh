import shutil
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit import HTML
from api_service import get_resources
from configuration import Configuration
from grammar import kubectlCommand, typeCommand
from constants import k8s_all_verbs, k8s_flags, k8s_api_resources
from pyparsing import ParseException


class CustomCompleter(Completer):

    def __init__(self, history):

        self.history = history

    def get_completions(self, document, _):

        line, word, last_word = self.handle_line(document)

        try:
            parsed = kubectlCommand.parseString(line, parseAll=True)

            next = list(parsed.keys()).pop()

            parts = next.split(" ")

            for part in parts:
                if part == "flags":
                    yield from self.handle_flags(word, last_word,line.split()[0])

                if part == "name":
                    yield from self.handle_name(line, word)

                if part == "resource":
                    yield from self.handle_resource(word)

            """Autocompletar con comando anterior"""
            """ 
            for prev_command in reversed(list(set(self.history.get_strings()))):
                if (
                    prev_command.startswith(document.current_line_before_cursor)
                    and len(document.current_line_before_cursor.split(" ")) > 3
                ):
                    yield Completion(
                        prev_command,
                        start_position=-len(document.current_line_before_cursor),
                        display=HTML("<b>%s</b>") % prev_command,
                    )
            """
        except ParseException:
            if line and len(line.split(" ")) < 2:
                for verb in k8s_all_verbs:
                    if verb.startswith(word):
                        yield self.create_completion(verb,len(word))
            

    def handle_line(self,document):
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
        type = "pods"  if not line.startswith("use") else "namespaces"  
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
                yield self.create_completion(resource, len(word))

    def handle_resource(self,word):
        for resource in k8s_api_resources:
            if resource.startswith(word):
                yield self.create_completion(resource,len(word))

    def create_completion(self,display_key, word_length):
        terminal_width, _ = shutil.get_terminal_size()
        display_width = (terminal_width // 3) - 2
        formatted_display = HTML("<b>%s</b>") % display_key.ljust(display_width)
        return Completion(
            display_key, start_position=-word_length, display=formatted_display
        )
