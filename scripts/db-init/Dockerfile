FROM python:3.11-alpine

RUN apk add --no-cache postgresql-client \
  && pip install --no-cache-dir pymongo

WORKDIR /app

# Copy init scripts
COPY scripts/init_postgres.sql /app/init_postgres.sql
COPY scripts/init_mongodb.py /app/init_mongodb.py
COPY scripts/db-init/entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

ENV POSTGRES_HOST=postgres \
    POSTGRES_DB=userdb \
    POSTGRES_USER=postgres \
    MONGO_HOST=mongodb \
    MONGO_PORT=27017

ENTRYPOINT ["/app/entrypoint.sh"]
