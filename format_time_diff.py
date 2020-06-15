 

def format_time_from_now(now, other_time): 

  total_secs = int((now - other_time).total_seconds())
  is_future = total_secs < 0
  total_secs = abs(total_secs)
  total_minutes, secs = divmod(total_secs, 60)
  total_hours, minutes = divmod(total_minutes, 60)
  total_days, hours = divmod(total_hours, 24)

  if total_hours < 1:
    result = '{minutes}m'.format(**locals())
  elif total_hours < 4:
    result = '{hours}h {minutes}m'.format(**locals())
  elif now.date() == other_time.date():
    result = other_time.strftime('%I:%M %p')
  elif is_future and total_days < 6:
    result = other_time.strftime('%a %I:%M %p')
  else:  
    result = other_time.strftime('%a %b %d %I:%M %p')

  if is_future: sign = '-'
  else: sign = '+'

  return sign + result;


if __name__ == '__main__':
  datetimeFormat = '%Y-%m-%d %H:%M:%S'

  now = datetime.datetime.strptime("2020-06-14 13:17:00", datetimeFormat)
  time_strs = (
    "2020-06-03 03:17:00",
    "2020-06-13 13:17:00",
    "2020-06-13 23:17:00",
    "2020-06-14 19:17:00",
    "2020-06-14 9:17:00",
    "2020-06-14 11:17:00",
    "2020-06-14 12:17:00",
    "2020-06-14 13:15:54",
    "2020-06-14 13:16:04",
    "2020-06-14 13:17:00",
    "2020-06-14 13:17:18",
    "2020-06-14 13:17:38",
    "2020-06-14 13:18:38",
    "2020-06-14 14:17:00",
    "2020-06-14 15:17:00",
    "2020-06-17 15:17:00",
    "2020-06-20 9:17:00",
    "2020-06-20 20:17:00",
    "2020-06-21 9:17:00",
    "2020-06-21 19:17:00",
    "2020-06-22 15:17:00",
    "2020-06-27 15:17:00",
    "2020-07-27 15:17:00",
  )

  for time_str in time_strs:
    other_time = datetime.datetime.strptime(time_str, datetimeFormat)
    print format_time_from_now(now, other_time)
