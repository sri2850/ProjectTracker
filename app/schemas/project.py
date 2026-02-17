from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str


class ProjectUpdate(BaseModel):
    name: str


class ProjectRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
