#!/usr/bin/env bash
# Nightly dump of the listmonk and Umami databases. Lives in /opt/backup on the VPS.
# Scheduled by /etc/cron.d/giuseppecorso-backup. Keeps the last KEEP_DAYS days.
set -euo pipefail

DEST=/var/backups/giuseppecorso
KEEP_DAYS=7
STAMP=$(date +%Y%m%d-%H%M%S)

mkdir -p "$DEST"
chmod 700 "$DEST"

dump() { # container, db user, db name
  local out="$DEST/$3-$STAMP.sql.gz"
  docker exec "$1" pg_dump -U "$2" "$3" | gzip > "$out.tmp"
  # an empty or truncated dump must not replace a good one
  [ "$(gzip -dc "$out.tmp" | head -c 200 | wc -c)" -gt 100 ] || { echo "dump $3 is empty" >&2; rm -f "$out.tmp"; exit 1; }
  mv "$out.tmp" "$out"
  chmod 600 "$out"
}

dump listmonk_db listmonk listmonk
dump umami_db umami umami

find "$DEST" -name '*.sql.gz' -mtime +"$KEEP_DAYS" -delete
echo "$(date -Is) backup ok: $(ls "$DEST" | wc -l) files, $(du -sh "$DEST" | cut -f1)"
