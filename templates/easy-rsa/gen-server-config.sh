#!/bin/bash

echo "First edit vars for initial setup"
read
vim vars

. vars >/dev/null 2>&1

if [ ! -f keys/dh2048.pem ]; then
	echo "Generate dh2048.pem key"
	openssl dhparam -out keys/dh2048.pem 2048
	openvpn --genkey --secret keys/ta.key
	./build-ca
fi

if [ -f /etc/openvpn/server.conf ]; then
	echo "Reset current server config at /etc/openvpn/server.conf ? y/n"
	read ans
	if [ "$ans" = "y" ]; then
		echo "Going to remove existing openvpn config"
		( cd /etc/openvpn/ && rm -f server.* ca.crt ta.key dh*.pem crl.pem )
	fi	
fi

if [ ! -f /etc/openvpn/server.conf ]; then
    ./build-key-server server
    ./make-crl crl.pem
    cp -a vpn/auth.py /etc/openvpn/scripts/
    cp -a vpn/auth.py /etc/openvpn/scripts/
	cp -a keys/crl.pem /etc/openvpn/crl.pem
	cp -a vpn/server.conf /etc/openvpn/server.conf
	cp -a keys/server.key /etc/openvpn/server.key
	cp -a keys/server.crt /etc/openvpn/server.crt
	cp -a keys/dh2048.pem /etc/openvpn/dh2048.pem
	cp -a keys/ca.crt /etc/openvpn/ca.crt
	cp -a keys/ta.key /etc/openvpn/ta.key
    mkdir /etc/openvpn/ccd
fi

echo "Hit enter to edit /etc/openvpn/server.conf to suit your need"
read
vim /etc/openvpn/server.conf
echo "Also edit /etc/default/openvpn to select which server to start"
read
vim /etc/default/openvpn
systemctl daemon-reload
systemctl start openvpn
systemctl enable openvpn

echo "Edit the vpn template to update the server IP and stuff"
read
vim vpn/template.ovpn