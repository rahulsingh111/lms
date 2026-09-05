FROM python:3.11-slim-bookworm AS builder

WORKDIR /build
COPY requirements.txt .
RUN mkdir -p /install \
    && pip install --no-cache-dir \
       --prefix=/install \
       -r requirements.txt


FROM cgr.dev/chainguard/python:latest
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
