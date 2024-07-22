# Board Service Backend with FastAPI

FastAPI 기반 게시판 서비스 Backend 서버  

## Requirements

- Python 3.11
    - check `requirements` directory for third-party packages
- MariaDB 11.1
- Redis 6.2
- Grafana
- Prometheus
- ELK

## Memo

- commends for running FastAPI dev server

```powershell
fastapi dev main.py
```

- commends for running uvicorn server for debugging

```powershell
main.py
```

## Migration with Alembic

- initialize alembic

```powershell
alembic init migrations
```

- create revision

```powershell
alembic revision --autogenerate
```

- run migration to latest revision

```powershell
alembic upgrade head
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