# syntax=docker/dockerfile:1.6
ARG TORCH_IMAGE=pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime
FROM ${TORCH_IMAGE} as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    git build-essential curl ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY pyproject.toml README.md ./
COPY sdf/ ./sdf/
COPY tests/ ./tests/

RUN python -m pip install --upgrade pip && pip install -e .[dev]

EXPOSE 9000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "9000"]
