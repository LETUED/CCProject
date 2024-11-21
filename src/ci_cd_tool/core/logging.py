import logging
from rich.logging import RichHandler
from pathlib import Path

def setup_logging(
    log_level: str = "INFO",
    log_file: str = ".cc/cc.log"
) -> None:
    """
    로깅 설정
    
    Args:
        log_level: 로그 레벨 (기본값: INFO)
        log_file: 로그 파일 경로 (기본값: .cc/cc.log)
    """
    # 로그 디렉토리 생성
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 로그 포맷 설정
    format_string = "%(asctime)s | %(levelname)s | %(message)s"
    
    # 기본 로깅 설정
    logging.basicConfig(
        level=log_level,
        format=format_string,
        handlers=[
            # 콘솔 출력용 Rich 핸들러
            RichHandler(rich_tracebacks=True),
            # 파일 출력용 핸들러
            logging.FileHandler(log_file)
        ]
    )
    
    # 로거 가져오기
    logger = logging.getLogger("ci_cd_tool")
    logger.setLevel(log_level)