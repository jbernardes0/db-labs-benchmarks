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

Você pode conferir os dados com:

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

nplusone=# select * from customers;
  id  |             name
------+-------------------------------
    1 | Brenda Alves
    2 | Sra. Isabelly Câmara
    3 | Cauã Rocha
    4 | Dra. Aurora Pastor
    5 | Ana Beatriz Alves
    [...]

```

## Subindo app (backend)
docker compose --profile backend up --build

## Zerando o lab

```bash
docker compose --profile ds_generator down -v
docker compose down -v
