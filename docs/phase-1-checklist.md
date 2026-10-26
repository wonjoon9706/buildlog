# BuildLog Phase 1 완료 점검표

## 1. 현재 상태

- 상태: 완료 — SQLite3 기준
- 완료일: 2026-10-26
- 구성: React, FastAPI, 개발용 SQLite3, 테스트용 메모리 SQLite3, Alembic

Supabase 연동은 관련 수업을 진행한 뒤 별도 단계에서 검토합니다.

## 2. 완료한 작업

- [x] React + Vite 프로젝트 구성
- [x] React Router 기본 경로 구성
- [x] FastAPI 프로젝트 구성
- [x] 환경 설정과 `.env.example` 구성
- [x] React와 FastAPI 연결 및 CORS 확인
- [x] 개발용 SQLite3 연결
- [x] 테스트용 메모리 SQLite3 분리
- [x] Alembic 변경 이력 구조 구성
- [x] 공통 오류 처리 틀 구성
- [x] 프론트엔드와 백엔드 실행 방법 기록
- [x] 실제 비밀값을 코드와 문서에 넣지 않음

## 3. 검증 결과

- [x] FastAPI 상태 API 200 응답
- [x] SQLite3 상태 API 200 응답
- [x] React 개발 서버 200 응답
- [x] React 주소에 대한 CORS 허용
- [x] 백엔드 코드 검사 통과
- [x] 프론트엔드 코드 검사 통과
- [x] 프론트엔드 배포 빌드 통과

## 4. 다음 할 일

Phase 2에서 사용자와 기록 데이터 구조, 공통 입력 규칙과 소유자 권한 검사를 구현합니다.
