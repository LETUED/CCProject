#!/bin/bash

# API 토큰 확인
if [ -z "$PYPI_API_TOKEN" ]; then
    echo "Error: PYPI_API_TOKEN 환경변수가 설정되지 않았습니다."
    echo "~/.zshrc 또는 ~/.bashrc 파일에 다음을 추가해주세요:"
    echo "export PYPI_API_TOKEN='your-api-token-here'"
    exit 1
fi

# 프로젝트 루트 디렉토리로 이동
cd "$(dirname "$0")/.."

# pyproject.toml이 있는지 확인
if [ ! -f "pyproject.toml" ]; then
    echo "Error: pyproject.toml 파일을 찾을 수 없습니다."
    echo "현재 디렉토리: $(pwd)"
    exit 1
fi

# 현재 버전 가져오기
CURRENT_VERSION=$(grep '^version = ' pyproject.toml | sed -E 's/version = "([0-9]+\.[0-9]+\.[0-9]+)"/\1/' | tr -d '\n\r')
echo "현재 버전: $CURRENT_VERSION"

# 버전 형식 검증
if ! [[ $CURRENT_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: 현재 버전 형식이 올바르지 않습니다: $CURRENT_VERSION"
    echo "예상되는 형식: X.Y.Z (예: 0.3.0)"
    exit 1
fi

# 새 버전 입력 받기
read -p "새 버전을 입력해주세요 (현재 버전은 \"$CURRENT_VERSION\") [자동 증가: Enter]: " NEW_VERSION

# 버전 업데이트
if [ -z "$NEW_VERSION" ]; then
    # 자동 증가 로직
    IFS='.' read -r major minor patch <<< "$CURRENT_VERSION"
    NEW_VERSION="${major}.${minor}.$((patch + 1))"
    echo "버전이 자동으로 $NEW_VERSION(으)로 설정되었습니다."
fi

# 입력된 버전이 현재 버전과 같은지 확인
if [ "$NEW_VERSION" = "$CURRENT_VERSION" ]; then
    echo "오류: 새 버전이 현재 버전과 동일합니다."
    exit 1
fi

# pyproject.toml 업데이트
sed -i '' "s/version = \"$CURRENT_VERSION\"/version = \"$NEW_VERSION\"/" pyproject.toml
if [ $? -ne 0 ]; then
    echo "버전 업데이트 중 오류가 발생했습니다."
    exit 1
fi
echo "버전을 $NEW_VERSION(으)로 업데이트했습니다."

# 빌드 및 배포
echo "기존 빌드 파일을 삭제하고 새로 빌드합니다..."
rm -rf dist/ build/ *.egg-info/
python -m build

echo "PyPI에 업로드 중..."
# API 토큰을 사용하여 업로드
TWINE_USERNAME="__token__" TWINE_PASSWORD="$PYPI_API_TOKEN" python -m twine upload dist/*

echo "작업이 완료되었습니다."
