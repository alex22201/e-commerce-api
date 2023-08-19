from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

oath2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')

password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
