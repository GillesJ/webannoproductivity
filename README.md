# WebAnno Productivity Checker

Check working hours of annotators in WebAnno.

## Usage:
Run example: 

`python log2workinghours.py -u user1 user2 -s 2020-04-27 -e 2020-04-29 -d webanno364`

Output:

```
USER1
Worked 1:59:14 on 2020-04-27 (08:27:17-11:56:09).
Worked 1:31:39 on 2020-04-28 (07:02:00-08:47:51).
Total time worked from 2020-04-27 to 2020-04-29: 4:00:49
-------
USER2
Worked 1:52:33 on 2020-04-27 (08:52:08-11:54:49).
Worked 1:40:16 on 2020-04-28 (07:06:51-08:47:07).
Total time worked from 2020-04-27 to 2020-04-29: 4:29:26
-------
```

Command arguments:
```
  -h, --help            show this help message and exit
  -u USERS [USERS ...], --users USERS [USERS ...]
                        One or multiple name(s) of the WebAnno users whose
                        working hours are retrieved.
  -p PAUSE, --pause PAUSE
                        Pause time in minutes: time between annotations after
                        this durat ion will be counted as a pause in
                        annotation and will not count tow ards total hours
                        worked.
  -s START, --start START
                        Starting day date in format %Y-%m-%d from which the
                        total working hours are counted.
  -e END, --end END     Ending day date in format %Y-%m-%d until which the
                        total working hours are counted.
  -d DOCKER, --docker DOCKER
                        Name of the WebAnno docker image for which the logs
                        are retrieved.
```
Requirements:
- Python 3.6+ 
