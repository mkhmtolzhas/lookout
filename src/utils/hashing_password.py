from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


if __name__ == "__main__":
    password = "mysecretpassword"

    hashed = hash_password(password)
    print(f"Hashed password: {hashed}")
    print(f"Password verification: {verify_password(password, hashed)}")
    print(f"Password verification (wrong password): {verify_password('wrongpassword', hashed)}")
    