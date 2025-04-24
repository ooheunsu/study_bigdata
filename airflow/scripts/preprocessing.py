import requests
import pandas as pd
import ast
import sys
import os
from datetime import datetime

# 1. API 호출 - 아바타 캐릭터 데이터
url = "https://api.sampleapis.com/avatar/characters"
response = requests.get(url)
data = response.json()

df = pd.DataFrame(data)


# 2. physicalDescription 컬럼 딕셔너리로 정보들 개별 칼럼으로 분리
df["physicalDescription"] = df["physicalDescription"].apply(
    lambda x: ast.literal_eval(x) if isinstance(x, str) else x
)
desc_df = df["physicalDescription"].apply(pd.Series)
df = pd.concat(
    [
        df.drop(
            columns=[
                "id",
                "bio",
                "physicalDescription",
                "personalInformation",
                "politicalInformation",
                "chronologicalInformation",
            ]
        ),
        desc_df,
    ],
    axis=1,
)

df = df.rename(
    columns={
        "eyeColor": "eye_color",
        "hairColor": "hair_color",
        "skinColor": "skin_color",
    }
)

# 3. 전처리한 파일 저장

#  파일명용 timestamp
timestamp = (
    sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y%m%d_%H%M%S")
)
# 폴더명용 날짜 (예: 20250421)
date_folder = datetime.now().strftime("%Y_%m%d")

# 기본 저장 경로 설정
base_path = os.path.abspath(os.path.join(os.getcwd(), "datas"))  # 로컬 기본값

# 도커 환경이라면 경로 변경
if os.path.exists("/opt/airflow/datas"):
    base_path = "/opt/airflow/datas"

# 날짜별 폴더 경로 생성
save_path = os.path.join(base_path, date_folder)
os.makedirs(save_path, exist_ok=True)

# 최종 파일 경로
file_path = os.path.join(save_path, f"avatar_characters_{timestamp}.csv")

# 저장
df.to_csv(file_path, index=False)
print(f"✅ CSV 저장 완료: {file_path}")
