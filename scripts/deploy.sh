#!/bin/bash

# 현재 버전 확인
current_version=$(sed -n 's/version = "\([^"]*\)"/\1/p' pyproject.toml)
echo "현재 버전: $current_version"

# 패치 버전 증가
IFS='.' read -r major minor patch <<< "$current_version"
new_version="$major.$minor.$((patch + 1))"

# pyproject.toml 버전 업데이트
sed -i '' "s/version = \"$current_version\"/version = \"$new_version\"/" pyproject.toml
echo "버전을 $new_version(으)로 업데이트했습니다."

# 빌드 및 배포
rm -rf dist/
python -m build
twine upload --username __token__ --password $PYPI_TOKEN dist/*

echo "배포가 완료되었습니다. 버전: $new_version"
