FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN apt update && \
    apt install sqlite3

COPY requirements.txt .

RUN python3 -m venv .venv && \
    .venv/bin/pip install --upgrade pip && \
    .venv/bin/pip install -r requirements.txt

COPY . .

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 5004

CMD ["python3","-u","bootstrap.py"]
