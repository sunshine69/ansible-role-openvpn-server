#!/bin/bash

## Generate VPN config file from template

source vars

[ -z "$1" ] && echo "Usage: $0 [key_name]" && exit 1
[ -z "$2" ] && echo "Usage: $0 [key_name]" && exit 1

yes | ./build-key $1


cp vpn/template.ovpn generated/${1}.ovpn
echo "<ca>"  >> generated/${1}.ovpn
cat $KEY_DIR/ca.crt >> generated/${1}.ovpn
echo "</ca>" >> generated/${1}.ovpn

echo "<tls-auth>" >> generated/${1}.ovpn
cat $KEY_DIR/ta.key >> generated/${1}.ovpn
echo "</tls-auth>" >> generated/${1}.ovpn

echo "<cert>" >> generated/${1}.ovpn
# Remove the cert info - header part
openssl x509 -in $KEY_DIR/$1.crt -out /tmp/$$.pem
cat /tmp/$$.pem >> generated/${1}.ovpn
rm -f /tmp/$$.pem
echo "</cert>" >> generated/${1}.ovpn
echo "<key>" >> generated/${1}.ovpn
cat $KEY_DIR/$1.key >> generated/${1}.ovpn
echo "</key>" >> generated/${1}.ovpn

useradd $1
echo "$1:$2" | chpasswd
