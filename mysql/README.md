# General Infra desing
```
┌──────────┐         ┌────────────────┐
│  MySQL   │ ─────── │  SysBench      │
│          │         │ (load / test)  │
└────┬─────┘         └────────────────┘
     │ metrics
┌────▼────────────┐
│ mysqld_exporter │
└────┬────────────┘
     │
┌────▼─────┐       ┌─────────┐
│Prometheus│◀────▶│ Grafana │
└──────────┘       └─────────┘
```

# Fluxo resumido

SysBench → gera carga / executa benchmarks

MySQL → processa queries

mysqld_exporter → expõe métricas do MySQL

Prometheus → coleta métricas

Grafana → visualiza tudo (QPS, latência, locks, buffer pool, etc.)


Você inicia esse lab com:
```
$ docker compose up -d
```

# Acessos padrão

MySQL → localhost:3306              | user appuser, pass: apppass

Prometheus → http://localhost:9090

Grafana → http://localhost:3000     | user: admin, pass: admin


# Rodando o  SysBench

```
docker compose --profile bench up -d
```

O fluxo do sysbench é: prepare > run > cleanup

```
docker exec -it sysbench bash

sysbench \
  /usr/share/sysbench/oltp_write_only.lua \
  --mysql-host=mysql \
  --mysql-user=bench \
  --mysql-password=benchpass \
  --mysql-db=appdb \
  --threads=4 \
  --time=60 \
  --report-interval=5 \
  run


-- Restartando db instance para limpar cache
docker restart mysql

-- Rodando teste customizado, commit every N:

sysbench \
  /work/commit_every_n.lua \
  --mysql-host=mysql \
  --mysql-user=bench \
  --mysql-password=benchpass \
  --mysql-db=appdb \
  --threads=4 \
  --events=0 \
  --time=60 \
  --report-interval=10 \
  --inserts-per-tx=1 \
  run

```

## Zerando o lab:

```
docker compose down -v
rm -rf data/mysql data/grafana
docker compose up -d
```