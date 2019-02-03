#!/bin/bash

sudo cp -R /home/pi/pidomo/jeedom/template /var/www/html/plugins/.
sudo chown -R www-data:www-data /var/www/html/plugins/template
sudo chmod -R 775 /var/www/html/plugins/template