#현재 코드베이스에서 사용 가능한 명령어 목록을 분석해보겠습니다.

### 기본 명령어 구조
```python:src/ci_cd_tool/cli.py
@click.group()
@click.version_option(version="0.2.6")
def main():
    """CI/CD 도구 CLI"""
    setup_logging()

main.add_command(init)
main.add_command(ci_group)
main.add_command(cd_group)
main.add_command(config_group)
```

### 사용 가능한 주요 명령어 목록

1. **초기화 명령어**
```bash
cc init [OPTIONS]
```

2. **CI 관련 명령어** (ci_group)
```bash
cc ci create     # CI 파이프라인 생성
cc ci status     # CI 파이프라인 상태 확인
cc ci list       # CI 파이프라인 목록 조회
cc ci validate   # CI 설정 유효성 검사
```

3. **CD 관련 명령어** (cd_group)
```bash
cc cd deploy     # 배포 실행
cc cd rollback   # 이전 버전으로 롤백
cc cd status     # 배포 상태 확인
cc cd config     # 배포 설정 관리
```

4. **설정 관련 명령어** (config_group)
```bash
cc config show           # 현재 설정 표시
cc config set KEY VALUE  # 설정 값 변경
cc config reset         # 설정 초기화
```

### 명령어 사용 예시

1. **프로젝트 초기화**
```bash
# 새 프로젝트 초기화
cc init
```

2. **CI 파이프라인 관리**
```bash
# CI 파이프라인 생성
cc ci create --provider github

# 파이프라인 상태 확인
cc ci status
```

3. **배포 관리**
```bash
# 배포 실행
cc cd deploy --env production

# 배포 상태 확인
cc cd status
```

4. **설정 관리**
```bash
# 현재 설정 확인
cc config show

# 설정 값 변경
cc config set ci_provider github

# 설정 초기화
cc config reset
```

### 공통 옵션
모든 명령어에서 사용 가능한 옵션들:
```bash
--help          # 도움말 표시
```

### 참고사항
1. 모든 명령어는 `cc` 접두어로 시작
2. 각 명령어의 상세 도움말은 `cc [command] --help`로 확인 가능
3. 설정 파일은 `.cc/config.yml`에 저장됨
4. 로그는 `logs/ci_cd_tool.log`에 기록됨