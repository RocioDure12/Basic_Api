from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordServices():
    
    def hash_password(self,password:str):
        return pwd_context.hash(password)
    
    def verify_password(self,hashed_password:str, plain_password):
        return pwd_context.verify(plain_password, hashed_password)
        