# backend/main.py

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
LIFF_ID = os.getenv("LIFF_ID")


# 1. try to fetch DATABASE_URL from PATH (on cloud)
# use local sqlite is not possible
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # fix Render response URL bug (postgres:// -> postgresql://)
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URL = DATABASE_URL
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./lending.db"

# 2. create Engine 
connect_args = {}
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    connect_args = {"check_same_thread": False}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# 2. data model
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)      # LINE User ID
    container_id = Column(String, index=True) # 容器/NFC ID
    borrow_time = Column(DateTime, default=datetime.now)
    return_time = Column(DateTime, nullable=True)
    status = Column(String, default="BORROWED") # BORROWED, RETURNED

# db init
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # change these into real urls
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. get frontend file
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
templates = Jinja2Templates(directory=frontend_dir)
# 2. mount static file (pic assets etc for beautiful UI...) 
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/liff")
async def read_index(request: Request): #  request parameter
    # ¥pass liff_id to HTML
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "liff_id": LIFF_ID  # pass ID to front end
    })

# get db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 4. define structure for response
class BorrowRequest(BaseModel):
    lineUserId: str
    containerId: str

# 5. borrow API:
@app.post("/api/borrow")
def borrow_container(req: BorrowRequest, db: Session = Depends(get_db)):
    # check if txn is alive(not returned yet)
    active_txn = db.query(Transaction).filter(
        Transaction.container_id == req.containerId,
        Transaction.status == "BORROWED"
    ).first()
    
    if active_txn:# check if txn is alive(not returned yet)
        raise HTTPException(status_code=400, detail="This container has been borrowed")

    # create a db record
    new_txn = Transaction(
        user_id=req.lineUserId,
        container_id=req.containerId
    )
    db.add(new_txn)
    db.commit()
    db.refresh(new_txn)
    
    print(f"user {req.lineUserId} borrowed container No. {req.containerId}")
    return {"status": "success", "message": f"{req.containerId} borrowed successfully", "time": new_txn.borrow_time}

# request strcure for return message
class ReturnRequest(BaseModel):
    containerId: str

# reset API: for demo
@app.post("/api/reset")
def reset_container(req: ReturnRequest, db: Session = Depends(get_db)):
    # check active txn (not returned yet container)
    active_txn = db.query(Transaction).filter(
        Transaction.container_id == req.containerId,
        Transaction.status == "BORROWED"
    ).first()
    
    if active_txn:
        active_txn.status = "RETURNED"
        active_txn.return_time = datetime.now()
        db.commit()
        return {"status": "success", "message": f"Container {req.containerId} returned, you can borrow it now!"}
    
    return {"status": "info", "message": "This container is not borrowed"}