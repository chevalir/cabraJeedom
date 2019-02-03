#/bin/bash

#  arg $1 possible values :

# Ch B-R lampe rouge = 2
# Chambre M          = 7
# Salle ˆ Manger     = 8
# Salon Appliques    = 9
# Salon table base   = 1
# Salon Lampe iMac   = 0

#  arg $2 possible values :
# command on  off


export CHACON_GPIO=6
export CHACON_SENDER_ID=666


/var/www/pidomogpio/newGpioAndRadio $2 $CHACON_GPIO $CHACON_SENDER_ID $1
echo $2
