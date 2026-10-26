# BuildLog backend

BuildLog의 FastAPI 백엔드입니다. 현재 개발 데이터베이스는 SQLite3, 자동 테스트 데이터베이스는 별도의 메모리 SQLite3를 사용합니다. Supabase 연동은 관련 수업 이후 별도 단계에서 검토합니다.

## 처음 실행

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\alembic.exe upgrade head
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

기본 주소는 `http://localhost:8000`이며 상태 확인 주소는 다음과 같습니다.

- API: `http://localhost:8000/api/health`
- 데이터베이스: `http://localhost:8000/api/health/database`

## 테스트

```powershell
.\.venv\Scripts\python.exe -m pytest
```

실제 비밀값은 `.env`에만 저장합니다. 환경 변수 항목은 `.env.example`을 참고합니다.
