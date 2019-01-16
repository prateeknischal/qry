#!/usr/bin/env bash
ZBAR=`which zbarimg`

if [ -z "$ZBAR" ]
then
  echo "[error] 'zbar' not found, please install zbar"
  exit 1
fi

if [ -z "$1" ]
then
  echo "Usage: decode.sh QRCode_image_file"
  exit 1
fi
# decode qrcode and get the secret
secret=$($ZBAR $1 2>/dev/null| \
  grep secret | \
  python3 -c 'from urllib.parse import parse_qs, urlparse, unquote; print(parse_qs(urlparse(unquote(input())).query)["secret"][0])')

python3 totp.py $secret
