from setuptools import setup, find_packages

setup(
    name='ci-cd-tool',  # 패키지 이름 (고유해야 함)
    version='0.1.4',  # 버전
    description='A CLI tool for managing CI/CD pipelines',
    long_description=open('README.md').read(),  # PyPI 페이지에 표시될 설명
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/username/ci-cd-tool',  # GitHub 또는 프로젝트 페이지
    packages=find_packages('src'),  # src 폴더 내의 모든 패키지 찾기
    package_dir={'': 'src'},  # 패키지 디렉토리를 src로 설정
    install_requires=[
        "click==8.0.3",  # CLI 명령어 관리 라이브러리
        "pyyaml==6.0",  # YAML 파일을 로드하는 라이브러리
        "pygithub==1.55",  # GitHub Actions API 연동 라이브러리
        "python-gitlab==3.0.0",  # GitLab CI API 연동 라이브러리
        "boto3==1.21.0",  # AWS SDK for Python (배포 관련)
        "heroku3",  # Heroku API 연동 라이브러리
        "google-cloud-storage==2.3.0",  # Google Cloud 배포를 위한 라이브러리
        "requests==2.26.0",  # HTTP 요청 유틸리티
        "inquirer"  # 사용자 입력을 위한 라이브러리
    ],
    entry_points={
        'console_scripts': [
            'cc = ci_cd_tool.cli:main',  # CLI 명령어
        ],
    },
    include_package_data=True,
    classifiers=[  # 패키지 메타데이터
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
