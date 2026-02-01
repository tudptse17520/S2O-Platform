#!/bin/bash
docker run -d \
  --name s2o-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=1234 \
  -e POSTGRES_DB=s2o_db \
  -p 5433:5432 \
  pgvector/pgvector:pg16
