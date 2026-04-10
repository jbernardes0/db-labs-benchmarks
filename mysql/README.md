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

-- No banco
docker exec -it mysql bash

CREATE USER 'bench'@'%' 
IDENTIFIED WITH mysql_native_password 
BY 'benchpass';

GRANT ALL PRIVILEGES ON appdb.* TO 'bench'@'%';
FLUSH PRIVILEGES;

-- O fluxo do sysbench é: prepare > run > cleanup

docker exec -it sysbench bash

sysbench \
  /usr/share/sysbench/oltp_write_only.lua \
  --mysql-host=mysql \
  --mysql-user=bench \
  --mysql-password=benchpass \
  --mysql-db=appdb \
  --tables=4 \
  --table-size=100000 \
  prepare


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

```

## Zerando o lab:

```
docker compose down -v
rm -rf data/mysql data/grafana
docker compose up -d
```