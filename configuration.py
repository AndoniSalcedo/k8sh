import os

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

    def set_flags(self, value):
        self.flags = value
    def set_namespace(self, value):
        self.current_namespace = value
