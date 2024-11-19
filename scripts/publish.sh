#!/bin/bash

# 현재 디렉토리를 프로젝트 루트로 변경
cd "$(dirname "$0")/.."

# 현재 버전 확인
current_version=$(sed -n "s/^version = \"\([^\"]*\)\"/\1/p" pyproject.toml)

# 버전 업데이트
echo "현재 버전: $current_version"
echo "새 버전을 입력하세요 (Enter를 누르면 패치 버전이 증가합니다):"
read -r new_version

if [[ -z "$new_version" ]]; then
    IFS="." read -r major minor patch <<< "$current_version"
    patch=$((patch + 1))
    new_version="$major.$minor.$patch"
fi

# pyproject.toml 업데이트
sed -i "" "s/version = \"$current_version\"/version = \"$new_version\"/" pyproject.toml
echo "버전을 $new_version(으)로 업데이트했습니다."

# 빌드 및 배포
rm -rf dist/
python -m build

if [ -z "$PYPI_TOKEN" ]; then
    echo "오류: PYPI_TOKEN 환경 변수가 설정되지 않았습니다."
    exit 1
fi

python -m twine upload --username __token__ --password "$PYPI_TOKEN" dist/*

# Git 태그 생성
git add pyproject.toml
git commit -m "chore: Bump version to $new_version"
git tag -a "v$new_version" -m "Release version $new_version"
git push origin main "v$new_version" 