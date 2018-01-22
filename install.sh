#!/bin/bash

NAME="insider"

if [ "$EUID" -ne 0 ]
then
  echo "ERR: Please run as root"
  exit 1
fi

grep -q "sfera" /etc/passwd
if [ $? -ne 0 ]
then
  useradd -U -b '/usr/local' sfera
fi


mkdir -p /usr/local/sfera/$NAME
cp -R * /usr/local/sfera/$NAME

mv /usr/local/sfera/$NAME/$NAME.service /lib/systemd/system/$NAME.service
systemctl daemon-reload
systemctl enable $NAME
systemctl start $NAME


if [ ! -e "/etc/sudoers.d/sfera" ]
then
  echo "sfera   ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/sfera
  chmod 400 /etc/sudoers.d/sfera
fi


pip3 install configparser paho-mqtt pymongo

apt install -y mosquitto 

python3 -c "import sferaconfig; sferaconfig.addDefaultConfig()"
systemctl start $NAME
