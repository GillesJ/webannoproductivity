# WebAnno Productivity Checker

Check working hours of annotators in WebAnno.

## Usage and Settings:
Run example: 
`python3 log2workinghours -u user1, user2 -p 5 -s 2020-01-01 -e 2020-01-06 -d webanno3`
```
command arguments:
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
