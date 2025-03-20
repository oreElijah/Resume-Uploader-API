from typing import Optional
from pydantic import BaseModel

class ResumeIn(BaseModel):
    """ResumeIn model definition"""
    job_post: str
    file_path:  str

class Resume(ResumeIn):
    """Resume model definition"""
    id: Optional[int] = None