import click
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm
from ..analyzer.project_analyzer import ProjectAnalyzer
from ..templates.ci_generator import CIGenerator
from ..core.exceptions import error_handler
from ..core.logging import setup_logging
from ..config.config_manager import ConfigurationManager
from ..config.manager import ConfigManager
from pathlib import Path

# 로깅 설정
setup_logging()

@click.command(name='init')
@click.option('--force', is_flag=True, help="기존 설정 덮어쓰기")
@error_handler()
def init(force: bool):
    """프로젝트 분석 및 CI/CD 자동 설정"""
    console = Console()
    
    # 1. 프로젝트 분석
    with console.status("[bold blue]프로젝트 분석 중...[/bold blue]"):
        analyzer = ProjectAnalyzer(console)
        try:
            structure = analyzer.analyze()
        except Exception as e:
            console.print(f"[red]프로젝트 분석 중 오류 발생: {str(e)}[/red]")
            return False
    
    # 2. 분석 결과 출력
    table = Table(title="🔍 프로젝트 분석 결과")
    table.add_column("항목", style="cyan")
    table.add_column("감지된 설정", style="green")
    
    table.add_row("언어", structure.language)
    table.add_row("프레임워크", structure.framework or "없음")
    table.add_row("테스트 도구", structure.test_framework or "없음")
    table.add_row("CI 도구", structure.ci_provider or "미설정")
    table.add_row("브랜치 전략", structure.branch_strategy or "미설정")
    
    console.print(table)
    
    # 3. 기존 설정 확인
    config_manager = ConfigManager()
    ci_config = config_manager.get_section_config('ci')
    
    if ci_config and not force:
        if not Confirm.ask("[yellow]이미 CI 설정이 존재합니다. 덮어쓰시겠습니까?[/yellow]"):
            console.print("[yellow]설정을 유지합니다.[/yellow]")
            return False
    
    # 4. CI/CD 설정 파일 생성
    try:
        with console.status("[bold blue]CI/CD 설정 생성 중...[/bold blue]"):
            generator = CIGenerator(structure)
            files_created = generator.generate()
            
            # 설정 저장
            if config_manager.update_config({
                'ci': {
                    'provider': structure.ci_provider,
                    'branch_strategy': structure.branch_strategy,
                    'language': structure.language,
                    'framework': structure.framework,
                    'test_framework': structure.test_framework,
                    'project_root': str(Path.cwd()),
                    'pipeline_stages': []
                }
            }, force=force):
                console.print("[green]CI/CD 설정이 저장되었습니다[/green]")
                return True
            else:
                console.print("[red]CI/CD 설정 저장 중 오류가 발생했습니다[/red]")
                return False
                
    except Exception as e:
        console.print(f"[red]CI/CD 설정 생성 중 오류 발생: {str(e)}[/red]")
        return False