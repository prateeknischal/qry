# QRy - The command line TOTP generator

**qry** is an command line Time based OTP generator that can scan Google Authenticator QR codes and generate OTPs based on it. The TOTP is an implementation of the RFC4226 that describes HMAC based OTP. The time component is taken from the TOTP RFC, but currently it only supports HMAC-SHA1, the original OTP spec which also the most widely used.

```
$ python3 qry.py --help
usage: QRy - TOTP generator [-h] {reg,gen} ...

positional arguments:
  {reg,gen}   operations

optional arguments:
  -h, --help  show this help message and exit
```

### Requirements
This tool uses a command line tool called `zbar` which is a library used to process QR Codes. Setting up `zbar` is tedious in OSX devices, which is why using this to maintain cross compatibility.

To install `zbar`, you can use your favourite package manager and just do `install zbar`.
eg: `brew install zbar` or `apt-get install zbar`

#### Python dependencies
* cryptography

### Usage
The flow is such.
1. Register the QR Code
```
$ python3 qry.py reg --config /path/to/qry.json --qrcode /path/to/qrcode.png
```
This step will create a file called `qry.json` by default which contains your secret from the QR Code and is encrypted using a password which will be asked during registration.

2. Generate
```
python3 qry.py gen --config /path/to/qry.json
```
This step will prompt user for the password to decode the secret in the file `qry.json`. If the password is correct it will generate an OTP and print it on the console.


#### TODO
1. Proper error handling, messages to stderr and error code propagation
2. Using a `~/.qry/` storage location instead of the project root.
3. Caching the secret/password in memory for some time, user does not have to enter password at every attempt
4. Daemonize it, so that the above password caching works and you don't need to invoke the script at evert attempt
