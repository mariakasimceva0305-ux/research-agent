"""
main.py - CLI entry point.
Usage: python main.py "research topic"
"""

import sys
from dotenv import load_dotenv

load_dotenv()

from agent import build_agent


def run_research(topic: str):
    print(f"\nTopic: {topic}\n")
    print("-" * 50)

    agent = build_agent()

    user_message = (
        f"Проведи исследование на тему: {topic}\n\n"
        f"После исследования сохрани отчёт в формате Markdown "
        f"по пути reports/research_001.md со структурой:\n"
        f"# {topic}\n"
        f"## Краткое резюме\n"
        f"## Основные находки\n"
        f"## Источники\n\n"
        f"Используй инструмент write_file для сохранения. "
        f"В конце сообщи путь к сохранённому файлу."
    )

    result = agent.invoke({"messages": [{"role": "user", "content": user_message}]})

    final_message = result["messages"][-1].content
    print(final_message)
    print("-" * 50)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python main.py "research topic"')
        print('Example: python main.py "quantum computing"')
        sys.exit(1)

    topic = " ".join(sys.argv[1:])
    run_research(topic)
