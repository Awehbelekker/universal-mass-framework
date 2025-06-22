#!/bin/bash
# Start script for MASS Framework

# Start nginx in background
nginx -g "daemon off;" &

# Start uvicorn
exec uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --access-log
