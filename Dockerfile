FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim


RUN useradd --create-home appuser
WORKDIR /app


COPY --from=builder /install /usr/local


COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 5000

CMD ["python", "run.py"]
