#!/bin/bash

export APPID=$1
export FOLDERID=$2

echo -e "\nChecking APPID $APPID and userdata $FOLDERID"

echo -e "\n========================="
echo -e "AppCache:"
echo -e "========================="
ls -la ~/.steam/steam/appcache/librarycache/ | grep $APPID

echo -e "\n========================="
echo -e "userdata grid:"
echo -e "========================="
ls -la ~/.steam/steam/userdata/$FOLDERID/config/grid/  | grep $APPID

