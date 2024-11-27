# CI/CD 도구 사용 설명서

## 목차
1. [소개](#1-소개)
2. [설치 및 초기 설정](#2-설치-및-초기-설정)
3. [명령어 개요](#3-명령어-개요)
4. [주요 사용 시나리오](#4-주요-사용-시나리오)

## 1. 소개
이 문서는 CI/CD 도구의 사용법을 설명합니다. 이 도구는 개발자가 CI/CD 파이프라인을 쉽게 설정하고 관리할 수 있도록 돕습니다.

## 2. 설치 및 초기 설정

### 설치
```bash
pip install ci-cd-tool
```

### 초기화
프로젝트를 초기화하여 기본 설정을 생성합니다.
```bash
cc init
```
**옵션:**
- `--force`: 기존 설정을 덮어쓰기

## 3. 명령어 개요

### 기본 명령어 구조
```python:src/ci_cd_tool/cli.py
startLine: 5
endLine: 14
```

### 사용 가능한 주요 명령어 목록

1. **초기화 명령어**
   ```bash
   cc init [OPTIONS]
   ```

2. **CI 관련 명령어** (ci_group)
   ```bash
   cc ci build     # 빌드 실행
   cc ci test      # 테스트 실행
   cc ci status    # CI 파이프라인 상태 확인
   ```

3. **CD 관련 명령어** (cd_group)
   ```bash
   cc cd deploy    # 배포 실행
   cc cd rollback  # 이전 버전으로 롤백
   cc cd status    # 배포 상태 확인
   cc cd list      # 버전 목록 확인
   ```

4. **설정 관련 명령어** (config_group)
   ```bash
   cc config show           # 현재 설정 표시
   cc config set KEY VALUE  # 설정 값 변경
   cc config reset          # 설정 초기화
   ```

## 4. 주요 사용 시나리오

### 새 프로젝트 설정
```bash
cc init
cc config show
cc ci test
```

### 배포 실행
```bash
cc ci build
cc cd deploy --env prod --version 1.0.0
cc cd status
```

### 문제 해결
```bash
cc cd status
cc cd rollback --version 0.9.0
cc cd status
```