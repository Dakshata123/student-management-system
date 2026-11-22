
#!/bin/bash

# Docker container name
CONTAINER="student-app"

# SQLite database path inside container
DB_PATH="/data/students.db"

# Your actual S3 bucket name
BUCKET="student-management-backups-dakshata-2026"

# Local backup directory
BACKUP_DIR="$HOME/backups"

mkdir -p "$BACKUP_DIR"

# Generate timestamp
DATE=$(date +%Y%m%d-%H%M%S)

# Backup file name
BACKUP_FILE="students-backup-$DATE.tar.gz"

echo "Starting student database backup..."

# Create consistent SQLite backup
docker exec "$CONTAINER" \
  python -c "import sqlite3; src=sqlite3.connect('$DB_PATH'); dst=sqlite3.connect('/tmp/backup.db'); src.backup(dst); dst.close(); src.close()"

if [ $? -ne 0 ]; then
    echo "ERROR: Database backup failed!"
    exit 1
fi

# Copy database out of container
docker cp "$CONTAINER:/tmp/backup.db" "$BACKUP_DIR/backup.db" || exit 1

# Create compressed archive
tar -czf "$BACKUP_DIR/$BACKUP_FILE" \
  -C "$BACKUP_DIR" backup.db || exit 1

# Remove temporary database
rm -f "$BACKUP_DIR/backup.db"

echo "Uploading backup to S3..."

# Upload archive to S3
aws s3 cp "$BACKUP_DIR/$BACKUP_FILE" \
  "s3://$BUCKET/backups/$BACKUP_FILE" || {
    echo "ERROR: S3 upload failed!"
    exit 1
}

echo "Backup completed successfully!"
echo "Backup file: $BACKUP_FILE"

