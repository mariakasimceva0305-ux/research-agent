"""
FileSystemMiddleware - provides file operation tools to the agent.
Extended from the deepagents pattern with an allowed_tools parameter
to explicitly control which tools are exposed to the agent.
"""

from pathlib import Path
from typing import Optional
from langchain_core.tools import tool


ALL_TOOLS = ["write_file", "read_file", "list_files"]


def make_write_file_tool(base_dir: str = "."):
    @tool
    def write_file(path: str, content: str) -> str:
        """
        Write content to a file. Creates parent directories if needed.
        Args:
            path: relative file path (e.g. 'reports/research_001.md')
            content: text content to write
        Returns:
            confirmation message with the file path
        """
        full_path = Path(base_dir) / path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")
        return f"File saved: {full_path}"

    return write_file


def make_read_file_tool(base_dir: str = "."):
    @tool
    def read_file(path: str) -> str:
        """
        Read content from a file.
        Args:
            path: relative file path
        Returns:
            file content as string, or an error message if not found
        """
        full_path = Path(base_dir) / path
        if not full_path.exists():
            return f"Error: file not found: {full_path}"
        return full_path.read_text(encoding="utf-8")

    return read_file


def make_list_files_tool(base_dir: str = "."):
    @tool
    def list_files(directory: str = ".") -> str:
        """
        List files in a directory.
        Args:
            directory: relative path to directory
        Returns:
            newline-separated list of file paths
        """
        full_path = Path(base_dir) / directory
        if not full_path.exists():
            return f"Directory not found: {full_path}"
        files = [str(p.relative_to(base_dir)) for p in full_path.rglob("*") if p.is_file()]
        return "\n".join(files) if files else "No files found."

    return list_files


class FileSystemMiddleware:
    """
    Provides filesystem tools to the agent.

    Extended from the deepagents FilesystemMiddleware: accepts an
    allowed_tools parameter to explicitly select which tools are
    injected into the agent.

    Args:
        base_dir: root directory for all file operations
        allowed_tools: list of tool names to expose.
                       Defaults to all tools if None.
                       Available: 'write_file', 'read_file', 'list_files'
    """

    def __init__(
        self,
        base_dir: str = ".",
        allowed_tools: Optional[list[str]] = None,
    ):
        self.base_dir = base_dir
        self.allowed_tools = allowed_tools or ALL_TOOLS
        self._tools = self._build_tools()

    def _build_tools(self) -> list:
        factories = {
            "write_file": make_write_file_tool,
            "read_file": make_read_file_tool,
            "list_files": make_list_files_tool,
        }
        result = []
        for name in self.allowed_tools:
            if name not in factories:
                raise ValueError(f"Unknown tool: '{name}'. Available: {ALL_TOOLS}")
            result.append(factories[name](self.base_dir))
        return result

    @property
    def tools(self) -> list:
        return self._tools

    def before_agent(self) -> str:
        return ""

    def wrap_model_call(self, system_prompt: str) -> str:
        return system_prompt
