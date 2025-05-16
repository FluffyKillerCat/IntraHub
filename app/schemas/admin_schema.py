from pydantic import BaseModel


class AdminCreate(BaseModel):

    org_id: str
    user_id: str

class AdminOut(BaseModel):

    user_id: int
    org_id: str
    status: str

    class Config:

        orm_mode = True




