# jbernardes0's Database Labs & Benchmarks

Hands-on database labs and performance benchmarks focused on real-world scenarios.

You know, we tend to do ad‑hoc testing all the time, and sometimes we catch ourselves testing the same thing for the tenth time. So I thought: why not organize this? And that’s how this repo came about.

This repository contains my practical experiments exploring database behavior under load, throughput limits, and system bottlenecks across different engines and infrastructures.

---

## 🚀 Scope

- Database performance under stress
- Throughput and concurrency analysis
- Transaction log impact (redo/binlog/WAL)
- Query plan behavior and regressions
- Infrastructure limits (CPU, IOPS, network)
- Cloud vs on-prem comparisons

---

## 🧠 Technologies

- MySQL (InnoDB)
- PostgreSQL
- MongoDB
- Oracle
- AWS RDS / Aurora
- Docker-based lab environments
- Sysbench and custom workload generators

---

## 📂 Structure
  mysql/ postgres/ mongo/ aws/

Each lab includes:

- *Context* → what is being tested
- *Setup* → how to reproduce
- *Workload* → type of load applied
- *Metrics* → DBLoad, latency, throughput, waits
- *Findings* → what actually happened
- *Takeaways* → practical conclusions

---

## 📊 Key Focus Areas

### Database Load
Understanding how load builds up and how it relates to CPU, waits and concurrency.

### Major DB internals Bottlenecks
How the database internal components impact throughput and response time.

### Plan Instability
Effects of cardinality changes and statistics on execution plans.

### Throughput Limits
How storage configuration affects performance.

---

## 🧪 Philosophy

This is not theory.

All experiments are designed to:
- be reproducible
- reflect production-like conditions
- expose real bottlenecks
- provide actionable insights

---

## ⚠️ Notes

- Results may vary depending on environment and configuration.
- Some tests intentionally push systems to failure scenarios.

---

## 👨‍💻 Author

[@jbernardes0](https://www.linkedin.com/in/jlbernardes/?locale=en-US)
Database Engineer focused on performance, reliability and large-scale systems.