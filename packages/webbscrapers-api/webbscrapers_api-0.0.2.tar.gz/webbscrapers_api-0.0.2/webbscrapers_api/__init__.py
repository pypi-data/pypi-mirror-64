import requests
from datetime import datetime
from typing import List

def getReports(authorization_token: str, startDateTime: datetime, endDateTime: datetime, keyTerms: List[str]=[], location: str='', timezone: str=None):
	newStartTime = datetime(startDateTime.year, startDateTime.month, startDateTime.day, startDateTime.hour, startDateTime.minute, startDateTime.second)
	newEndTime = datetime(endDateTime.year, endDateTime.month, endDateTime.day, endDateTime.hour, endDateTime.minute, endDateTime.second)
	payload = {}
	if (len(keyTerms) > 0):
		payload = {
			'startDateTime': newStartTime.isoformat(),
			'endDateTime': newEndTime.isoformat(),
			'keyTerms': ','.join(keyTerms),
			'location': location,
			'timezone': timezone
		}
	else:
		payload = {
			'startDateTime': newStartTime.isoformat(),
			'endDateTime': newEndTime.isoformat(),
			'location': location,
			'timezone': timezone
		}
	
	headers = {
		'Authorization': 'Bearer ' + authorization_token
	}
	return requests.get('https://webbscrapers.live/reports', params=payload, headers=headers).json()

def getStatistics(authorization_token):
	headers = {
		'Authorization': 'Bearer ' + authorization_token
	}

	return requests.get('https://webbscrapers.live/statistics', headers=headers)

def getCovid19Cases(authorization_token):
	headers = {
		'Authorization': 'Bearer ' + authorization_token
	}

	return requests.get('https://webbscrapers.live/covid-19', headers=headers)

def login(email, password):
	params = {
		'email': email,
		'password': password
	}

	return requests.get('https://webbscrapers.live/login', params=params)

def register(email, password):
	data = {
		'email': email,
		'password': password
	}

	return requests.post('https://webbscrapers.live/register', data=data)
