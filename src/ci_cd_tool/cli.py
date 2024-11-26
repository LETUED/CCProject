import click
from rich.console import Console
from .commands import init, ci_group, cd_group, config_group
from .core.logging import setup_logging

@click.group()
@click.version_option(version="0.2.6")
def main():
    """CI/CD 도구 CLI"""
    setup_logging()

# 명령어 등록
main.add_command(init)
main.add_command(ci_group)
main.add_command(cd_group)
main.add_command(config_group)

if __name__ == "__main__":
    main()
