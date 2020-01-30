import requests
from datetime import (datetime, timezone)
from random import randint

CLIENT_ID = 'Client1'
MIN_VALUE = 0
MAX_VALUE = 150

DEBUG = False
API_URL = 'http://35.204.56.226/api/data/'
API_URL_DEVELOP = 'http://127.0.0.1:8000/api/data/'
VALUES_FILE_NAME = 'values.txt'


def init_payload():
	'''
	Creates payload object and populates it with data values thaw were not posted
	'''
	payload = {"clientId": CLIENT_ID, "data": []}

	# Get all not posted data
	with open(VALUES_FILE_NAME, 'r') as f:
		for line in f.readlines():
			(timestamp, value) = line.strip().split('---')
			print(timestamp, value)
			payload['data'].append({'timestamp': timestamp, 'value': int(value)})

	return payload


def generate_new_row():
	'''
	Generates new row of data 
	'''
	return { "timestamp": str(datetime.now(timezone.utc)), "value": randint(MIN_VALUE, MAX_VALUE) }



def post_data():
	'''
	Tries to post data to server. If not succeed saves data values to backup file.
	'''
	payload = init_payload()

	# add new value
	payload['data'].append(generate_new_row())

	print(payload['data'])

	succeed = False
	try:
		response = requests.post(API_URL_DEVELOP if DEBUG else API_URL, json=payload, timeout=3)
		if response.ok:
			succeed = True

			# Clear backup data values
			open(VALUES_FILE_NAME, 'w').close()

			print('Succeed!')
		else:
			print(f'Request failed! Status code: {response.status_code}')
	except:
		print('Request failed! Something wrong.')
	
	# Write to values.txt if something wrong
	if not succeed:
		with open(VALUES_FILE_NAME, 'a') as f:
			lastVaue = payload['data'].pop()
			f.write("{}---{}\n".format(lastVaue['timestamp'], str(lastVaue['value'])))


post_data()
