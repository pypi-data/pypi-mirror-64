import json
import os
from typing import Callable
from pythreepio.errors import TranslationMissing

COMMANDS_FILE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '../../static/mapped_commands_full.json'
        )
    )


def get_mapped_commands() -> dict:
    commands = {}
    with open(COMMANDS_FILE_PATH, 'r') as f:
        commands = json.load(f)
    return commands


class Command(object):

    def __init__(self, function_name: str, args: list,
                 kwargs: dict, exec_fn: Callable = None):
        self.function_name = function_name
        self.args = args
        self.kwargs = kwargs
        self.exec_fn = exec_fn

    def execute_routine(self):
        if self.exec_fn is None:
            raise TranslationMissing()

        return self.exec_fn(*self.args, **self.kwargs)
