# Агент для поиска источников и подготовки обзора

Учебный CLI-агент на LangGraph: получает тему, выполняет веб-поиск и сохраняет обзор в Markdown. Модель — Groq; поиск — DuckDuckGo через ddgs.

## Компоненты

- `agent.py` — сборка агента;
- `tools/web_search.py` — поиск;
- `middleware/skills.py` — загрузка инструкций из `skills/`;
- `middleware/filesystem.py` — файловые инструменты с ограниченным набором операций;
- `reports/` — сохранённые обзоры.

## Запуск

```bash
pip install -r requirements.txt
cp .env.example .env
# Укажите GROQ_API_KEY
python main.py "computer vision for satellite imagery"
```

Результат — текстовый обзор со ссылками. Источники и соответствие утверждений их содержанию требуют проверки: наличие ссылок само по себе не доказывает точность. Отдельный benchmark качества обзоров не проводился.
