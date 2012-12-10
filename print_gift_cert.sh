#! /bin/sh

sed -e "s/REPLACE_SERIAL/$1/g; s/REPLACE_DENOM/$2/g; s/REPLACE_RJUST_DENOM/$3/g" moneymaster.ps |\
lp -o media=Custom.3.125x7.65in
