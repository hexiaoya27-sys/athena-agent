FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    --trusted-host pypi.tuna.tsinghua.edu.cn

COPY athena/ ./athena/

RUN mkdir -p /app/logs

EXPOSE 8000

CMD ["uvicorn", "athena.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
