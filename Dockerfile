FROM python:3.11-slim-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ffmpeg git curl ca-certificates gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && node --version && npm --version

WORKDIR /app
COPY . /app/

RUN pip3 install --no-cache-dir -U pip \
    && pip3 install --no-cache-dir -U -r requirements.txt

CMD ["bash", "start"]
