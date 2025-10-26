from passlib.context import CryptContext

hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def hashing(password: str):
        return hash_context.hash(password)

    def verify(password, hash_pass):
        return hash_context.verify(password, hash_pass)
