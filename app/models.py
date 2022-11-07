from sqlmodel import SQLModel, Field


class URLBase(SQLModel):
    target_url: str
    key: str = Field(default=None, unique=True)
    created_on: str
    is_active: bool


class URLInfo(URLBase, table=True):
    id: int = Field(default=None, primary_key=True)


class UserBase(SQLModel):
    email: str = Field(unique=True)
    password: str
    created_on: str
    is_active: bool
    is_super_admin: bool


class UserInfo(UserBase, table=True):
    id: int = Field(primary_key=True)


class URLTarget(SQLModel):
    target_url: str


class URLKey(SQLModel):
    key: str
