from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


class LoginModel(SQLModel, table=True):
    username: str | None = Field(default=None, primary_key=True, unique=True)
    password: str 