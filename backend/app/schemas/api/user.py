from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    username: str | None = None


class UserResponse(UserBase):
    pass


class UserCreate(UserBase):
    model_config = ConfigDict(from_attributes=True)
    password: str


class UserSchema(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
