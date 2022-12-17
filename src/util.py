import time
import logging
import requests
import socket
from datetime import datetime


def date_is_today(dt):
	'''
	Return True if given date equals today's date.
	'''
	return dt.date() == datetime.today().date()

def get_time_exceeded(dt):
	'''
	Returns the time exceeded since given datetime until now
	as formatted string.

	Return:
		Exceeded (now-dt)	Example return value
		-------------------------------------
		< 1 min			'3 seconds'
		< 1 hour		'24 minutes'
		< 1 day			'5 hours'
		< 2 days		'yesterday'
		< 7 days		'2 days'
		> 6 days		'2022-05-14 23:54'
	'''
	now    = datetime.now()
	ts_now = time.mktime(now.timetuple())
	ts_dt  = time.mktime(dt.timetuple())

	secDiff  = int(ts_now - ts_dt)
	minDiff  = int(secDiff / 60)
	hourDiff = int(minDiff / 60)
	dayDiff  = now.day-dt.day
	dayDiff2 = (now - dt.replace(tzinfo=None)).days

	def fmt_timediff(val, typ):
		if val == 1:
			return str(val) + ' ' + typ
		else:
			return str(val) + ' ' + typ + 's'

	if secDiff < 60:
		return fmt_timediff(secDiff, "second")
	elif minDiff < 60:
		return fmt_timediff(minDiff, "minute")
	elif hourDiff < 24 and dayDiff == 0:
		return fmt_timediff(hourDiff, "hour")
	elif dayDiff == 1 and dayDiff2 == 0:
		return "yesterday"
	else:
		return fmt_timediff(dayDiff2, "day")


#d = datetime.strptime('%Y-%m-%d %H:%M', '2021-06-16 17:44')
#d = datetime.strptime('2022-11-17 17:44', '%Y-%m-%d %H:%M')
#d = datetime.strptime('2021-06-16 17:44', '%Y-%m-%d %H:%M')
#print(get_time_exceeded(d))


def internet_is_reachable(host="8.8.8.8", port=53, timeout=3):
	"""
	Check if we can connected to given host and service.

	Args:
		host: Host to connect (8.8.8.8 | google-public-dns-a.google.com)
		port: Port to connect (53/tcp | domain (DNS/TCP))
		timeout: Connection timeout
	"""
	try:
		socket.setdefaulttimeout(timeout)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
		return True
	except socket.error as ex:
		return False


def page_is_reachable(url):
	'''
	Return True if given url is reachable and host returned 200.
	This will send a HEAD request.
	'''
	try:
		req = requests.head(url)
		if req.status_code == 200:
			return True
		else:
			logging.warning("Got invalid status code {} from {}"
					.format(req_status.code, url))
			return False

	except requests.exceptions.ConnectionError as ce:
		logging.warning("Host {} is not reachable or internet is down :-("
				.format(url))
		return False

