import click
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm
from ..analyzer.project_analyzer import ProjectAnalyzer
from ..templates.ci_generator import CIGenerator
from ..core.exceptions import error_handler
from ..core.logging import setup_logging

# 로깅 설정
setup_logging()

@click.command(name='init')
@click.option('--force', is_flag=True, help="기존 설정 덮어쓰기")
def init(force: bool):
    """프로젝트 분석 및 CI/CD 자동 설정"""
    console = Console()
    
    # 1. 프로젝트 분석
    with console.status("[bold blue]프로젝트 분석 중...[/bold blue]"):
        analyzer = ProjectAnalyzer()
        structure = analyzer.analyze()
    
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
    if structure.ci_provider and not force:
        if Confirm.ask("[yellow]이미 CI 설정이 존재합니다. 덮어쓰시겠습니까?[/yellow]"):
            force = True
        else:
            console.print("[yellow]설정을 유지합니다.[/yellow]")
            return
    
    # 4. CI/CD 설정 파일 생성
    with console.status("[bold blue]CI/CD 설정 생성 중...[/bold blue]"):
        generator = CIGenerator(structure)
        files_created = generator.generate()
    
    # 5. 결과 출력
    console.print("\n[bold green]✨ CI/CD 설정이 완료되었습니다![/bold green]")
    for file in files_created:
        console.print(f"📄 생성된 파일: {file}")
    
    # 6. 다음 단계 안내
    console.print("\n[bold blue]🚀 다음 단계:[/bold blue]")
    console.print("1. git add . 로 생성된 파일들을 스테이징")
    console.print("2. git commit -m 'chore: Add CI/CD configuration'")
    console.print("3. git push 로 변경사항을 원격 저장소에 푸시")