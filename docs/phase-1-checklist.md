# BuildLog Phase 1 진행 점검표

## 1. 현재 상태

- 상태: 진행 중 — Supabase 실연결 확인 대기
- 작업일: 2026-10-26
- 완료된 범위: React, FastAPI, SQLite3 테스트, 환경 설정, Alembic, 로컬 연결 검증
- 남은 범위: 실제 Supabase 데이터베이스 연결 확인

## 2. 개발 환경 확인

- [x] Node.js 24.22.1 확인
- [x] npm 11.19.1 확인
- [x] Python 3.13.14 확인
- [x] PowerShell에서 `npm.ps1` 대신 `npm.cmd` 사용
- [x] 시스템 실행 정책은 변경하지 않음

## 3. 프론트엔드

- [x] `frontend`에 React + Vite 프로젝트 구성
- [x] React Router 기본 경로 구성
- [x] `VITE_API_BASE_URL` 환경 설정 추가
- [x] BuildLog 기본 연결 확인 화면 작성
- [x] FastAPI 상태를 화면에서 확인하는 요청 연결
- [x] 모바일 크기에서도 깨지지 않는 기본 화면 작성
- [x] 실행 방법을 `frontend/README.md`에 기록
- [x] npm 보안 검사에서 발견된 취약점 0개
- [x] 프론트엔드 코드 검사 통과
- [x] 프론트엔드 배포 빌드 통과

## 4. 백엔드

- [x] `backend`에 FastAPI 프로젝트 구조 구성
- [x] `/api/health` 상태 확인 API 작성
- [x] `/api/health/database` 데이터베이스 상태 확인 API 작성
- [x] React 개발 주소의 CORS 연결 허용
- [x] 환경 설정을 `.env`에서 읽는 구조 작성
- [x] 사용자용 오류와 예상하지 못한 오류의 공통 처리 틀 작성
- [x] Supabase 연결용 psycopg 드라이버 설치
- [x] 실행 방법을 `backend/README.md`에 기록
- [x] Python 코드 검사 통과

## 5. 데이터베이스와 테스트

- [x] 개발 기본값으로 로컬 SQLite3 연결 가능
- [x] 자동 테스트에서 메모리 SQLite3만 사용
- [x] 테스트 시작 전에 운영 DB 환경 설정을 SQLite3로 덮어씀
- [x] Supabase 연결 정보가 없어도 테스트 실행 가능
- [x] Alembic 데이터 변경 이력 폴더 구성
- [x] Alembic이 환경 설정의 데이터베이스 주소를 사용하도록 연결
- [x] 데이터베이스 설계 폴더 안내 문서 작성
- [ ] 실제 Supabase 연결 문자열로 상태 확인 API 검증

## 6. 환경 설정과 비밀값

- [x] `frontend/.env.example` 작성
- [x] `backend/.env.example` 작성
- [x] `.env`와 `.env.*`는 제외하고 `.env.example`은 기록 가능
- [x] `.venv`, `node_modules`, 빌드 결과와 로컬 DB 파일 제외
- [x] 실제 비밀번호나 연결 문자열을 코드와 문서에 기록하지 않음

## 7. 검증 결과

| 검증 | 결과 |
| --- | --- |
| 백엔드 Ruff 코드 검사 | 통과 |
| FastAPI 상태 API 테스트 | 통과 |
| SQLite3 상태 API 테스트 | 통과 |
| 백엔드 pytest | 4개 통과 |
| Alembic SQLite3 연결 | 통과 |
| 프론트엔드 oxlint | 통과 |
| 프론트엔드 Vite 빌드 | 통과 |
| React 개발 서버 HTTP 응답 | 200 OK |
| FastAPI 개발 서버 HTTP 응답 | 200 OK |
| SQLite3 상태 HTTP 응답 | 200 OK |
| React 주소에 대한 CORS 응답 | 허용 확인 |
| 실제 Supabase 연결 | 사용자 설정 대기 |

테스트 실행 시 FastAPI 테스트 도구의 향후 변경을 알리는 경고가 1건 표시되지만, 테스트 실패나 현재 기능 오류는 아닙니다.

## 8. 사용자가 해야 할 작업

Phase 1을 완전히 끝내려면 Supabase 프로젝트의 데이터베이스 연결 문자열이 필요합니다.

1. Supabase에서 BuildLog용 프로젝트를 만듭니다.
2. 프로젝트의 PostgreSQL 데이터베이스 연결 문자열을 확인합니다.
3. `backend/.env.example`을 참고해 `backend/.env` 파일을 만듭니다.
4. `DATABASE_URL`에 Supabase 연결 문자열을 입력합니다.
5. 비밀번호에 URL에서 특별한 의미를 가진 문자가 있다면 연결 문자열에 맞게 변환된 값을 사용합니다.

연결 문자열에는 비밀번호가 포함되므로 채팅, `docs` 문서나 `.env.example`에 붙여 넣지 않습니다. `backend/.env`에 직접 저장한 뒤 완료했다고 알려주면 실제 연결을 검증할 수 있습니다.

## 9. Phase 1 완료 조건

- [x] React가 실행됨
- [x] FastAPI가 실행됨
- [x] React에서 FastAPI로 요청할 수 있음
- [x] SQLite3 기반 자동 테스트가 운영 DB와 분리됨
- [x] 환경 설정과 비밀값 저장 위치가 분리됨
- [x] 데이터 변경 이력 도구가 준비됨
- [ ] FastAPI에서 Supabase로 실제 연결됨

마지막 항목이 통과하면 Phase 1을 완료로 바꾸고 Phase 2로 진행합니다.
