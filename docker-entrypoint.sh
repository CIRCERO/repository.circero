#!/bin/bash

# Copy shared files and create the initial database on first run
if [[ ! -f "/database/favorites.db" ]]; then
  cp -R /database.template/* /database
  
  php /app/src/protected/yiic.php createinitialdatabase
  echo "Created initial database"
fi

# Set permissions and apply database migrations every time the container starts
php /app/src/protected/yiic.php setpermissions
chmod ugo+w /shared/*
php /app/src/protected/yiic.php migrate --interactive=0

# Indicate whether a reverse-proxy.conf was found or not to help debugging
if [[ -f "/database/config/apache2/reverse-proxy.conf" ]]; then
  echo "Using reverse proxy configuration from /database/config/apache2/reverse-proxy.conf"
fi

apache2ctl -D FOREGROUND
