from pathlib import Path
from typing import Dict, Optional
from jinja2 import Environment, FileSystemLoader
from ..core.exceptions import TemplateError

class TemplateManager:
    """CI/CD 템플릿 관리 클래스"""
    
    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = Path(templates_dir)
        self.env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def render_template(
        self, 
        template_name: str, 
        context: Dict,
        output_path: Optional[str] = None
    ) -> str:
        """
        템플릿 렌더링
        
        Args:
            template_name: 템플릿 파일명
            context: 템플릿 컨텍스트
            output_path: 출력 파일 경로 (선택)
            
        Returns:
            str: 렌더링된 템플릿 내용
        """
        try:
            template = self.env.get_template(template_name)
            rendered = template.render(**context)
            
            if output_path:
                self._save_template(rendered, output_path)
                
            return rendered
            
        except Exception as e:
            raise TemplateError(f"템플릿 렌더링 실패: {str(e)}")
    
    def _save_template(self, content: str, path: str) -> None:
        """템플릿 저장"""
        try:
            output_path = Path(path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(content)
        except Exception as e:
            raise TemplateError(f"템플릿 저장 실패: {str(e)}")