from pydantic import BaseModel, Field, EmailStr, ConfigDict


config = ConfigDict(from_attributes=True)


class UserSchema(BaseModel):
    model_config = config
    login: str = Field(title="User's login",
                       description="User's login")
    email: EmailStr = Field(title="User's email",
                            description="User's email")
    password: str = Field(title="User's password",
                          description="User's password")


class UserResponse(BaseModel):
    id: str = Field(title="User's id",
                    description="User's id")
    login: str = Field(title="User's login",
                       description="User's login")
    email: EmailStr = Field(title="User's email",
                            description="User's email")
    password: str = Field(title="User's password",
                          description="User's password")
    access_token: str = Field(title="User’s token",
                              description="User’s token")


class TokenResponse(BaseModel):
    access_token: str = Field(title="User’s access token",
                              description="User’s access token")
    token_type: str = Field(title="User’s token type",
                            description="User’s token type")


class UserLogin(BaseModel):
    model_config = config
    email: EmailStr = Field(title="User’s email",
                            description="User’s email")
    password: str = Field(title="User’s password",
                          description="User’s password")
