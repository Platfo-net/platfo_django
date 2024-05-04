#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 <<-EOSQL
    CREATE ROLE platfo WITH LOGIN PASSWORD 'F23jfyq$341asDF';
    CREATE DATABASE platfo_django;
    GRANT ALL PRIVILEGES ON DATABASE platfo_django TO platfo;
EOSQL
