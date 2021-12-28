#3rd waxing gibbous or 3rd waning crescent
import ics.alarm
import numpy as np
import moon
import datetime
import decimal
from ics import Calendar, Event
import pytz
#Get all dates that moon is in the third waxing gibbous or in the third waning crescent
#write those dates to an ics file

dec = decimal.Decimal

base = datetime.datetime(2022, 1, 1)
dates_this_year = [base + i * datetime.timedelta(hours=1) for i in range(8760)]

ekadashi_dates_list: list[datetime] = []
in_range_list = []
new_moon_counter = 0
for date in dates_this_year:
    pos = moon.position(date)

    rising_diff = abs(pos - dec(0.35))
    waning_diff = abs(pos - dec(0.85))

    significant_rising_date = float(rising_diff) < float(0.05)
    significant_waning_date = float(waning_diff) < float(0.05)

    significant_date = significant_waning_date or significant_rising_date

    if significant_rising_date:
        in_range_list.append([date, rising_diff, pos])
    elif significant_waning_date:
        in_range_list.append([date, waning_diff, pos])

    if in_range_list and not significant_date:
        sorted_list = sorted(in_range_list, key=lambda x: x[1])
        ekadashi_dates_list.append(sorted_list[0][0])
        in_range_list.clear()
    """
    if phase == "New Moon":
        new_moon_counter += 1
        if new_moon_counter == 3:
            ekadashi_dates_list.append(date + datetime.timedelta(hours=259.86))
            ekadashi_dates_list.append(date + datetime.timedelta(hours=614.22))
            new_moon_counter = 0
    """
    #print(date, pos, moon.phase(pos))

cal = Calendar()

for date in ekadashi_dates_list:
    event = Event()
    event.name = "Ekadashi Fasting"
    begin = date.replace(hour=0, minute=0) + datetime.timedelta(hours=8)
    end = begin + datetime.timedelta(days=1)
    begin = begin.strftime("%Y-%m-%d %H:%M:%S")
    end = end.strftime("%Y-%m-%d %H:%M:%S")
    event.begin = begin
    event.end = end
    event.alarms.append(ics.alarm)
    cal.events.add(event)

with open("cal.ics", "w") as cal_obj:
    cal_obj.writelines(cal)

#print(ekadashi_dates_list)
#for date in ekadashi_dates_list:
    #print(date)