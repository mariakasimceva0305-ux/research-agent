# Research Agent

Research agent built with LangGraph. Takes a topic, runs web searches, and saves a structured Markdown report.

## What is implemented

- Part 1 (required): SkillsMiddleware, FileSystemMiddleware with `allowed_tools`, `web_search` tool, ReAct agent, responses in Russian
- Part 2 (bonus): `write_file` tool, Markdown report saved to `reports/`

## Stack

| Component | Choice |
|-----------|--------|
| LLM | Groq llama-3.1-8b-instant (free) |
| Agent | `langgraph.prebuilt.create_react_agent` |
| Search | DuckDuckGo via `ddgs` (no API key required) |
| Interface | CLI |

## Project structure

```
research-agent/
├── main.py                  # CLI entry point
├── agent.py                 # agent assembly with middleware
├── tools/
│   └── web_search.py        # DuckDuckGo search tool
├── middleware/
│   ├── skills.py            # SkillsMiddleware
│   └── filesystem.py        # FileSystemMiddleware (extended)
├── skills/
│   └── researcher.md        # Researcher skill definition
├── reports/                 # saved reports go here
├── .env.example
└── requirements.txt
```

## Middleware

### SkillsMiddleware

Reads `.md` files from the `skills/` directory and prepends their content to the agent system prompt via `wrap_model_call()`. The `researcher.md` skill defines the agent role: how to formulate search queries, how to structure output, and what language to respond in.

### FileSystemMiddleware

Extended from the deepagents `FilesystemMiddleware` pattern. Accepts an `allowed_tools` parameter to explicitly control which file tools are exposed to the agent:

```python
# only write_file
FileSystemMiddleware(base_dir=".", allowed_tools=["write_file"])

# all available tools
FileSystemMiddleware(base_dir=".", allowed_tools=["write_file", "read_file", "list_files"])
```

## Setup

```bash
cd research-agent
pip install -r requirements.txt
cp .env.example .env
# add your GROQ_API_KEY to .env
```

### API keys

| Key | Where to get | Required |
|-----|-------------|----------|
| `GROQ_API_KEY` | console.groq.com (free) | yes |

DuckDuckGo does not require an API key.

## Usage

```bash
python main.py "quantum computing"
python main.py "LLM applications in medicine"
python main.py "electric vehicle market 2025"
```

## Example output

```
Topic: квантовые компьютеры
--------------------------------------------------
# квантовые компьютеры

## Краткое резюме
Квантовые компьютеры представляют собой новую модель вычислений, основанную
на принципах квантовой механики. Они могут решать проблемы, которые невозможно решить
классическими компьютерами.

## Основные находки
* Квантовые компьютеры могут решать проблемы, невозможные для классических машин.
* Будущие области: криптография, оптимизация, материаловедение, медицина.
* Лидеры: IBM, Google, IonQ, Rigetti.

## Источники
* [1] https://en.wikipedia.org/wiki/Quantum_computer
* [2] https://www.ibm.com/quantum/
* [3] https://arxiv.org/abs/2105.01134
* [4] https://www.analyticssteps.com/blogs/recent-advancements-quantum-computing

Report saved: reports/research_001.md
--------------------------------------------------
```

## Agent logic (ReAct loop)

```
1. Receives topic from user
2. SkillsMiddleware injects Researcher instructions into system prompt
3. Agent formulates 2-3 search queries
4. Calls web_search() for each query
5. Analyzes and cross-references results
6. Produces a summary in Russian
7. Calls write_file() to save reports/research_001.md
8. Returns the file path to the user
```
