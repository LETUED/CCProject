#!/bin/bash

# 1. pyproject.toml 파일이 위치한 디렉토리로 이동
cd "$(dirname "$0")"

# 2. 현재 버전 확인
current_version=$(sed -n "s/^version = \"\([^\"]*\)\"/\1/p" pyproject.toml)

# 3. 버전 업데이트를 입력받고, 아무 입력이 없을 경우 자동 증가
while true; do
    echo "새 버전을 입력해주세요 (현재 버전은 \"$current_version\") [자동 증가: Enter]: "
    read -r new_version

    if [[ -z "$new_version" ]]; then
        IFS="." read -r major minor patch <<< "$current_version"
        patch=$((patch + 1))
        new_version="$major.$minor.$patch"
        echo "버전이 자동으로 $new_version(으)로 설정되었습니다."
    fi

    sed -i "" "s/version = \"$current_version\"/version = \"$new_version\"/" pyproject.toml
    echo "버전을 $new_version(으)로 업데이트했습니다."
    break
done

# 4. 기존 빌드 파일 삭제 및 새 빌드 생성
echo "기존 빌드 파일을 삭제하고 새로 빌드합니다..."
rm -rf dist
python -m build

# 5. PyPI에 업로드
echo "PyPI에 업로드 중..."
if [ -z "$PYPI_TOKEN" ]; then
    echo "오류: PYPI_TOKEN 환경 변수가 설정되지 않았습니다."
    exit 1
fi

twine upload --username __token__ --password "$PYPI_TOKEN" dist/*

# 6. 프로젝트 업데이트
pip install .
echo "ccproject 작업 디렉토리 업데이트가 완료되었습니다."
