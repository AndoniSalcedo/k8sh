import os
import json
import subprocess

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Configuration(metaclass=SingletonMeta):
    def __init__(self):
        self.flags = ""
        self.current_namespace = "default"
        self.current_directory = os.path.basename(os.getcwd())
        self.current_context = self._get_current_context()
        self.aliases = {
            "kgp": "get pods",
            "kdp": "describe pod",
            "kd": "delete",
            "kgd": "get deployments",
            "kgs": "get services",
        }
        self.style_config = {
            "path": "#33E0FF bold",
            "symbol": "#1848FF bold",
            "namespace": "#FF1818 bold",
            "context": "#ffb86c bold",
            "start": "#FFFF00 bold",
        }
        self.load_config()

    def _get_current_context(self):
        try:
            result = subprocess.run(
                "kubectl config current-context",
                shell=True,
                capture_output=True,
                text=True,
            )
            return result.stdout.strip() if result.returncode == 0 else "unknown"
        except Exception:
            return "unknown"

    def load_config(self):
        config_path = os.path.expanduser("~/.k8sh.json")
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    config = json.load(f)
                    if "aliases" in config:
                        self.aliases.update(config["aliases"])
                    if "style" in config:
                        self.style_config.update(config["style"])
            except Exception as e:
                print(f"Error loading config: {e}")

    def save_config(self):
        config_path = os.path.expanduser("~/.k8sh.json")
        try:
            with open(config_path, "w") as f:
                json.dump({"aliases": self.aliases, "style": self.style_config}, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def set_flags(self, value):
        self.flags = value

    def set_namespace(self, value):
        self.current_namespace = value

    def set_context(self, value):
        self.current_context = value
