import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm
from ..analyzer.project_analyzer import ProjectAnalyzer
from ..config.config_manager import ConfigManager
from ..core.exceptions import error_handler

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
    existing_config = config_manager.config
    
    if existing_config and not force:
        if not Confirm.ask("[yellow]이미 설정이 존재합니다. 덮어쓰시겠습니까?[/yellow]"):
            console.print("[yellow]설정을 유지합니다.[/yellow]")
            return False
            
    # 4. 설정 저장
    try:
        config = {
            'ci': {
                'provider': structure.ci_provider,
                'branch_strategy': structure.branch_strategy,
                'language': structure.language,
                'framework': structure.framework,
                'test_framework': structure.test_framework,
                'project_root': str(Path.cwd())
            },
            'repository': {
                'owner': '',  # GitHub 사용자명 설정 필요
                'name': Path.cwd().name  # 현재 디렉토리 이름을 저장소 이름으로 사용
            }
        }
        
        for key, value in config.items():
            config_manager.set_value(key, value)
            
        console.print("[green]✨ CI/CD 설정이 완료되었습니다![/green]")
        console.print("\n[yellow]다음 단계:[/yellow]")
        console.print("1. GitHub 토큰 설정: export GITHUB_TOKEN=your_token")
        console.print("2. 저장소 정보 설정:")
        console.print("   cc config set repository.owner your-github-username")
        console.print("3. Git 원격 저장소 설정:")
        console.print("   git remote add origin https://github.com/your-github-username/your-repo-name.git")
        console.print("   git push -u origin main")
        return True
            
    except Exception as e:
        console.print(f"[red]설정 저장 중 오류 발생: {str(e)}[/red]")
        return False

__all__ = ['init']