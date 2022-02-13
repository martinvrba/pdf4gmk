FROM debian:bullseye-slim

RUN mkdir -p /app/output

COPY requirements.txt /app/

RUN apt-get update && apt-get install -y poppler-utils python3-pip

RUN python3 -m pip install -U pip && python3 -m pip install -r /app/requirements.txt

COPY pdf4gmk.py /app/

WORKDIR /app/output

ENTRYPOINT ["python3", "/app/pdf4gmk.py"]
