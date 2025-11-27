from abc import ABC, abstractmethod

class IBcryptService(ABC):

    @abstractmethod
    @staticmethod
    def HashPassword(plain_password: str) -> str:
        pass

    @abstractmethod
    @staticmethod
    def CheckPassword(plain_password: str , hashed_password: str) -> bool:
        pass