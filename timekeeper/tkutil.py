# -- coding: utf-8 --
from datetime import datetime
from datetime import timedelta

class JobType:
    """Enum like class for job types: Work, Non-Work"""
    WORK = 1
    NON_WORK = 2

class DateFormat:
    """Date formats for writing and reading. Pretty is only for reports. For rest compact"""
    COMPACT = "%d/%m/%Y-%H:%M"
    PRETTY = "%a, %d %b %Y %H:%M"
    MONTH = "%m/%Y"
    YEAR = "%Y"
    
    
def get_job_type(string):
    """Returns JobType corresponding to string: work or non-work. For any other string it will raise an exception"""
    if string == "work":
        return JobType.WORK
    elif string == "non-work":
        return JobType.NON_WORK
    else:
        msg = "%s is not a valid job type" % string
        raise ValueError(msg) # find a better exception

def parse_line(line, delim='=>'):
    """Removes the new line character and splits the line according to delimiter"""
    line = line.rstrip('\n')
    return line.split(delim)
    
def parse_timedelta(td):
    """Returns a human-readable string for time differences"""
    days = td.days
    hours = int(td.seconds / 3600)
    minutes = int((td.seconds - (hours * 3600)) / 60)
    msg = "%d days, %d hours, %d minutes" % (days,hours,minutes)
    return msg
        
def parse_time_details(line):
    """Parses the line of completed job file and returns a dictionary with following keys: record_id, jobid, start_time, end_time"""
    data = parse_line(line)
    times = data[2].split('#')
    start_time = datetime.strptime(times[0],DateFormat.COMPACT)
    end_time = datetime.strptime(times[1],DateFormat.COMPACT)
    details = {}
    details["record_id"] = data[0]
    details["jobid"] = data[1]
    details["start_time"] = start_time
    details["end_time"] = end_time
    return details

def print_job_ids(joblist):
    """Prints job ids and job names"""
    print("Job ID\tJob Name");
    for jobid, jobname in joblist:
        print(str(jobid) + "\t" + jobname)

def get_print_header():
    """Returns a pretty string for header to be used reports with all time entries"""
    return "\t".join([ "id".ljust(5),
            "job name".ljust(25),
            "start time".ljust(25),
            "end time".ljust(25),
            "time spent" ])


def get_pretty_print_record(details):
    """Returns a pretty string for given time records. Note that argument must a dictionary with following keys:
       record_id, jobname, start_time, end_time
    """
    time_spent = details["end_time"] - details["start_time"]
    return "\t".join([ details["record_id"].ljust(5),
            details["jobname"].ljust(25),
            details["start_time"].strftime(DateFormat.PRETTY).ljust(25),
            details["end_time"].strftime(DateFormat.PRETTY).ljust(25),
            parse_timedelta(time_spent)])