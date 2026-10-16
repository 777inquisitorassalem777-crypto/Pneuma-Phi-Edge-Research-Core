# PNEUMA-Edge Unified v0.2.0

**Phenomenological Reflective Ethical Unified Mind Architecture**

Объединённый исследовательский проект с двумя режимами:

| Режим | Описание |
|-------|----------|
| **scientific** | Классический контур: сенсоры → аналитика → рефлексия → этика → безопасность. Никаких метафизических утверждений. |
| **archetypal** | Тот же научный контур + **опциональный гипотетический слой**. Модель «сущностей», руминаций и циклов 70–100 лет явно помечена как `archetypal_hypothesis_not_fact`. |

Проект **не утверждает** существование душ, низкочастотных сущностей или «жатвы».  
Архетипический слой — инструмент для исследования культурных и эзотерических моделей смысла.

## Возможности

- Расширенный симулятор сенсоров (HRV, CO₂, инфразвук, свет, шум, sleep debt, social isolation).
- Расширенная аналитика паттернов (включая rumination_loop, moral_erosion_proxy).
- Рефлексия с жёстким разделением observation / interpretation / hypothesis.
- Этическое ядро + SafetyGate (human-in-the-loop, append-only audit).
- Архетипический слой (только в режиме `archetypal`).
- Отчёты: JSON + Markdown + данные для визуализации.
- 8 unit-тестов.

## Быстрый старт

```bash
cd pneuma_edge_unified
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Научный режим
python -m pneuma_edge.cli run --mode scientific --steps 100 --scenario stress --export sci.json

# Архетипический режим
python -m pneuma_edge.cli run --mode archetypal --steps 80 --scenario stress --export arch.json

# Тесты
pytest -q
```

## Архитектура

```
sensors → analytics → reflection (± archetypal layer) → ethics → safety → reporting
```

## Структура

```
pneuma_edge_unified/
├── README.md
├── LICENSE (MIT)
├── Makefile
├── pyproject.toml
├── requirements.txt
├── docs/RESEARCH_PROTOCOL.md
├── pneuma_edge/
│   ├── cli.py
│   ├── core/models.py
│   ├── sensors/simulator.py
│   ├── analytics/engine.py
│   ├── reflection/
│   │   ├── module.py
│   │   └── archetypal.py      # гипотетический слой
│   ├── ethics/core.py
│   ├── safety/guard.py
│   ├── reporting/report.py
│   └── archetypal/            # полный симулятор сущностей + циклы
│       ├── entities.py
│       ├── rumination.py
│       └── war_cycle.py
└── tests/test_pneuma.py
```

## Научная позиция

Все выводы архетипического слоя имеют статус  
`epistemic_status: "archetypal_hypothesis_not_fact"`.

Система никогда не утверждает, что сущности реальны.
