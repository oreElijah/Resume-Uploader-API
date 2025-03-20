from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile, status, Request
from database.config import user_table, database

from utils.email_confirmation import send_confirmation_email
from models.user import UserIn, UserLogin
from utils.security import (
                      create_confirmation_token, create_access_token, 
                      decode_confirmation_token, get_current_user_id, get_password_hash, 
                      get_user, verify_password
                      )

router = APIRouter()

@router.get("/users", status_code=200)
async def get_users():
    query = user_table.select()
    return await database.fetch_all(query)

@router.post("/register", status_code=201)
async def register_user(user: UserIn, request: Request, background_task: BackgroundTasks):
    cond = await get_user(user.email)
    if cond:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "User with the email already exists")
    hashed_password = get_password_hash(user.password)
    query = user_table.insert().values(first_name=user.first_name,middle_name = user.middle_name, last_name=user.last_name, email=user.email, password = hashed_password,role = user.role.value, confirmed=False)
    user_id = await database.execute(query)
    confirmation_url = request.url_for(
                "confirm_email", 
                token=create_confirmation_token(user.email))
    background_task.add_task(send_confirmation_email, user.email, confirmation_url)
    return {
        "Message": "User has been created successfully. Please confirm your email",
        "user_id": user_id,
        "confirmation_url": confirmation_url
        }

@router.post("/login", status_code=200)
async def login_user(user: UserLogin):
    cond = await get_user(user.email)
    if not cond:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with the email does not exist")
    hashed_password = cond["password"]
    # password=get_pwd(user.password)
    if not verify_password(user.password,hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    if not cond["confirmed"]:
        raise HTTPException(status_code=401, detail="User has not confirmed email")
    
    token = create_access_token(cond["id"], cond["role"])
    return {"Message": "User has been logged in successfully",
                    "token": "Bearer " + token}

@router.get("/confirm-email/{token}", name="confirm_email")
async def confirm_email(token: str):
    email = decode_confirmation_token(token)
    query = (
        user_table.update().where(user_table.c.email==email).values(confirmed=True)
    )
    await database.execute(query)
    return {"message": "User confirmed"}

@router.post("/upload_profile_picture", status_code=status.HTTP_200_OK)
async def upload_pfp(file: UploadFile = File(...), user_id:int = Depends(get_current_user_id)):
    # cond = await get_user(user.email)
    with open(f"profile_picture_uploads/{file.filename}", "wb") as f:
        f.write(await file.read())
    query = user_table.update().where(user_table.c.id==user_id).values(profile_picture = file.filename)
    await database.execute(query)
    return {"message": "Profile picture uploaded successfully", "filename": file.filename}

