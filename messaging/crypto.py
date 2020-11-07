from django.conf import settings
from Crypto.Cipher import AES
import hashlib, random
import base64


def __random5():
    return bytes(''.join(map(chr,random.sample(range(255),5))), 'utf-8')


def __fill():
    return hashlib.sha512(__random5()).digest()


def __cipher():
    key=hashlib.sha256(bytes(settings.SECRET_KEY, 'utf-8')).digest()
    return AES.new(key, AES.MODE_CBC, settings.MESSAGE_IV)


def encrypt(data):
    FILL=__fill()
    enc=__cipher().encrypt(bytes(data, 'utf-8')+b'|'+FILL[len(data)+1:])
    return enc.hex()


def decrypt(data):
	data=bytes.fromhex(data)
	return __cipher().decrypt(data).split(b'|')[0].decode('utf-8')