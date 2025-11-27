from abc import ABC, abstractmethod

class IBcryptService(ABC):

    @staticmethod       
    @abstractmethod     
    def HashPassword(plain_password: str) -> str:
        pass

    @staticmethod       
    @abstractmethod     
    def CheckPassword(plain_password: str , hashed_password: str) -> bool:
        pass