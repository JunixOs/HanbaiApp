from src.bussines_layer.services.module_gestion_usuarios.interfaces.IBcryptService import IBcryptService

import bcrypt

class BcryptService(IBcryptService):

    @staticmethod
    def HashPassword(plain_password: str) -> str:
        salt = bcrypt.gensalt(rounds=10)
        hashed_password = bcrypt.hashpw(plain_password.encode("utf-8") , salt)
        return hashed_password.decode("utf-8")

    @staticmethod
    def CheckPassword(plain_password: str , hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )