#!/bin/bash

sudo cp -R /home/pi/pidomo/jeedom/cabratt /var/www/html/plugins/.
sudo chown -R www-data:www-data /var/www/html/plugins/cabratt
sudo chmod -R 775 /var/www/html/plugins/cabratt