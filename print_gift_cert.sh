#! /bin/sh

sed -e "s/REPLACE_SERIAL/$1/g; s/REPLACE_DENOM/$2/g; s/REPLACE_RJUST_DENOM/$3/g" moneymaster.ps > /var/www/certs/$4.ps
lp -o media=Custom.3.125x7.65in /var/www/certs/$4.ps
gs -sDEVICE=pngmono -sOutputFile=/var/www/certs/$4.png /var/www/certs/$4.ps
