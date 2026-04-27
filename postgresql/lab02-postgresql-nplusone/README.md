## Subindo camada de infra:

```
docker compose up -d --build
```

## Subindo camada do faker (dataset generator)
Confira se o estado do container 'postgres' está (healthy), e então prossiga com a geração dos dados artificiais do lab:

```
docker compose --profile datasetgen build ds_generator
docker compose --profile datasetgen run --rm ds_generator
```

É possível customizar o volume do dataset através de variáveis de ambientes lidas pelo argparse. Dê uma conferida no ds_generator/generate_data.py.

Então, você pode conferir os dados com:

```
docker exec -it postgres bash

-- Dentro do container:
psql -U lab -d nplusone

-- No psql:
nplusone=# \dt
          List of relations
 Schema |    Name     | Type  | Owner
--------+-------------+-------+-------
 public | customers   | table | lab
 public | order_items | table | lab
 public | orders      | table | lab
(3 rows)

nplusone=# select * from customers limit 5;
  id  |             name
------+-------------------------------
    1 | Brenda Alves
    2 | Sra. Isabelly Câmara
    3 | Cauã Rocha
    4 | Dra. Aurora Pastor
    5 | Ana Beatriz Alves
```

## Subindo app (backend)

```bash
docker compose --profile backend up --build
```

Valide o backend através de chamada curl/wget, postman ou pelo seu próprio browser, pelo url http://localhost:8000/customers/12/products/nplus1. O navegador vai mostrar o JSON retornado pela API.

O equivalente via curl é:

```bash
curl -s http://localhost:8000/customers/12/products/nplus1 | jq
```

## Subindo o teste de carga

Uma vez que temos o banco funcional, observabilidade configurada (acessível em http://localhost:3000), e um backend comunicando com esse banco, faremos um teste de carga simples, usando wrk e dois scripts Lua bem triviais, um chamando o endpoint n+1 e outro chamando o endpoint que resolve o dataset através de join.

``` bash
docker compose --profile loadtest up --build
docker compose exec loadtest bash
```

Com o container de pé, rode o teste N+1, por no mínimo 3x para validar consistencia de resultados:

```bash
wrk -t4 -c50 -d30s \
  -s /wrk/backend_calling_nplusone.lua \
  http://backend:8000
```

Avalie as métricas do banco, e o sumário de tempos de resposta e TP retornados pelo WRK.
Agora, rode a chamada que envolve Join:

```bash
wrk -t4 -c50 -d30s \
  -s /wrk/backend_calling_join.lua \
  http://backend:8000
```

Compare os resultados de ambas, e impacto no ambiente de dados.

## Zerando o lab

```bash
docker compose --profile ds_generator down -v
docker compose --profile loadtest down -v
docker compose --profile backend down -v
docker compose down -v
docker compose down --
```