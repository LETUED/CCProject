from setuptools import setup, find_packages

setup(
    name="ci_cd_tool",  # 패키지 이름
    version="0.1.0",  # 패키지 버전
    packages=find_packages(),  # 패키지 내 하위 디렉토리를 자동으로 패키지로 포함
    install_requires=[
        "click",  # CLI 라이브러리
        "pygithub",  # GitHub Actions API 통합
        "python-gitlab",  # GitLab CI API 통합
    ],
    entry_points={
        'console_scripts': [
            'cc=ci_cd_tool.cli:main',  # CLI 진입점 정의 (ci_cd_tool에 맞춰 수정)
        ],
    },
    python_requires=">=3.6",  # 파이썬 버전 제한
)
