import ics.alarm
import moon
import datetime
import decimal
from ics import Calendar, Event

dec = decimal.Decimal

base = datetime.datetime(2022, 1, 1)
dates_this_year = [base + i * datetime.timedelta(hours=1) for i in range(8760)]

ekadashi_dates_list: list[datetime] = []
in_range_list = []
new_moon_counter = 0
for date in dates_this_year:
    pos = moon.position(date)

    #found that the rising ekadasi is around a moon phase of 0.35 and waning ekadasi is around 0.85
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