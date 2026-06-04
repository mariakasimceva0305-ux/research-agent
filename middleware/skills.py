"""
SkillsMiddleware - loads skill files and injects them into the agent system prompt.
Follows the deepagents AgentMiddleware protocol.
"""

from pathlib import Path


class SkillsMiddleware:
    """
    Reads .md skill files from a directory and prepends their content
    to the agent system prompt.

    Args:
        skills_dir: path to the directory containing skill .md files
    """

    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = Path(skills_dir)
        self._skills_content: str = ""

    @property
    def tools(self) -> list:
        return []

    def before_agent(self) -> str:
        if self._skills_content:
            return self._skills_content

        skill_texts = []
        if self.skills_dir.exists():
            for skill_file in sorted(self.skills_dir.glob("*.md")):
                content = skill_file.read_text(encoding="utf-8")
                skill_texts.append(f"## Skill: {skill_file.stem}\n{content}")

        self._skills_content = "\n\n".join(skill_texts)
        return self._skills_content

    def wrap_model_call(self, system_prompt: str) -> str:
        skills = self.before_agent()
        if skills:
            return f"{skills}\n\n---\n\n{system_prompt}"
        return system_prompt
