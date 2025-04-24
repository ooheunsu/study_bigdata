import boto3
import os
import sys
from datetime import datetime

# S3 업로드
# S3 스토리지 이름 정의
bucket_name = "hk-mlops-storage-1"

# AWS S3 클라이언트 생성
s3 = boto3.client("s3", region_name="ap-northeast-2")

# S3에 파일 업로드
try:
    # 현재 날짜와 시간으로 파일 이름 생성
    timestamp = (
        sys.argv[1] if len(sys.argv) > 1 else datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    date_folder = datetime.now().strftime("%Y_%m%d")

    # 기본 저장 경로 설정
    default_path = os.path.abspath(
        os.path.join(os.getcwd(), f"datas/{date_folder}")
    )  # 로컬 기본값

    # 도커 환경이라면 /opt/airflow 경로가 존재함
    if os.path.exists(f"/opt/airflow/datas/{date_folder}"):
        default_path = f"/opt/airflow/datas/{date_folder}"

    # 디렉토리 없으면 생성
    os.makedirs(default_path, exist_ok=True)

    # 최종 저장 경로
    file_path = os.path.join(default_path, f"avatar_characters_{timestamp}.csv")

    file_name = f"test/{date_folder}/avatar_characters_{timestamp}.csv"

    # S3에 파일 업로드
    s3.upload_file(
        file_path, bucket_name, file_name
    )  # 저장할 파일명, S3 버킷명, 저장할 폴더 경로
    print(f"✅ S3 업로드 완료: s3://{bucket_name}/{file_name}")
except Exception as e:
    print(f"❌ S3 업로드 실패: {e}")
