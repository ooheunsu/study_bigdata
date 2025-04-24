# save_rdb.py

from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy import inspect
from sqlalchemy import text
import sys
from datetime import datetime
import os

############## 업로드할 파일 경로 설정 ###############

# 현재 날짜와 시간
timestamp = (
    sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y%m%d_%H%M%S")
)
date_folder = datetime.now().strftime("%Y_%m%d")

# 기본 저장 경로 설정
default_path = os.path.abspath(
    os.path.join(os.getcwd(), f"datas/{date_folder}")
)  # 로컬 기본값

# 도커 환경이라면 /opt/airflow 경로가 존재함
if os.path.exists("/opt/airflow/datas"):
    default_path = f"/opt/airflow/datas/{date_folder}"

# 디렉토리 없으면 생성
os.makedirs(default_path, exist_ok=True)

# 최종 저장 경로
file_path = os.path.join(default_path, f"avatar_characters_{timestamp}.csv")

df = pd.read_csv(file_path, low_memory=False)


############## DB 연결 ###############

# 1. 연결 정보 설정
pg_user = "airflow"
pg_pass = "airflow"
pg_host = "postgres" # 도커 환경에서는 'postgres'로 설정
pg_port = "5432"
pg_db   = "mlops"
db_url  = f"postgresql+psycopg2://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"

# 2. SQLAlchemy 엔진 생성 
engine = create_engine(db_url)

# 3. DB 연결 테스트
try:
    with engine.connect() as conn:
        print("✅ DB 연결 성공")
except Exception as e:
    print(f"❌ DB 연결 실패: {e}")

# 4. 테이블 존재 확인
inspector = inspect(engine)
if "avatar_characters" in inspector.get_table_names():
    print("✅ 테이블 'avatar_characters' 존재함")
else:
    print("❌ 테이블 없음")


############## DB 데이터 삽입 ###############

# 넣을 컬럼만 추출
columns = ["name", "image", "gender", "eye_color", "hair_color", "skin_color"]

# INSERT 쿼리 문자열
insert_query = text(
    f"""
        INSERT INTO avatar_characters (name, image, gender, eye_color, hair_color, skin_color)
        VALUES (:name, :image, :gender, :eye_color, :hair_color, :skin_color)
    """
)

# DB 연결 후 데이터 삽입
with engine.begin() as conn:
    for _, row in df[columns].iterrows():
        conn.execute(insert_query, {
            "name": row["name"],
            "image": row["image"],
            "gender": row["gender"],
            "eye_color": row["eye_color"],
            "hair_color": row["hair_color"],
            "skin_color": row["skin_color"],
        })

print("✅ 데이터 삽입 완료")
