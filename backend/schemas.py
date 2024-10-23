from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str


class ScrapperDataBase(BaseModel):
    name: str
    tax_id: str
    gtdb_id: Optional[str] = None
    domain: Optional[str] = None
    abundance_score: Optional[float] = None
    relative_abundance: Optional[float] = None
    unique_matches: Optional[float] = None
    total_matches: Optional[float] = None
    unique_matches_frequency: Optional[float] = None
    reads_frequency: Optional[int] = None
    normalized_reads_frequency: Optional[int] = None
    go_id: Optional[str] = None
    go_category: Optional[str] = None
    go_description: Optional[str] = None
    copies_per_million: Optional[float] = None  # cpm
    enzyme_id: Optional[str] = None
    pfam_id: Optional[str] = None
    cazy_id: Optional[str] = None


class ScrapperDataCreate(ScrapperDataBase):
    pass


class ScrapperDataResponse(ScrapperDataBase):
    id: int

    class Config:
        orm_mode = True
