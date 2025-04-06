import os
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from database.config import resume_table, database, user_table

from models.user import Role
from utils.security import get_current_user_id, role_required
from fastapi.responses import FileResponse

router = APIRouter(dependencies=[Depends(get_current_user_id)])

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

@router.post("download/{name}/{filename}", status_code=status.HTTP_200_OK, dependencies=[Depends(role_required(Role.hirer))])
async def download_resume(name: str, filename: str):
    query = user_table.select().where(user_table.c.last_name==name)
    result = await database.execute(query)
    if result:
        Upload_Dir = "resume_uploads"
        file_path = os.path.join(Upload_Dir, filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
        return FileResponse(path=file_path, filename=filename, media_type="application/pdf", status_code=status.HTTP_200_OK)