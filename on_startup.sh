#!/bin/sh

ALEMBIC=/usr/local/bin/alembic

if [ $AUTO_MIGRATE = "true" ]; then
    echo "INFO  Running database migrations..."
    $ALEMBIC --raiseerr upgrade head
else
    echo "INFO  Auto migrate is disabled, not running database migrations."
fi

if [ $($ALEMBIC heads | wc -l) -ne 1 ]; then
    echo "WARNING Multiple migration heads found:"
    $ALEMBIC heads
fi

echo "INFO  Checking if database is at current migration: $($ALEMBIC heads)."
if ! $ALEMBIC current | grep -q '(head)'; then
    echo "WARNING Database migration (`$ALEMBIC current`) is not up to date with head."
else
    echo "INFO  Database is at right migration."
fi

echo "INFO  Starting application..."

echo "INFO Executing $@"
exec $@
