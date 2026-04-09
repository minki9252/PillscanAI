from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from datetime import datetime
import uvicorn

app = FastAPI(title="스마트팩토리 알약 검수 서버")

# --- 데이터 모델 정의 ---
class PillLog(BaseModel):
    line_id: str = "Line_A_Minki" # 기본값 설정
    pill_name: str
    company: str
    status: str = "정상"

# --- 데이터베이스 초기화 ---
def init_db():
    conn = sqlite3.connect('pill_factory.db')
    c = conn.cursor()
    # [상세주석] status 컬럼이 포함된 테이블 생성
    c.execute('''CREATE TABLE IF NOT EXISTS pill_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  line_id TEXT,
                  pill_name TEXT,
                  company TEXT,
                  status TEXT,
                  timestamp TEXT)''')
    conn.commit()
    conn.close()

@app.on_event("startup")
def startup_event():
    init_db() # 서버 시작 시 DB 초기화

@app.get("/")
def read_root():
    return {"message": "서버가 정상 작동 중입니다."}

# --- 알약 로그 저장 API 엔드포인트 ---
@app.post("/log")
async def log_pill(data: PillLog):
    time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        conn = sqlite3.connect('pill_factory.db')
        c = conn.cursor()
        # [상세주석] 전달받은 4개 데이터 + 시간 정보를 DB에 삽입
        c.execute("INSERT INTO pill_logs (line_id, pill_name, company, status, timestamp) VALUES (?, ?, ?, ?, ?)",
                  (data.line_id, data.pill_name, data.company, data.status, time_str))
        conn.commit()
        conn.close()
        
        print(f"[*] DB 저장 성공: {data.pill_name} ({data.status})")
        return {"status": "success", "pill": data.pill_name}
    except Exception as e:
        print(f"[*] DB 에러: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)