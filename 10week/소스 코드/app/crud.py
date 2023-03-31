import hashlib
import secrets

from sqlalchemy.orm import Session

from app import models, schemas


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).order_by(models.User.id.asc()).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    m = hashlib.sha256()
    salt = secrets.token_bytes(16).hex()
    m.update(user.password.encode('utf-8'))
    m.update(bytes.fromhex(salt))
    password = m.hexdigest()

    db_user = models.User(username=user.username, salt=salt, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def verify_user(db: Session, username: str, password: str):
    db_user = db.query(models.User).filter(models.User.username == username).first()

    m = hashlib.sha256()
    m.update(password.encode('utf-8'))
    m.update(bytes.fromhex(db_user.salt))
    password = m.hexdigest()
    if db_user.password != password:
        return None

    return db_user

# pasteuser 의 정보를 get 해주는 함수입니다.
# pastuser가 여러 user가 존재하므로 위의 get_users와 파라미터를 똑같이 설정해주었습니다.
# 또한 사용자별 메모를 열람하기 위해 사용자 이름이 필요하므로 username도 파라미터로 설정합니다.
def get_paste_users(db: Session, username: str):
    user_info = db.query(models.User).filter(models.User.username == username).first()
    # user의 info를 get_user 메소드를 불러와서 담아옵니다.
    if user_info:# user_info안에 paste.id와 일치하는 user.id가 있으면 그 paste를 반환합니다.
        # filter 함수는 일종의 조건문, Paste.owner_id와 user_info.id가 같은 paste를 모두(all) 불러옵니다.
        return db.query(models.Paste).filter(models.Paste.owner_id == user_info.id).all()
    else:
        return None

def get_pastes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Paste).order_by(models.Paste.id.asc()).offset(skip).limit(limit).all()

# 사용자별 메모 저장을 위한 함수입니다.
# 사용자 이름, 비밀번호로 사용자 인증 후 메모를 저장하기 때문에 파라미터들을 username, password를 추가해주었습니다.
def create_paste_memo(db: Session, username: str, password: str, paste: schemas.PasteCreate):
    # 검증하는 과정입니다. verify_user을 호출하여 제대로 검증이 됬다면 다음단계로 넘어가고, 검증이 되지 않았다면
    # None을 반환하여 오류 메시지를 나타냅니다.
    db_user = db.query(models.User).filter(models.User.username == username).first()

    m = hashlib.sha256()
    m.update(password.encode('utf-8'))
    m.update(bytes.fromhex(db_user.salt))
    password = m.hexdigest()
    if db_user.password != password:
        return None
    # 검증이 완료되었다면 메모저장을 시작합니다.
    memo = models.Paste(title=paste.title, content=paste.content, owner_id=db_user.id)
    db.add(memo)
    db.commit()
    db.refresh(memo)

    return memo
