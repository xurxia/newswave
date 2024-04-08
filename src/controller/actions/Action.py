from abc import ABC, abstractmethod
from flask import Request

from src.controller.actions.Output import Output

class Action(ABC):

    @abstractmethod
    def exec(self, request : Request) -> Output:
        pass