"""
agent.py - assembles the research agent with middleware stack.
"""

from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from middleware.skills import SkillsMiddleware
from middleware.filesystem import FileSystemMiddleware
from tools.web_search import web_search


def build_agent(skills_dir: str = "skills"):
    skills_mw = SkillsMiddleware(skills_dir=skills_dir)
    filesystem_mw = FileSystemMiddleware(
        base_dir=".",
        allowed_tools=["write_file"],
    )

    base_system_prompt = (
        "You are a research assistant. "
        "Always respond to the user in Russian. "
        "Use web_search tool to find information. "
        "Perform 2-3 searches on different aspects of the topic."
    )
    system_prompt = skills_mw.wrap_model_call(base_system_prompt)

    all_tools = [web_search] + filesystem_mw.tools

    model = ChatGroq(model="llama-3.1-8b-instant", temperature=0.2)

    agent = create_react_agent(
        model=model,
        tools=all_tools,
        prompt=system_prompt,
    )

    return agent
