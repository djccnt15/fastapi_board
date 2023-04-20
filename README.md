# study_fastapi

[study_svelte 저장소](https://github.com/djccnt15/study_svelte)의 Backend

## memo

FastAPI의 개발용 서버 구동 명령어는 아래와 같다.  

```powershell
> uvicorn main:app --reload
```

## configuration 관련

- `config.ini` 파일을 통해 각종 환경 설정 제어
- `DEFAULT` 섹션의 `mode`는 개발과 운용의 차이가 있는 환경에서 설정을 관리하기 위해 사용
- `CORSLIST` 섹션은 CORS 목록 관리용 섹션
- 비밀번호 등 외부 저장소에 저장해서는 안 되는 정보는 `keys.json`으로 별도 관리

```json
{
    "db": {
        "dev": {
            "drivername": "sqlite",
            "database": "./sql_app.db"
        }
    }
}
```