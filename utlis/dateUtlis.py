
import time
import pytz
import datetime

def utc_to_local(utc_time_str, utc_format='%Y-%m-%dT%H:%M:%S'):
    local_tz = pytz.timezone('Asia/Shanghai')  # 定义本地时区
    utc_dt = datetime.datetime.strptime(utc_time_str, utc_format)  # 讲世界时间的格式转化为datetime.datetime格式
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(
        local_tz)  # 想将datetime格式添加上世界时区，然后astimezone切换时区：世界时区==>本地时区
    formatTime = int(time.mktime(local_dt.timetuple()))
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(formatTime))