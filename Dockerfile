FROM python:3.13-slim
WORKDIR /app
RUN apt-get update -y \
 && apt-get install -y --no-install-recommends ffmpeg curl unzip git \
 && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["bash", "start"]
