from app import rag
import shutil
import os
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select
from app.models import User, UserCreate, UserLogin, Token
from app.auth import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from app.database import init_db, get_session
from sqlmodel import Session
from fastapi.middleware.cors import CORSMiddleware


# Initialize DB
init_db()

app = FastAPI()

# Allow your frontend origin
origins = [
    "http://localhost:5173",  # React dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],  # allow POST, GET, OPTIONS, etc.
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ------------------------
# Protected Route Example
# ------------------------
def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    username = payload.get("sub")
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}, you are authenticated!"}

@app.post("/upload")
def upload_file(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    user_id = current_user.username
    file_path = f"./uploads/{file.filename}"
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    rag.add_document(file_path, user_id=user_id)
    return {"message": "Document uploaded successfully."}

@app.get("/ask")
def ask(q: str, current_user: User = Depends(get_current_user)):
    user_id = current_user.username
    qa = rag.get_qa_chain(user_id=user_id)
    answer = qa.run(q)
    return {"question": q, "answer": answer}


# ------------------------
# Auth Endpoints
# ------------------------

@app.post("/signup", response_model=Token)
def signup(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    db_user = User(username=user.username, hashed_password=hash_password(user.password))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    access_token = create_access_token({"sub": db_user.username})
    refresh_token = create_refresh_token({"sub": db_user.username})
    return {"access_token": access_token, "refresh_token": refresh_token}

@app.post("/signin", response_model=Token)
def signin(user: UserLogin, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.username == user.username)).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token({"sub": db_user.username})
    refresh_token = create_refresh_token({"sub": db_user.username})
    return {"access_token": access_token, "refresh_token": refresh_token}

from fastapi import Body

@app.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str = Body(..., embed=True)):
    payload = decode_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    username = payload.get("sub")
    # ✅ issue a new access token
    new_access_token = create_access_token({"sub": username})
    # we can either reuse the refresh_token or rotate it (issue a new one)
    return {"access_token": new_access_token, "refresh_token": refresh_token}



