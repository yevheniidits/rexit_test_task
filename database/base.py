from abc import ABC
from abc import abstractmethod


class Database(ABC):
    """
    Database context manager
    """

    def __init__(self, driver) -> None:
        self.driver = driver

    @abstractmethod
    def connect(self):
        raise NotImplementedError()

    def __enter__(self):
        self.connection = self.connect()
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exception_type, exc_val, traceback):
        self.cursor.close()
        self.connection.close()



