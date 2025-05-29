from sqlmodel import SQLModel, Field, Column
import uuid
import sqlalchemy.dialects.postgresql as pg
from sqlalchemy.dialects.postgresql import TIMESTAMP

from datetime import datetime,timezone

class User(SQLModel, table = True):
    __tablename__ = 'users'
    uid:uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    username:str
    email:str
    first_name:str
    last_name:str
    is_verified:bool= Field(default=False)
    hash_password:str = Field(exclude=True)
    created_at: datetime = Field(
    sa_column=Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
)
    updated_at: datetime = Field(
    sa_column=Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
)
    
def __repr__(self):
    return f"<User {self.username}>"