import requests
import json
import csv
import time
from os.path import expanduser
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

# Configuration


parser = configparser.ConfigParser()
parser.read(expanduser('~') + '/.storagegrid_admin')
hostname = parser.get('config', 'hostname')
username = parser.get('config', 'username')
password = parser.get('config', 'password')

base_url = 'https://' + hostname + '/api/v1'

# Get Authorization token
data = json.dumps({'username': username, 'password': password}) 
req = requests.post(base_url + "/authorize", data, verify=False)
token = json.loads(req.text)['data']

# Get all accounts in the GRID
req = requests.get(base_url + "/grid/accounts", headers={'Authorization': 'Bearer ' + token}, verify=False)
accounts = req.json()['data']

# Get usage for all accounts
for _ in accounts:
    stats = []  
    id = _['id']  
    name = _['name']  
    req = requests.get(base_url + "/grid/accounts/" + id + "/usage", headers={'Authorization': 'Bearer ' + token}, verify=False)
    usage = req.json()['data']
    bytes_used = str(usage['dataBytes'])
    objects_used = str(usage['objectCount'])
    stats.append({'bytes_used': bytes_used, 'objects_used': objects_used});
    filename = name + '.csv'
    f = open(filename, 'a')
    try:
       writer = csv.writer(f)
       #writer.writerow(('Datum', 'Used bytes', 'Used objects'))
       for _ in stats:
           writer.writerow((time.strftime("%Y-%m-%d_%H-%M-%S"),bytes_used,objects_used))
    finally:
	    f.close()


