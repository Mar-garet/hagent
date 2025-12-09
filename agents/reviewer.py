from agents.base import BaseAgent
from agents.context import Riew
from prompts.reviewer import reviewer
from tools import tool_registry
from tools.registry import AgentType
from settings import settings
from prompts.common import common
from pathlib import Path
from typing import TypeAlias

Riew_output: TypeAlias = Riew


class ReviewerAgent(BaseAgent[Riew_output]):
    def __init__(self):
        tools = tool_registry.get_tools(AgentType.REVIEWER)
        super().__init__(tools=tools, output_type=Riew_output)

    def get_system_prompt(self) -> str:
        base_dir = Path(settings.TEST_BED) / settings.PROJECT_NAME
        combined_prompt = common.format(base_dir=str(base_dir)) + "\n" + reviewer
        return combined_prompt
