import os
from prompt_toolkit import HTML
from prompt_toolkit.completion import Completer, Completion
from pathlib import Path

k8s_options = [
    "create",
    "apply",
    "get",
    "describe",
    "delete",
    "logs",
    "exec",
    "cp",
    "attach",
    "top",
    "cordon",
    "uncordon",
    "drain",
    "taint",
    "describe",
    "rolling-update",
    "scale",
    "autoscale",
    "expose",
    "run",
    "set",
    "label",
    "annotate",
    "explain",
    "rollout",
    "create",
    "expose",
    "run",
    "set",
    "explain",
    "rollout",
    "edit",
    "replace",
    "wait",
    "delete",
    "describe",
    "get",
    "logs",
    "attach",
    "port-forward",
    "proxy",
    "cp",
    "auth",
    "diff",
    "kustomize",
    "wait",
    "kubeadm",
    "kubeconfig",
    "plugin",
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
    if len(command.split()) > 1:
        current_directory = Path(os.getcwd())
        subcommand = command.split()[1]
        for entry in current_directory.iterdir():
            if entry.is_dir() and entry.name.startswith(subcommand):
                yield Completion(entry.name[len(subcommand) :], start_position=0)


def none_func():
    return []


linux_options = {
    "ls": none_func,
    "cd": print_directories,
    "echo": none_func,
    "mkdir": none_func,
    "rmdir": none_func,
    "rm": none_func,
    "cat": none_func,
    "touch": none_func,
    "pwd": none_func,
    "chmod": none_func,
    "chown": none_func,
    "find": none_func,
    "grep": none_func,
    "awk": none_func,
    "sed": none_func,
    "sort": none_func,
    "cut": none_func,
    "curl": none_func,
}


class CustomCompleter(Completer):
    def __init__(self, history):
        self.history = history
        self.available_options = k8s_options

    def get_completions(self, document, complete_event):
        command = document.text_before_cursor
        if not command:
            return

        if command.startswith("kubectl"):
            for option in self.available_options:
                if option.startswith(command.split()[-1]):
                    yield Completion(option, start_position=-len(command.split()[-1]))

        elif any(command.startswith(opt) for opt in linux_options):
            func = linux_options.get(command.split()[0], none_func)
            for completion in func(command):
                yield completion

        elif not any(
            command.startswith(opt) for opt in k8s_options + list(linux_options.keys())
        ):
            for option in k8s_options + list(linux_options.keys()):
                if option.startswith(command):
                    yield Completion(option)

    def add_options(self, options):
        self.available_options.extend(options)
        self.available_options = list(set(self.available_options))

    def reset_options(self):
        self.available_options = k8s_options
