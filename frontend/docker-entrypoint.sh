#!/bin/sh

echo "API_PROTOCOL=$API_PROTOCOL"
echo "API_HOST=$API_HOST"
echo "API_PORT=$API_PORT"
echo "API_BASE_PATH=$API_BASE_PATH"
echo "BASE_URL=$BASE_URL"

envsubst < /usr/share/nginx/html/config.template.js > /usr/share/nginx/html/config.js

exec "$@"