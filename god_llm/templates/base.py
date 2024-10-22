from abc import ABC, abstractmethod
import re
from typing import Any, Dict, List, Optional, Set
from string import Template
import json
from pathlib import Path


class BaseTemplate(ABC):
    def __init__(self, template: str):
        self.template = Template(template)

    @abstractmethod
    def format(self, **kwargs) -> str:
        pass


class SimpleTemplate(Template):
    def get_required_variables(self) -> Set[str]:
        pattern = r"\$\{([^}]*)\}"
        matches = re.findall(pattern, self.template)
        return set(matches)

    def get_missing_variables(self, **kwargs) -> List[str]:
        required = self.get_required_variables()
        provided = set(kwargs.keys())
        return list(required - provided)

    def format(self, **kwargs) -> str:
        missing = self.get_missing_variables(**kwargs)
        if missing:
            raise ValueError(f"Missing required variables: {', '.join(missing)}")
        return self.safe_substitute(**kwargs)


class JsonTemplate(BaseTemplate):
    def format(self, **kwargs) -> str:
        try:
            formatted = self.template.safe_substitute(**kwargs)
            json.loads(formatted)  # Validate JSON
            return formatted
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON template: {e}")


class TemplateManager:
    def __init__(self, templates_dir: Optional[Path] = None):
        self.templates_dir = templates_dir or Path(__file__).parent
        self.templates: Dict[str, BaseTemplate] = {}
        self._load_templates()

    def _load_templates(self):
        if not self.templates_dir.exists():
            return

        for template_file in self.templates_dir.glob("*.json"):
            with open(template_file) as f:
                data = json.load(f)
                for name, template_data in data.items():
                    template_type = template_data.get("type", "simple")
                    template_class = self._get_template_class(template_type)
                    self.templates[name] = template_class(template_data["template"])

    def _get_template_class(self, template_type: str) -> type[BaseTemplate]:
        return {"simple": SimpleTemplate, "json": JsonTemplate}.get(
            template_type, SimpleTemplate
        )

    def get_template(self, name: str) -> BaseTemplate:
        if name not in self.templates:
            raise KeyError(f"Template {name} not found")
        return self.templates[name]

    def register_template(
        self, name: str, template: str, template_type: str = "simple"
    ):
        template_class = self._get_template_class(template_type)
        self.templates[name] = template_class(template)

    def list_templates(self) -> List[str]:
        return list(self.templates.keys())
