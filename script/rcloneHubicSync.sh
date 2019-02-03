#!/usr/bin/env bash

sudo runuser -l pi -c 'rclone -vv sync /var/www/html/backup hremote:default/jeedom/backup'

