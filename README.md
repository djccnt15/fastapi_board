# study_fastapi

[study_svelte 저장소](https://github.com/djccnt15/study_svelte)의 Backend

## memo

- FastAPI의 개발용 서버 구동 명령어

```powershell
uvicorn main:app --reload
```

## alembic 기반 migration 관련

- alembic 시작

```powershell
alembic init migrations
```

- revision 생성

```powershell
alembic revision --autogenerate
```

- 최신 리비전으로 migration 실행

```powershell
alembic upgrade head
```

## configuration 관련

- `config.ini`, `.env` 파일을 통해 각종 환경 설정 제어

```ini
# DEFAULT
mode = dev

# AUTH
token_expire_minutes = 0000
secret_key = ****
algorithm = ****
```

- 비밀번호 등 외부 저장소에 저장해서는 안 되는 정보는 `key.json`으로 별도 관리 + 암호화

```json
{
    "db": {
        "dev": {
            "drivername": "sqlite+aiosqlite",
            "database": "./sql_app.db"
        },
        "test": {
            "drivername": "mysql+aiomysql",
            "username": "root",
            "password": "****",
            "host": "host.docker.internal",
            "port": "3306",
            "database": "fastapi"
        }
    }
}
```

## Docker

- Dockerfile build

```
docker build -t fastboard .
```

- Docker container run

```
docker run -itd -p 8000:8000 --name fastboard fastboard
```