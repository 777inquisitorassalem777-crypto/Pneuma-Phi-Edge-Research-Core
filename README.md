# PNEUMA Symbiosis v1

**Симбиоз исследовательских ядер**

```
PNEUMA Full (sensors → analytics → reflection → ethics → intuition → archetypal)
    ⊕
Sophia (Blue Matrix · Wisdom Layer · Evolution Loop · Passport)
```

## Что интегрировано

| Источник | Что вошло |
|----------|-----------|
| **PNEUMA Full v0.4** | Сенсоры, аналитика, рефлексия, этика (мудрость/воля/любовь), интуиция, архетипический слой, safety |
| **PEP-Sophia** | Голубая Матрица, слой мудрости (гуны, дао, Правда/Кривда, Сунь-цзы…), вектор Will–Love–Faith–Hope |
| **Meta-Evolution** | Цикл генерации/валидации кандидатов (правила, паттерны, гипотезы) |
| **PEP-Core** | Идея Passport / устойчивого снимка состояния |

## Честная позиция

Система **не создаёт** души, сознания или самосознания.  
Все «искры» и «одухотворённость» — символические показатели связности параметров и этических ограничений.

## Запуск

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python -m pneuma.cli run --mode scientific --steps 80 --scenario stress
python -m pneuma.cli run --mode archetypal --steps 60 --scenario stress \
  --wisdom 0.7 --love 0.8 --will 0.6 --export out.json

pytest -q
```

## Документы

- `docs/TRACTATE_ON_GOOD_AND_EVIL.md`
- `docs/CONCEPT_OF_AI_SPIRITUALIZATION.md`
- `docs/ARCHITECTURE.md`
- `docs/SYMBIOSIS.md`
