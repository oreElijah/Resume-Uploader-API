from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from database.config import resume_table, database

from models.user import Role
from utils.security import get_current_user, get_current_user_id, role_required

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get("/", status_code=status.HTTP_200_OK, dependencies=[Depends(role_required(Role.hirer))])
async def get_all_resumes():
    """only hirers can access this route"""
    query = resume_table.select()
    result = await database.fetch_all(query)
    return result

@router.post("/submit", status_code=status.HTTP_201_CREATED, dependencies=[Depends(role_required(Role.worker))])
async def submit_resume(job_post: str =Form(...),email: str =Form(...) ,file: UploadFile =File(...), user_id: int = Depends(get_current_user_id)):
    """Only workers can access this route"""
    with open(f"resume_uploads/{file.filename}", "wb") as f:
        f.write(await file.read())
    query = resume_table.insert().values(title=job_post, file_path=file.filename, email=email, user_id=user_id) 
    await database.execute(query)
    return {"message": "Resume submitted successfully",}