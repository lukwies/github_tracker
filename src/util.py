from datetime import datetime
import time

def date_is_today(dt):
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
	elif dayDiff == 1:
		return "yesterday"
	else:
		return fmt_timediff(dayDiff2, "day")

