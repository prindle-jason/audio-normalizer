FROM python:3.11-slim

LABEL maintainer="Jason Prindle <prindle.jason@gmail.com>" \
        version="1.0" \
        description="Batch audio normalizer using ffmpeg-normalize"

RUN apt-get update && \
    apt-get install -y \
        ffmpeg \
        --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY audio_normalizer.py .

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd appuser
USER appuser

CMD ["python", "audio_normalizer.py"]