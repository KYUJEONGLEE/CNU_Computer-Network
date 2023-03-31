import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

# POST : INSERT
# GET : SELECT
# PUT : UPDATE
# DELETE : DELETE

app = FastAPI()
conn = sqlite3.connect('answer.db', check_same_thread=False)
cur = conn.cursor()
# DB 파일을 열고 cursor 생성

cur.execute('''CREATE TABLE IF NOT EXISTS Paste (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 content TEXT);''')
# 불러온 DB에 Paste 라는 TABLE이 존재 하지 않으면 Paste 테이블 생성
# id : INTEGER, content : TEXT

conn.commit()
# 테이블의 변경내용을 DB에 commit하는 부분    . uvicorn을 종료해도 데이터가 사라지지 않음.

# Paste 테이블의 content column에 접근하기 위한 class, content는 str로 선언.
class Paste(BaseModel):
    content: str

# POST method
@app.post('/paste/')
def post_paste(paste: Paste):
    POST_SQL = '''INSERT INTO Paste(content) VALUES (?)'''
    # 테이블에 데이터를 삽입하기 위한 SQL 쿼리문

    res = cur.execute(POST_SQL, (paste.content,))
    # Cursor class의 sql 쿼리를 실행하는 함수(execute)
    # param 에는 위에서 작성한 POST_SQL과 FastAPI 에서 content = "..." 에 접근하기 위해 paste.content로 선언.

    print("DATA INSERT, ID:", cur.lastrowid)
    # 입력한 content data에 접근하기 위한 paste_id를 알기 위해 출력문으로 작성.
    # cursor class의 lastrowid() 함수로 마지막으로 입력된 row의 번호가 출력.
    cur.fetchone()
    conn.commit()
    # commit로 변경사항 저장.

    return {'paste_id': cur.lastrowid,
            'paste': paste.content}

# GET method
@app.get('/paste/{paste_id}')
def get_paste(paste_id: int):
    GET_SQL = '''SELECT id, content FROM Paste WHERE id = ?'''
    # 테이블의 데이터 조회 SQL 쿼리문

    res = cur.execute(GET_SQL, (paste_id,))
    # execute로 sql 문장 실행, 조회하고자 하는 paste_id로 접근
    data = res.fetchone()

    # 단지 테이블을 조회 하는것 뿐이기에 commit는 할 필요없음.
    if data is not None:
        paste = Paste(content=data[1])
        return {'paste_id': data[0],
                'paste': paste}
    else:
        return {'paste_id': paste_id,
                'paste': None}

# PUT method
@app.put('/paste/{paste_id}')
def put_paste(paste_id: int, paste: Paste):
    PUT_SQL = '''UPDATE Paste SET content = ? WHERE id = ?'''
    res = cur.execute(PUT_SQL, (paste.content, paste_id))
    # UPDATE 하고자 하는 변수 : paste.content, id = paste_id 로 접근
    res.fetchone()
    conn.commit()

    return {'paste_id': paste_id,
            'paste': None}

# DELETE method
@app.delete('/paste/{paste_id}')
def delete_paste(paste_id: int):
    DELETE_SQL = '''DELETE FROM Paste WHERE id = ?'''
    res = cur.execute(DELETE_SQL, (paste_id,))
    # DELETE : 입력한 paste_id 삭제
    res.fetchone()
    conn.commit()

    return {'paste_id': paste_id,
            'paste': None}