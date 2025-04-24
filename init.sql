-- # init.sql
-- # 도커 컨테이너 서버 실행 시 DB 및 Table 생성하는 스크립트
-- # 아바타 캐릭터 전처리한 데이터를 RDB에 넣기 위해 DB, Table을 생성

/* CREATE DB mlops */
CREATE DATABASE mlops;

/* SWITCH TO mlops DB */
\connect mlops

/* CREATE TABLE avatar_characters*/
CREATE TABLE IF NOT EXISTS avatar_characters (
    id SERIAL PRIMARY KEY,
    name TEXT,
    image TEXT,
    gender VARCHAR(20),
    eye_color VARCHAR(50),
    hair_color VARCHAR(100),
    skin_color VARCHAR(50)
);