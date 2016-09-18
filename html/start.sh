#!/bin/sh

python app.py >> /var/log/webserver.log 2>&1 &
