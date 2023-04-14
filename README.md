# study_fastapi

[study_svelte 저장소](https://github.com/djccnt15/study_svelte)의 Backend

## memo

FastAPI의 개발용 서버 구동 명령어는 아래와 같다.  

```powershell
> uvicorn main:app --reload
```

## configuration 관련

- `config.ini` 파일을 통해 각종 환경 설정 제어
- `DEFAULT` 섹션의 `mode`는 개발과 운용의 차이가 있는 환경에서 설정을 차별화하기 위해 사용
- `CORSLIST` 섹션은 CORS 목록 관리용 섹션