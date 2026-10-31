#!/bin/sh
# Creates Mattermost's own database and role next to Heimdall's on first boot.
set -eu

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
  -v mm_password="$MATTERMOST_DB_PASSWORD" <<'SQL'
CREATE ROLE mattermost LOGIN PASSWORD :'mm_password';
CREATE DATABASE mattermost OWNER mattermost;
SQL
