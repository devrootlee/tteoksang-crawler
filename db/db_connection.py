import psycopg2

def db_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="tteoksang",
        user="leeroot",
        password=""  # 환경 변수로 대체 권장
    )