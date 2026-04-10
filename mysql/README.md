# General Infra desing
```
┌──────────┐         ┌────────────────┐
│  MySQL   │ ─────── │  MySQL Bench   │
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

MySQL Bench → gera carga / executa benchmarks
MySQL → processa queries
mysqld_exporter → expõe métricas do MySQL
Prometheus → coleta métricas
Grafana → visualiza tudo (QPS, latência, locks, buffer pool, etc.)

Você inicia esse lab com:
$ docker compose up -d


# Acessos padrão

MySQL → localhost:3306              | user appuser, pass: apppass
Prometheus → http://localhost:9090
Grafana → http://localhost:3000     | user: admin, pass: admin

# MySQL Bench
```
docker exec -it mysqlbench bash

mysql \
  -h mysql \
  -u appuser \
  -papppass \
  appdb

mysqlslap \
  --host=mysql \
  --user=appuser \
  --password=apppass \
  --concurrency=10 \
  --iterations=5 \
  --auto-generate-sql

```