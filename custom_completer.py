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

    def get_completions(self, document, complete_event):
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
        terminal_width, _ = shutil.get_terminal_size()

        try:
            parsed = kubectlCommand.parseString(line, parseAll=True)

            next = list(parsed.keys()).pop()

            parts = next.split(" ")

            for part in parts:
                #TODO: refactorizar
                if part == "flags":
                    if word:
                        for key, values in k8s_flags.items():
                            if key.startswith(word):
                                if not values:
                                    display_width = (terminal_width // 3) - 2
                                    display = HTML("<b>%s</b>") % key.ljust(
                                        display_width
                                    )
                                    yield Completion(
                                        key, start_position=-len(word), display=display
                                    )
                                else:
                                    for value in list(values):
                                        output = f"{key} {value}"
                                        display_width = (terminal_width // 3) - 2
                                        display = HTML("<b>%s</b>") % output.ljust(
                                            display_width
                                        )
                                        yield Completion(
                                            output,
                                            start_position=-len(word),
                                            display=display,
                                        )
                    else:
                        if last_word in k8s_flags.keys() and k8s_flags[last_word]:
                            for value in list(k8s_flags[last_word]):
                                if value.startswith(word):
                                    display_width = (terminal_width // 3) - 2
                                    display = HTML("<b>%s</b>") % value.ljust(
                                            display_width
                                        )
                                    yield Completion(
                                            value,
                                            start_position=-len(word),
                                            display=display,
                                        )

                        else: 
                            for key, values in k8s_flags.items():
                                if not values:
                                    display_width = (terminal_width // 3) - 2
                                    display = HTML("<b>%s</b>") % key.ljust(display_width)
                                    yield Completion(
                                        key, start_position=-len(word), display=display
                                    )
                                else:
                                    for value in values:
                                        output = f"{key} {value}"
                                        display_width = (terminal_width // 3) - 2
                                        display = HTML("<b>%s</b>") % output.ljust(
                                            display_width
                                        )
                                        yield Completion(
                                            output,
                                            start_position=-len(word),
                                            display=display,
                                        )

                if part == "name":
                    type = "pods"  # TODO: solve this to use with "use" default pods cause cmd only refered to pods
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
                    for resource in k8s_api_resources:
                        if resource.startswith(word):
                            display_width = (terminal_width // 3) - 2
                            display = HTML("<b>%s</b>") % resource.ljust(display_width)
                            yield Completion(
                                resource, start_position=-len(word), display=display
                            )
            """Autocompletar con comando anterior"""
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
        except ParseException:
            if line and len(line.split(" ")) < 2:
                for verb in k8s_all_verbs:
                    if verb.startswith(word):
                        display_width = (terminal_width // 3) - 2
                        display = HTML("<b>%s</b>") % verb.ljust(display_width)
                        yield Completion(
                            verb, start_position=-len(word), display=display
                        )
