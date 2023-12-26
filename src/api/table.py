from api.connect import Connect
from src.api.connect import AbstractConnect

class Table(AbstractConnect):
    def __init__(self, connection: Connect) -> None:
        super().__init__(connection)