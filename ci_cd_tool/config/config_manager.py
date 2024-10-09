import yaml  # PyYAML 라이브러리
import os
import click

# 설정 파일 경로
CONFIG_FILE = "config.yml"


# 설정 파일 로드 함수
def load_config():
    """config.yml 파일을 로드"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return yaml.safe_load(f)
    else:
        return {}


# 설정 파일 저장 함수
def save_config(config):
    """config.yml 파일을 저장"""
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    click.echo(f"설정이 {CONFIG_FILE}에 저장되었습니다.")


# 설정 파일 조회 기능
def show_config():
    """설정 파일을 출력"""
    config_data = load_config()
    if config_data:
        click.echo("현재 설정 파일 내용:")
        click.echo(yaml.dump(config_data, default_flow_style=False))
    else:
        click.echo("설정 파일이 존재하지 않거나 비어 있습니다.")


# 설정 파일 값 변경 기능
def change_config(key, value):
    """설정 파일의 특정 값을 변경"""
    config_data = load_config()
    config_data[key] = value
    save_config(config_data)
    click.echo(f"'{key}' 값이 '{value}'로 설정되었습니다.")


# 설정 파일 초기화 기능
def reset_config():
    """설정 파일 초기화"""
    config_data = {}
    save_config(config_data)
    click.echo(f"{CONFIG_FILE} 파일이 초기화되었습니다.")
