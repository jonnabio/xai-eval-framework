"""
Prompt engineering engine using Jinja2 templates.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import jinja2

class PromptEngine:
    """
    Manages loading and rendering of Jinja2 prompt templates.
    """
    
    def __init__(self, template_dir: Optional[Path] = None):
        """
        Initialize the prompt engine.
        
        Args:
            template_dir: Path to directory containing templates. 
                          Defaults to 'templates' subdirectory of this module.
        """
        if template_dir is None:
            # Default to 'templates' dir relative to this file
            template_dir = Path(__file__).parent / "templates"
            
        self.template_dir = template_dir
        
        # Initialize Jinja2 environment
        # Autoescape is generally good safety, though for prompts we might want raw control.
        # Keeping it False for flexibility with prompt engineering constructs unless needed.
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.template_dir)),
            autoescape=jinja2.select_autoescape(['html', 'xml'], default=False),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
    def render(self, template_name: str, **kwargs) -> str:
        """
        Render a template with provided context.
        
        Args:
            template_name: Name of the template file (e.g., 'eval_instruction.j2')
            **kwargs: Context variables to pass to the template.
            
        Returns:
            Rendered string.
            
        Raises:
            jinja2.TemplateNotFound: If template does not exist.
        """
        template = self.env.get_template(template_name)
        return template.render(**kwargs)
