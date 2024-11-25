네, 테스트 환경 자동 감지 기능에 대한 문서를 작성하겠습니다.

```markdown:docs/test_environment.md
# 테스트 환경 자동 감지

## 개요
테스트 실행 시 현재 Git 브랜치를 기반으로 테스트 환경을 자동으로 감지하는 기능입니다.

## 동작 방식

### 1. 환경 감지 우선순위
1. `--env` 옵션으로 직접 지정된 환경
2. config.yml의 environments 설정과 일치하는 브랜치
3. 기본 브랜치 매핑 규칙
4. 기본값 (staging)

### 2. 기본 브랜치 매핑 규칙
- `develop`, `development` → dev 환경
- `main`, `master` → prod 환경
- 그 외 브랜치 → staging 환경

### 3. 설정 방법
config.yml 파일에서 브랜치와 환경을 매핑할 수 있습니다:

```yaml
environments:
  dev:
    branch: "feature/dev"
  staging:
    branch: "release"
  prod:
    branch: "main"
```

## 사용 방법

### 1. 자동 감지 사용
```bash
cc test run
```

### 2. 특정 모듈 테스트 (자동 감지)
```bash
cc test run auth
```

### 3. 수동으로 환경 지정
```bash
cc test run --env prod
```

## 에러 처리
- Git 저장소가 아닌 경우: staging 환경으로 fallback
- 브랜치 감지 실패: staging 환경으로 fallback
- 설정 파일 로드 실패: 기본 매핑 규칙 사용

## 관련 코드
- TestManager._detect_environment(): 브랜치 감지 및 환경 매핑
```python:src/ci_cd_tool/services/test_manager.py
startLine: 67
endLine: 93
```

- test_commands.py의 run 명령어: CLI 인터페이스
```python:src/ci_cd_tool/commands/test_commands.py
startLine: 14
endLine: 27
```

## 주의사항
1. Git 저장소 초기화가 필요합니다.
2. config.yml 파일이 없어도 기본 매핑으로 동작합니다.
3. 환경 변수 TEST_ENV가 자동으로 설정됩니다.
```

이 문서는 다음 코드들을 참조했습니다:
- TestManager 클래스의 _detect_environment 메서드
- test_commands.py의 run 명령어 정의
- TestService 클래스의 run_tests 메서드