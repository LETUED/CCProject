# CI/CD 도구 (ci-cd-tool)

> 프로젝트를 분석해 CI/CD 파이프라인 설정·배포를 돕는 CLI(`cc`). 2024-2 캡스톤(8조).

## 무엇인가

`cc init`으로 프로젝트를 분석해 CI/CD 설정을 자동 생성하고, `cc ci` / `cc cd`로 파이프라인을 관리하는 명령줄 도구다.

## 구성 (명령어)

실제 등록된 명령 그룹은 5개다 (`cc <그룹> --help`로 옵션 확인):

```
cc init                              프로젝트 분석 및 CI/CD 자동 설정 (--force)
cc ci    build | test | status       CI 파이프라인
cc cd    deploy | rollback | status | list | push | init    CD 파이프라인
cc config init | show                설정
cc src   init | add | commit | status | push                소스 관리
```

전체 설계 명세(계획된 명령 포함)는 [docs/기능명세서.docx](docs/기능명세서.docx) 참고 — 일부 명령은 명세에만 있고 아직 구현되지 않았다.

## 실행

> PyPI 배포본(0.3.2)은 패키징 버그로 설치 시 import가 실패한다. 현재는 소스에서 설치할 것.

```bash
git clone https://github.com/LETUED/CCProject.git
cd CCProject
pip install -e .

cc init
cc config show
cc ci test
cc cd deploy --env prod --version 1.0.0
cc cd rollback --version 0.9.0
```

## 상태

캡스톤 제출 완료 (46커밋, GitHub Actions CI, PyPI 배포 스크립트, Release v1.3.0). PyPI 배포본은 0.3.2에서 패키징 버그로 깨져 있어 재배포 예정이며, 그전까지는 소스 설치를 권장한다.
