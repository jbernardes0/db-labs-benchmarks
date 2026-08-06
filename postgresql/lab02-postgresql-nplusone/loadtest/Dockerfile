FROM debian:bookworm-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    wrk \
    lua5.4 \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*


WORKDIR /wrk

ENTRYPOINT ["sh", "-c"]
CMD ["sleep infinity"]