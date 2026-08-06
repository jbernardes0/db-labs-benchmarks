# N+1 Dataset Generator

Este módulo gera um dataset realista de `orders -> order_items`
com distribuição desbalanceada (skew), voltado para labs de Query N+1.

## Distribuição padrão

- 5% orders heavy (50–100 items)
- 20% orders medium (10–30 items)
- 75% orders light (1–5 items)

## Executando via Docker

```bash
docker compose up --build
```

## Parametros

--orders        Total de orders (default: 100000)
--heavy-pct     Percentual heavy
--medium-pct    Percentual medium
--light-pct     Percentual light
--days          Janela de datas (default: 90)

Exemplo:

```bash
docker compose run datasetgen \
  python generate_data.py --orders 500000
```
