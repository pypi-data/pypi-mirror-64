import json
import os.path
from abc import abstractmethod
from pathlib import Path

from mygp_cli.state import State


class StateStorage:
    @abstractmethod
    def load_state(self) -> State:
        ...

    @abstractmethod
    def save_state(self, state: State) -> None:
        ...


class StateFile(StateStorage):
    def __init__(self) -> None:
        self.state_file_name: str \
            = os.path.join(str(Path.home()), ".mygp", "state.json")

    def load_state(self) -> State:
        if os.path.isfile(self.state_file_name):
            with open(self.state_file_name) as file:
                return State(json.load(file))
        else:
            return State({})

    def save_state(self, state: State) -> None:
        state_dir = os.path.dirname(self.state_file_name)
        if not os.path.exists(state_dir):
            os.makedirs(state_dir)
        with open(self.state_file_name, "w") as file:
            json.dump(state.state_dict(), file, indent=4)
