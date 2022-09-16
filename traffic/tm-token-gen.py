# encoding: utf-8

import sys, os
import hashlib

PRODUCT_UUID_FILE = '/sys/class/dmi/id/product_uuid'
WINDOWS_UUID = 'WINDOWS_UUID'

profiles = os.environ.get('PROFILE')
private_secret = os.environ.get('PROFILE_SECRET')

if not profiles:
    print('ERROR: variable PROFILE no definida')
    sys.exit(-1)
if not private_secret:
    print('ERROR: variable PROFILE_SECRET no definida')
    sys.exit(-1)

host_uuid = None
if sys.platform.startswith('win'):
    host_uuid = WINDOWS_UUID

if not host_uuid:
    if not os.path.isfile(PRODUCT_UUID_FILE):
        print('ERROR: Fichero UUID no existe')
        sys.exit(-1)
    with open(PRODUCT_UUID_FILE, 'rt') as f:
        host_uuid = f.read().strip()

profiles = [p.strip() for p in profiles.split(',')]
profiles.sort()

payload = '{}_{}_{}'.format(host_uuid, ','.join(profiles), private_secret)
#print('Payload:', payload)
print(hashlib.sha3_256(bytes(payload, encoding='utf8')).hexdigest())
