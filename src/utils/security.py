import datetime
import os
from typing import Optional
from dotenv import load_dotenv

from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
import jose.jwt
from database.config import user_table, database

from passlib.context import CryptContext

from models.user import Role

load_dotenv()

pwd_content =CryptContext(schemes=["bcrypt"])
SECRET_KEY = os.getenv("SECRET_KEY") 

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set!")
ALGORITHM="HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_password_hash(password:str):
    return pwd_content.hash(password)

def verify_password(password: str, hashed_password: str):
    return pwd_content.verify(password, hashed_password)

def create_access_token(id:int, role: str):
    expire = datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(minutes=30)
    expire = int(expire.timestamp()) 
    jwt_data = {"sub":str(id),"role":role,"exp":expire, "type": "access"}
    encoded_jwt = jose.jwt.encode(jwt_data,key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_user(email: str) -> Optional[dict]:
    query = user_table.select().where(user_table.c.email==email)
    result = await database.fetch_one(query)
    return result

def decode_access_token(token: str):
    try:
        payload = jose.jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jose.jwt.JWTError:
        raise HTTPException(status_code=401,detail="Invalid token")
    
async def get_current_user(token: str=Security(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload.get("type") is None or payload.get("type")!="access":
        raise HTTPException(status_code=401, detail="invalid token")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload
def get_current_user_id(token: str=Security(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload.get("type") is None or payload.get("type")!="access":
        raise HTTPException(status_code=401, detail="invalid token")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = int(payload.get("sub"))
    # role = payload.get("role")
    return user_id
def get_current_user_role(token: str=Security(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload.get("type") is None or payload.get("type")!="access":
        raise HTTPException(status_code=401, detail="invalid token")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    role = payload.get("role")
    return role

def role_required(required_role: Role):
    def role_checker(user_role: str = Depends(get_current_user_role)):
        if user_role != required_role.value:
            raise HTTPException(status_code=403, detail="Access denied")
        return user_role
    return role_checker

# async def get_pwd(password: str):
    # cond2=user_table.select().where(user_table.c.password==password)
    # result = await database.fetch_one(cond2)
    # if result:
        # return result
def create_confirmation_token(email: str):
    expire = datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(minutes=1440)
    expire = int(expire.timestamp()) 
    jwt_data = {"sub":email, "exp":expire, "type": "confirmation"}
    encoded_jwt = jose.jwt.encode(jwt_data,key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_confirmation_token(token: str):
    try:
        payload = jose.jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except jose.jwt.JWTError:
        raise HTTPException(status_code=401,detail="Invalid token") 
    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="invalid token")    
       
    if payload.get("type") is None or payload.get("type")!="confirmation":
        raise HTTPException(status_code=401, detail="invalid token")    
    return email