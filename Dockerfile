FROM python:3.11-slim-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg git curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app/

RUN pip3 install --no-cache-dir -U pip \
    && pip3 install --no-cache-dir -U -r requirements.txt

CMD ["bash", "start"]
