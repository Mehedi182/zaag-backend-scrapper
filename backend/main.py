from datetime import timedelta

from auth import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
    get_user,
)
from config import settings
from crud import (
    create_sample_data,
    delete_sample_data,
    get_sample_data,
    get_samples,
    update_sample_data,
)
from database import Base, engine, get_db
from fastapi import Depends, FastAPI, HTTPException, status
from models import User
from schemas import (
    ScrapperDataCreate,
    ScrapperDataResponse,
    Token,
    UserCreate,
    UserLogin,
    UserResponse,
)
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/token", response_model=Token)
def login_for_access_token(
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@app.post("/samples/", response_model=ScrapperDataResponse)
def create_sample(
    sample: ScrapperDataCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return create_sample_data(db=db, sample_data=sample)


@app.get("/samples/", response_model=list[ScrapperDataResponse])
def read_samples(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    samples = get_samples(db)
    return samples


@app.get("/samples/{sample_id}", response_model=ScrapperDataResponse)
def read_sample(
    sample_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    db_sample = get_sample_data(db, sample_id=sample_id)
    if db_sample is None:
        raise HTTPException(status_code=404, detail="Sample not found")
    return db_sample


@app.put("/samples/{sample_id}", response_model=ScrapperDataResponse)
def update_sample(
    sample_id: int,
    sample: ScrapperDataCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    db_sample = update_sample_data(db, sample_id=sample_id, sample_data=sample)
    if db_sample is None:
        raise HTTPException(status_code=404, detail="Sample not found")
    return db_sample


@app.delete("/samples/{sample_id}", response_model=ScrapperDataResponse)
def delete_sample(
    sample_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    db_sample = delete_sample_data(db, sample_id=sample_id)
    if db_sample is None:
        raise HTTPException(status_code=404, detail="Sample not found")
    return db_sample
