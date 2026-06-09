from pydantic import BaseModel, field_validator
from typing import List, Optional, Literal

class JobPosting(BaseModel):
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[Literal["full-time", "part-time", "contract", "internship"]] = None
    #employment_type: Optional[str] = None   # e.g. "full-time"
    salary_min: Optional[int] = None         # 130000
    salary_max: Optional[int] = None         # 160000
    remote: bool
    skills: List[str]
    experience_years: Optional[int] = None   # 5
    @field_validator("employment_type", mode="before")
    @classmethod
    def normalize_employment_type(cls, v):
        if isinstance(v, str):
            return v.lower().strip()
        return v