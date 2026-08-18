FROM python:3.12-slim

LABEL org.opencontainers.image.title="SOC Detection Engineering Lab"
LABEL org.opencontainers.image.description="Synthetic CrowdStrike and Proofpoint SOC detection lab"
LABEL org.opencontainers.image.licenses="MIT"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SOC_DB_PATH=/data/soc.db \
    SOC_DATASET_PATH=/app/data/events.jsonl

WORKDIR /app
RUN useradd --create-home --uid 10001 soc && mkdir -p /data && chown -R soc:soc /data
COPY --chown=soc:soc . .
USER soc
EXPOSE 8080
ENTRYPOINT ["python", "-m", "soclab"]

