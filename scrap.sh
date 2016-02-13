#!/bin/bash
PATH=/opt/someApp/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

cd /home/anyjava/_dev/scrapMagnet
python3 /home/anyjava/_dev/scrapMagnet/scrap.py >> /home/anyjava/_dev/scrapMagnet/log/scrap.log
python3 /home/anyjava/_dev/scrapMagnet/autodown.py >> /home/anyjava/_dev/scrapMagnet/log/autodown.log
