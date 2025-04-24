# entrypoint.sh
# Docker 서버 실행 시 Airflow 실행을 위한 커맨드 파일입니다.

echo "⏳ Waiting for PostgreSQL at postgres:5432..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "✅ PostgreSQL is up - continuing..."

airflow db init

airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com || true

exec airflow "$@"