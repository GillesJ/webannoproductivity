import re
from itertools import groupby
import datetime
import subprocess
import argparse

# parse args and set vars
parser = argparse.ArgumentParser(
    prog="log2workinghours",
    usage="Parses WebAnno log to working hours. Example: python3 log2workinghours -u user1, user2 -p 5 -s 2020-01-01 -e 2020-01-06 -d webanno3"
)
parser.add_argument(
    "-u",
    "--users",
    nargs="+",
    required=True,
    help="""One or multiple name(s) of the WebAnno users whose working hours\
             are retrieved."""
)
parser.add_argument(
    "-p",
    "--pause",
    nargs=1,
    default=[5],
    type=int,
    help="""Pause time in minutes: time between annotations after this durat\
            ion will be counted as a pause in annotation and will not count tow\
            ards total hours worked."""
)
parser.add_argument(
    "-s",
    "--start",
    nargs=1,
    type=str,
    default=None,
    help="Starting day date in format %%Y-%%m-%%d from which the total working hours are counted."
)
parser.add_argument(
    "-e",
    "--end",
    nargs=1,
    type=str,
    default=None,
    help="Ending day date in format %%Y-%%m-%%d until which the total working hours are counted."
)
parser.add_argument(
    "-d",
    "--docker",
    nargs=1,
    type=str,
    default=["webanno364"],
    help="Name of the WebAnno docker image for which the logs are retrieved."
)

args = parser.parse_args()

annotators = args.users
start_day = datetime.datetime.strptime(args.start[0], "%Y-%m-%d") if args.start else datetime.datetime.min
end_day = datetime.datetime.strptime(args.end[0], "%Y-%m-%d") if args.end else datetime.datetime.max
pause = args.pause[0]
docker_name = args.docker[0]

# get logs
log_text = subprocess.check_output(["docker", "logs", docker_name]).decode("utf8")

# parse entries
entry_re = re.compile("(?P<dt>\d{4}-\d\d-\d\d\s\d\d:\d\d:\d\d)\s(?P<type>\w+)\s\[(?P<user>\w+)\]\s(?P<dispatcher>\w+)\s-\s(?P<message>.*)", re.MULTILINE)
entries = [match.groupdict() for match in entry_re.finditer(log_text)
           if match.groupdict()["user"] in annotators]

# group entries by annotator
keyfunc = lambda d: d["user"]
user_seen = set()
for user, user_entries in groupby(sorted(entries, key=keyfunc), key=keyfunc):
    user_seen.add(user)
    # collect hours worked
    user_dts = []
    print(user.upper())
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

    total_worked = sum(block[2].total_seconds() for block in time_blocks if start_day < block[0] < end_day )
    print(f"Total time worked from {start_day.strftime('%Y-%m-%d')} to {end_day.strftime('%Y-%m-%d')}: {datetime.timedelta(seconds=total_worked)}")
    print("-------")

# warn about non-found users
for u in annotators:
    if u not in user_seen:
        print(f"WARNING: {u} was not found in the logs.")