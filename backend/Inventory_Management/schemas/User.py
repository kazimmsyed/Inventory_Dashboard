from typing import Optional
from pydantic import BaseModel, Field
from models.Inventory import User

"""
CREATE TABLE users (
	user_id INTEGER NOT NULL, 
	email VARCHAR(30) NOT NULL, 
	username VARCHAR(20) NOT NULL, 
	last_name VARCHAR(30) NOT NULL, 
	first_name VARCHAR(30) NOT NULL, 
	hashed_password VARCHAR(20) NOT NULL, 
	is_active BOOLEAN NOT NULL, 
	role VARCHAR(15), 
	PRIMARY KEY (user_id), 
	UNIQUE (email)
);

"""

class UserRequest(BaseModel):
    user_id: Optional[int] = None
    email:str=Field(unique=True,nullable=False,min_length=8)
    username:str=Field(unique=True,nullable=False,min_length=4)
    last_name:str=Field(nullable=False,min_length=4)
    first_name:str=Field(nullable=False,min_length=4)
    hashed_password:str=Field(nullable=False,max_length=100)
    is_active:bool=Field(nullable=False,default=True)
    role:str=Field(nullable=False,default=None)

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "kazimmsyed9911",
                "username": "kazimmsyed",
                "first_name": "kazim",
                "last_name": "syed",
                "is_active": True
            }
        }
    }





class UserBuilder:
    def __init__(self):
        self.user = User()

    def set_identity(self, email: str, username: str):
        self.user.email = email
        self.user.username = username
        return self

    def set_name(self, first_name: str, last_name: str):
        self.user.first_name = first_name
        self.user.last_name = last_name
        return self

    def set_password(self, plain_password: str):
        # Here is where the "heavy lifting" happens.
        # You would use a library like passlib or bcrypt here.
        # For now, we simulate the hashing.
        self.user.hashed_password = plain_password
        return self

    def set_role(self, role: str = "user"):
        self.user.role = role
        return self

    def build(self):
        # Validation Logic
        if "@" not in self.user.email:
            raise ValueError("Invalid email format")
        if len(self.user.username) < 4:
            raise ValueError("Username too short")

        return self.user

class Token(BaseModel):
    access_token: str
    token_type: str