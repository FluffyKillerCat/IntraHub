from pydantic import BaseModel


class AdminCreate(BaseModel):

    org_id: int
    user_id: int

class AdminOut(BaseModel):

    user_id: int
    org_id: int
    to_be_accepted_by: str
    status: str

    class Config:

        orm_mode = True




