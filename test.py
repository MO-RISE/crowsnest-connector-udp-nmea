from datetime import datetime
import pytz

d = "2022-10-20"
t = "06:48:29.010000"

datetime_str = d +" "+ t

print(datetime_str)
datetime_object = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S.%f")
datetime_object = pytz.utc.localize(datetime_object)

print(datetime_object)