import re
from itertools import groupby
import datetime
import subprocess

annotators = ["haiyanhuang", "elinevandewalle", "jefdhondt", "gilles"]
start_day = datetime.datetime(2020, 4, 29)
start_day = None
pause = 5 # 5 minutes

# get logs
log_text = subprocess.check_output(["docker", "logs", "webanno364"]).decode("utf8")

# parse entries
entry_re = re.compile("(?P<dt>\d{4}-\d\d-\d\d\s\d\d:\d\d:\d\d)\s(?P<type>\w+)\s\[(?P<user>\w+)\]\s(?P<dispatcher>\w+)\s-\s(?P<message>.*)", re.MULTILINE)
entries = [match.groupdict() for match in entry_re.finditer(log_text)
           if match.groupdict()["user"] in annotators]

# group entries by annotator
keyfunc = lambda d: d["user"]
for user, user_entries in groupby(sorted(entries, key=keyfunc), key=keyfunc):
    # collect hours worked
    user_dts = []
    print(user)
    for x in user_entries:
        dt = datetime.datetime.strptime(x["dt"], "%Y-%m-%d %H:%M:%S")
        if dt not in user_dts:
            user_dts.append(dt)
    user_dts = sorted(user_dts)
    time_blocks = []
    start = user_dts[0]
    for i, dt in enumerate(user_dts):
        try:
            next = user_dts[i+1]
            diff = next - dt
            if diff > datetime.timedelta(minutes=pause):
                time_blocks.append((start, dt, dt - start))
                start = next
        except IndexError as e:
            time_blocks.append((start, dt, dt - start))

    keyfunc = lambda x: x[0].strftime("%Y-%m-%d")
    for date_str, blocks_in_day in groupby(sorted(time_blocks, key=keyfunc), key=keyfunc):
        blocks_in_day = list(blocks_in_day)
        total_in_day = sum(block[2].total_seconds() for block in blocks_in_day)
        work_start = blocks_in_day[0][0].strftime("%H:%M:%S")
        work_end = blocks_in_day[-1][1].strftime("%H:%M:%S")
        print(f"Worked {datetime.timedelta(seconds=total_in_day)} on {date_str} ({work_start}-{work_end}).")

    if start_day:
        total_worked = sum(block[2].total_seconds() for block in time_blocks if block[0] > start_day)
        print(f"Total time worked since {start_day.strftime('%Y-%m-%d')}: {datetime.timedelta(seconds=total_worked)}")
    else:
        total_worked = sum(block[2].total_seconds() for block in time_blocks)
        print(f"Total time worked: {datetime.timedelta(seconds=total_worked)}")