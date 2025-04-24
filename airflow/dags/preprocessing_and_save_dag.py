# preprocessing_and_save_dag.py 수정

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# 기본 설정 정의
default_args = {
    "owner": "airflow",  # DAG 소유자
    "start_date": datetime(2024, 4, 16),  # DAG 실행 시작 날짜
    "retries": 1,  # 실패 시 재시도 횟수
    "retry_delay": timedelta(minutes=5),  # 재시도 간격 (5분 후 재시도)
}

# DAG 정의 (with 블록 내부에서 task들을 정의함)
with DAG(
    dag_id="avatar_character_preprocessing",  # DAG 이름 (고유 식별자)
    default_args=default_args,  # 기본 인자 전달
    schedule_interval="* * * * *",  # 실행 주기: 매 1분마다 실행
    catchup=False, 
    tags=["preprocessing"],  # Airflow UI에서 DAG 구분용 태그
    is_paused_upon_creation=False, 
) as dag:

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # preprocessing.py 실행
    run_preprocessing = BashOperator(
        task_id="run_avatar_preprocessing",  # task의 이름 (UI에서 식별용)
        bash_command="python /opt/airflow/scripts/preprocessing.py '{{ execution_date.strftime('%Y%m%d_%H%M%S') }}'",  # 실제 실행할 bash 명령어
    )

    # preprocessing.py 실행 >> save_file.py 실행
    run_save_file = BashOperator(
        task_id="run_save_file",  # task의 이름 (UI에서 식별용)
        bash_command="python /opt/airflow/scripts/save_file.py '{{ execution_date.strftime('%Y%m%d_%H%M%S') }}'",  # 실제 실행할 bash 명령어
    )

    # preprocessing.py 실행 >> save_rdb.py 실행
    run_save_rdb = BashOperator(
        task_id="run_save_rdb",  # task의 이름 (UI에서 식별용)
        bash_command="python /opt/airflow/scripts/save_rdb.py '{{ execution_date.strftime('%Y%m%d_%H%M%S') }}'",  # 실제 실행할 bash 명령어
    )

    # run_preprocessing이 끝난 후 run_save_file과 run_save_rdb 실행
    run_preprocessing >> [run_save_file, run_save_rdb] 
