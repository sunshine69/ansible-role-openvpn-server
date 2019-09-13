#!/bin/bash -ex

# start from this script
source vars >/dev/null 2>&1

if [ "$RESET_OPENVPN" = "y" ]; then
    ./clean-all
fi

mkdir keys generated >/dev/null 2>&1 || true

if [ ! -f keys/dh2048.pem ]; then
	echo "Generate dh2048.pem key"
	openssl dhparam -out keys/dh2048.pem 2048
	openvpn --genkey --secret keys/ta.key
	./build-ca openvpn-ca
fi

if [ -f /etc/openvpn/server.conf ]; then
	if [ "$RESET_OPENVPN" = "y" ]; then
		echo "Going to remove existing openvpn config"
		( cd /etc/openvpn/ && rm -f server.* ca.crt ta.key dh*.pem crl.pem )
        systemctl stop openvpn || true
	fi
fi

if [ ! -f /etc/openvpn/server.conf ]; then
    yes | ./build-key-server server
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
    mkdir /etc/openvpn/ccd >/dev/null 2>&1 || true
fi
