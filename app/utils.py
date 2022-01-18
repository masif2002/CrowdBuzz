from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify(raw_password, hashed_pass):
    return pwd_context.verify(raw_password, hashed_pass)