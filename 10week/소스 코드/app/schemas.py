from typing import List, Union

from pydantic import BaseModel


class PasteBase(BaseModel):
    # Paste 의 BaseModel을 설정하는 부분
    # model에서 추가한 title과 content를 str로 설정해줍니다.
    title: str
    content: str

class PasteCreate(PasteBase):
    # PasteCreate, 즉 생성하는 부분입니다. BaseModel에서 따로 추가해줄 부분이 없기 때문에
    # PasteBase를 그대로 불러옵니다.
   pass

class Paste(PasteBase):
    id: int
    owner_id = int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    pastes: List[Paste] = []

    class Config:
        orm_mode = True

class UserDetail(User):
    salt: str

