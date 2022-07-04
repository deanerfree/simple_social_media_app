from passlib.context import CryptContext

# THis lets passlib know what library we are using which is bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)

# veryify that the 2 hashes match


def verify(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)
