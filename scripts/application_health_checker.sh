#!/bin/bash
# Application Health Checker
# Checks if an application is running on port 4499

URL="http://localhost:4499"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" $URL)

if [ $STATUS -eq 200 ]; then
  echo "Application is UP"
else
  echo "Application is DOWN (status: $STATUS)"
fi
