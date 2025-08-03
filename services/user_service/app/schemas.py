# services/user_services/app/schemas.py

from sqlmodel import SQLModel, Field

# This is a base model that contains shared fields that
# are present in both creating a user and showing a user's public info.
class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: str = Field(unique=True, index=True)


# This is the schema we will use when a user signs up.
# It has all the base fields plus the password.
class UserCreate(UserBase):
    password: str


# This is the schema we will use when we return a user's data from our API.
# It has the base fields plus the database-generated ID.
# Notice it does NOT include the password for security.
class UserPublic(UserBase):
    id: int