FROM python:3.12.3

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    ncbi-blast+ \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /viro-3d-api

COPY ./requirements.txt /viro-3d-api

COPY ./.env /viro-3d-api

RUN pip install --no-cache-dir --upgrade -r /viro-3d-api/requirements.txt

COPY ./app /viro-3d-api/app

RUN makeblastdb -in ./app/blast_db/viro3d_seq_db.fas -dbtype prot

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]