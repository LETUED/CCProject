import pytest
from click.testing import CliRunner
from ci_cd_tool.commands.init_commands import init

def test_init_command_basic(cli_runner, mocker):
    """기본 초기화 명령어 테스트"""
    # ProjectAnalyzer mock 설정
    mock_analyzer = mocker.patch('ci_cd_tool.analyzer.project_analyzer.ProjectAnalyzer')
    mock_structure = mocker.MagicMock()
    mock_structure.language = 'Python'
    mock_structure.framework = None
    mock_structure.test_framework = 'pytest'
    mock_structure.ci_provider = None
    mock_structure.branch_strategy = None
    mock_analyzer.return_value.analyze.return_value = mock_structure
    
    result = cli_runner.invoke(init)
    
    assert result.exit_code == 0
    assert "🔍 프로젝트 분석 결과" in result.output
    assert "Python" in result.output
    assert "pytest" in result.output

def test_init_command_with_force(cli_runner, mocker):
    """강제 초기화 옵션 테스트"""
    # ProjectAnalyzer mock 설정
    mock_analyzer = mocker.patch('ci_cd_tool.analyzer.project_analyzer.ProjectAnalyzer')
    mock_structure = mocker.MagicMock()
    mock_structure.language = 'Python'
    mock_structure.ci_provider = None
    mock_analyzer.return_value.analyze.return_value = mock_structure
    
    # CIGenerator mock 설정
    mock_generator = mocker.patch('ci_cd_tool.templates.ci_generator.CIGenerator')
    mock_generator.return_value.generate.return_value = ['.github/workflows/ci.yml']
    
    result = cli_runner.invoke(init, ['--force'])
    
    assert result.exit_code == 0
    assert "🔍 프로젝트 분석 결과" in result.output
    assert "✨ CI/CD 설정이 완료되었습니다!" in result.output

def test_init_command_with_existing_ci(cli_runner, mocker):
    """기존 CI 설정 존재 시 테스트"""
    # ProjectAnalyzer mock 설정
    mock_analyzer = mocker.patch('ci_cd_tool.analyzer.project_analyzer.ProjectAnalyzer')
    mock_structure = mocker.MagicMock()
    mock_structure.language = 'Python'
    mock_structure.ci_provider = 'GitHub Actions'
    mock_analyzer.return_value.analyze.return_value = mock_structure
    
    result = cli_runner.invoke(init, input='n\n')
    
    assert result.exit_code == 0
    assert "이미 CI 설정이 존재합니다" in result.output
    assert "설정을 유지합니다" in result.output

def test_init_command_with_analysis_error(cli_runner, mocker):
    """프로젝트 분석 중 오류 발생 테스트"""
    # ProjectAnalyzer mock이 예외를 발생시키도록 설정
    mock_analyzer = mocker.patch('ci_cd_tool.analyzer.project_analyzer.ProjectAnalyzer')
    mock_analyzer.return_value.analyze.side_effect = Exception("EOF when reading a line")
    
    result = cli_runner.invoke(init)
    
    assert result.exit_code == 0
    assert all(text in result.output for text in [
        "시스템 오류",
        "예상치 못한 오류",
        "EOF when reading a line"
    ])

def test_init_command_successful_generation(cli_runner, mocker):
    """CI/CD 설정 파일 생성 성공 테스트"""
    # ProjectAnalyzer mock 설정
    mock_analyzer = mocker.patch('ci_cd_tool.analyzer.project_analyzer.ProjectAnalyzer')
    mock_structure = mocker.MagicMock()
    mock_structure.language = 'Python'
    mock_structure.ci_provider = None
    mock_analyzer.return_value.analyze.return_value = mock_structure
    
    # CIGenerator mock 설정
    mock_generator = mocker.patch('ci_cd_tool.templates.ci_generator.CIGenerator')
    mock_generator.return_value.generate.return_value = ['.github/workflows/ci.yml']
    
    result = cli_runner.invoke(init, ['--force'])  # force 옵션 추가
    
    assert result.exit_code == 0
    assert "✨ CI/CD 설정이 완료되었습니다!" in result.output
    assert "생성된 파일: .github/workflows/ci.yml" in result.output
    assert "다음 단계:" in result.output

@pytest.fixture
def cli_runner():
    return CliRunner() 