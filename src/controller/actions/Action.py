from abc import ABC, abstractmethod
from flask import request

from src.controller.actions.Output import Output

class Action(ABC):

    @abstractmethod
    def exec(self, request) -> Output:
        pass