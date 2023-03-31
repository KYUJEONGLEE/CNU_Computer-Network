from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

FLAGS = _ = None
DEBUG = False

def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    main()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail='username already registered')
    return crud.create_user(db=db, user=user)


@app.get('/users/', response_model=List[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get('/pastes/', response_model=List[schemas.Paste])
def get_pastes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    paste = crud.get_pastes(db, skip=skip, limit=limit)
    return paste

@app.get('/users/{username}', response_model=schemas.User)
def get_user(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


@app.get('/users/{username}/verify/', response_model=schemas.UserDetail)
def verify_user(username: str, password: str, db: Session = Depends(get_db)):
    db_user = crud.verify_user(db, username=username, password=password)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User authentication failed')
    return db_user

# 메모를 열람하는 함수입니다.
# crud.py에서 작성한 get_paste_users를 불러와 user의 정보를 가져오고 정보가 없으면 404를 반환, 정보가 존재하면 메모를 보여줍니다.
@app.get('/users/{username}/pastes/', response_model=schemas.List[schemas.Paste])
def get_paste_users(username: str, db: Session = Depends(get_db)):
    db_paste = crud.get_paste_users(db, username=username)
    if db_paste is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_paste



# 메모를 저장하는 함수입니다.
# 열람과 마찬가지로 crud.py에서 작성한 create_paste_memo를 불러와서 저장하고 이 때는 password 정보도 필요하기 때문에 파라미터로 넣어
# 줍니다. create_paste_memo 함수에서 검증이 완료되고 성공적으로 메모저장이 완료되었다면 paste를 반환하고, 실패하면 404를 반환합니다.
@app.post('/users/{username}/pastes/', response_model=schemas.Paste)
def create_paste_memo(username: str, password: str, paste: schemas.PasteCreate, db: Session = Depends(get_db)):
    db_paste = crud.create_paste_memo(db, username=username, password=password, paste=paste)
    if db_paste is None:
        raise HTTPException(status_code=404, detail='User authentication failed')
    return db_paste
