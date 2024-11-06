from fastapi import FastAPI
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated
from models import LoginModel
from fastapi.responses import JSONResponse
import traceback
from fastapi.middleware.cors import CORSMiddleware
from schemas import LoginSchema


origins = [
   "*"
]

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/create/")
def create_user(login: LoginModel, session: SessionDep) -> LoginModel:
    try:
        session.add(login)
        session.commit()
        session.refresh(login)
        return JSONResponse({"status": "success", "message": "User Successfully Created"}, status_code=201)
    except Exception as e:
        print("Traceback - ", traceback.print_exc())
        print("Error - ", e)
        return JSONResponse({"status": "failure", "message": "Internal Server Error"}, status_code=500)


@app.post("/login/")
async def login(login: LoginSchema, session: SessionDep):
    try:

        user = session.exec(select(LoginModel)).first()
 
        if not user.username == login.username:
            return JSONResponse({"status": "failure", "message": "Invalid Username"}, status_code=400)
        
        if user.password != login.password:
            return JSONResponse({"status": "failure", "message": "Invalid Password"}, status_code=400)
        
        return JSONResponse({"status": "success", "message": "Logged In Successfully!"}, status_code=400)
 

 
    except Exception as e:
        print("e", e)
        return JSONResponse({"status": "failure", "message": "Internal Server Error"}, status_code=500)

