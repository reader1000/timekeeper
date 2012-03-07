#!/usr/bin/python
# -- coding: utf-8 --

import sys
import argparse
from datetime import datetime
from datetime import timedelta
import fileinput
import backend
from tkutil import DateFormat
from tkutil import JobType
import tkutil

def get_job_name(string_list):
    """Helper function to join string elements in the list to constitute job name
    It will raise an exception if the given list is empty
    """
    if len(string_list) <= 0:
        msg = "A job name is needed"
        raise argparse.ArgumentTypeError(msg)
  
    return ' '.join(string_list)


# TODO shoud we also consider job type for duplication check?
# i.e x is the job name then should (x, work) and (x,non-work) be considered same?
def add_job_category(jobcategory):
    """Parses addjob arguments and fires the add job category action"""
    try:
        jobtype = tkutil.get_job_type(jobcategory[0])
        jobname = get_job_name(jobcategory[1:])
        jobid = backend.add_job_category(jobtype, jobname)
        print(jobname + " added as " + ("work" if jobtype == JobType.WORK else "non-work") + " with id " + str(jobid))
    except (ValueError,argparse.ArgumentTypeError ) as msg:
        print(msg)
        return

class AddJobAction(argparse.Action):
    """Custom action for parsing and firing add job action"""
    def __call__(self, parser, namespace, values, option_string=None):
        add_job_category(values)
        setattr(namespace, self.dest, values)

# TODO generate an error message for non-existing job id
def delete_job_category(jobid):
    """Parses deletejob arguments and fires the delete job category action"""
    try:
        jobname = backend.delete_from_job_category(jobid)
        print("Following job category has been deleted: " + jobid + " => " + jobname)
    except ValueError as msg:
        print(msg)
        return
    except IOError:
        print("An error occured, please try again")

class DeleteJobCategoryAction(argparse.Action):
    """Custom action for parsing and firing delete job action"""
    def __call__(self, parser, namespace, values, option_string=None):
        delete_job_category(values[0])
        setattr(namespace, self.dest, values)

# TODO generate an error message for non-existing record id
def delete_record(record_id):
    """Parses deleterecord arguments and fires the delete time record action"""
    try:
        record = backend.delete_from_records(record_id)
        print("Following record has been deleted:")
        print(tkutil.get_pretty_print_record(record))
    except ValueError as msg:
        print(msg)
        return
    except IOError:
        print("An error occured, please try again")

class DeleteRecordAction(argparse.Action):
    """Custom action for parsing and firing delete time record action"""
    def __call__(self, parser, namespace, values, option_string=None):
        delete_record(values[0])
        setattr(namespace, self.dest, values)

def search_job_ids(search_words):
    """Parses search arguments and fires the search job category action"""
    joblist = backend.search_jobs_for_ids(search_words)
    tkutil.print_job_ids(joblist)
    
class SearchAction(argparse.Action):
    """Custom action for parsing and firing seach job categories action"""
    def __call__(self, parser, namespace, values, option_string=None):
        search_job_ids(values)
        setattr(namespace, self.dest, values)

def list_job_ids():
    """Parses list argument and fires the list categories action"""
    joblist = backend.list_all_jobs_ids()
    tkutil.print_job_ids(joblist)

class ListAction(argparse.Action):
    """Custom action for parsing and firing list job categories action"""
    def __call__(self, parser, namespace, values, option_string=None):
        list_job_ids()
        setattr(namespace, self.dest, values)

# TODO should we allow multiple jobs concurrently started
def start_job(jobid):
    """Parses start arguments and fires the start job action"""
    start_time = datetime.now()
    try:
        jobname = backend.insert_job_to_currents(str(jobid), start_time)
        print("Timer started for " + jobname)
    except IOError:
        print("No job category found. Please check and add some")
        return

class StartAction(argparse.Action):
    """Custom action for parsing and firing start time record action"""
    def __call__(self, parser, namespace, values, option_string=None):
        start_job(values)
        setattr(namespace, self.dest, values)
    
# TODO should we allow multiple jobs concurrently started
def end_job():
    """Parses end argument and fires end job action"""
    end_time = datetime.now()
    try:
        details = backend.pop_from_currents()
        jobname = backend.insert_completed_job(details["jobid"], details["start_time"], end_time)
    except KeyError:
        print("Error: There is no job started before")
        return
    print('The job "' + jobname + '" has ended and saved')
    
class EndAction(argparse.Action):
    """Custom action for parsing and firing end time record action"""
    def __call__(self, parser, namespace, values, option_string=None):
        end_job()
        setattr(namespace, self.dest, values)

def add_job(values):
    """Parses add arguments and fires add time record action"""
    jobid = values[0]
    try:
        start_time = datetime.strptime(values[1],DateFormat.COMPACT)
        end_time = datetime.strptime(values[2],DateFormat.COMPACT)
    except ValueError:
        msg = "Format for times %s %s are not a valid, use this format: dd/mm/yyyy-hh:mm" % (values[1], values[2])
        print(argparse.ArgumentTypeError(msg))
        return
    
    if start_time > end_time:
        msg = "Start time cannot be later than  end time (unless you've a time machine): %s %s" % (values[1], values[2])
        print(argparse.ArgumentTypeError(msg))
        return
    
    try:
        jobname = backend.insert_completed_job(jobid, start_time, end_time)
        print('Time record for the job "' + jobname + '" has been saved')
    except ValueError as msg:
        print(msg)
        return
    except IOError:
        print("No job category found. Please check and add some")
        return
    
class AddRecordAction(argparse.Action):
    """Custom action for parsing and firing add time record action"""
    def __call__(self, parser, namespace, values, option_string=None):
        add_job(values)
        setattr(namespace, self.dest, values)
    
def report_summary(start_time, end_time):
    """Prints the summary report"""
    total_time_spent = backend.get_time_summaries(start_time, end_time)
    print("Time spent for work related things:\t %s" % tkutil.parse_timedelta(total_time_spent[JobType.WORK]))
    print("Time spent for non-work related things:\t %s" % tkutil.parse_timedelta(total_time_spent[JobType.NON_WORK]))
    print("Total time spent:\t\t\t %s" % tkutil.parse_timedelta(total_time_spent[JobType.WORK] + total_time_spent[JobType.NON_WORK]))

def report_all(job_types, start_time, end_time):
    """Prints the detailed report for given job types"""
    all_records = backend.get_all_records_with_type(job_types,start_time, end_time)
    
    print(tkutil.get_print_header())
    all_records = sorted(all_records, key = lambda x : x["start_time"])
    for details in all_records:
        print(tkutil.get_pretty_print_record(details))

def report_time(report_type='summary', start_time=datetime(1, 1, 1), end_time=datetime(9999, 12, 31)):
    """Parses report arguments and fires the report action"""
    job_types = {}
    job_types['all'] = set([JobType.WORK, JobType.NON_WORK])
    job_types['allwork'] = set([JobType.WORK])
    job_types['allnonwork'] = set([JobType.NON_WORK])
    
    try:
        if report_type == 'summary':
            report_summary(start_time, end_time)
        else:
            try:
                report_all(job_types[report_type], start_time, end_time)
            except KeyError:
                print('There is no corresponding report type for "%s", please chech' % report_type)
    except IOError:
        print("No data to report. Please add some job categories and time records first")
        return

class ReportAction(argparse.Action):
    """Custom action for parsing and firing report time records action"""
    def __call__(self, parser, namespace, values, option_string=None):
        report_time(values[0])
        setattr(namespace, self.dest, values)
        
class ReportMonthAction(argparse.Action):
    """Custom action for parsing and firing report time records action"""
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            time_interval = get_interval(values[1], 32, DateFormat.MONTH)
            report_time(values[0], time_interval["start_time"], time_interval["end_time"])
            setattr(namespace, self.dest, values)
        except ValueError as msg:
            print(msg)
            return

def get_interval(start_date, days_to_add, date_format):
    try:
        time_interval = {}
        time_start = datetime.strptime(start_date,date_format)
        time_interval["start_time"] = time_start
        # as long as we are not dealing with exceptional dates in the history (and I hope in the future) this should work
        time_end = time_start + timedelta(days=days_to_add) 
        time_interval["end_time"] = datetime.strptime(time_end.strftime(date_format), date_format)
    
        return time_interval
    except ValueError:
        raise ValueError("Check the format, please: %s" % start_date)
    
class ReportYearAction(argparse.Action):
    """Custom action for parsing and firing report time records action"""
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            time_interval = get_interval(values[1], 367, DateFormat.YEAR)
            report_time(values[0], time_interval["start_time"], time_interval["end_time"])
            setattr(namespace, self.dest, values)
        except ValueError as msg:
            print(msg)
            return

def main(argv):
    """Main method which parses and fires the related action.
    Note that argument parsing mechanism is used like something similar to onclick like actions.
    All the optional arguments are actions to be performed so parsing and firing are performed together.
    """
    
    parser = argparse.ArgumentParser(description='Time keeper for the things you do.')
    
    # all the arguments are mutually exclusive
    group = parser.add_mutually_exclusive_group(required=True)
    
    # parse and perform the add job action
    group.add_argument('--addjob', nargs='+', type=str, 
                                    help='Adds a job category type and name for future use format: jobtype(work | non-work) jobname',
                                    action=AddJobAction)

    # parse and perform the delete job category action
    group.add_argument('--deletejob', nargs=1, metavar='jobid', type=str, 
                                    help='Deletes the job category. This will also delete time records related to this job',
                                    action=DeleteJobCategoryAction)

    # parse and perform the delete record action
    group.add_argument('--deleterecord', nargs=1, metavar='ID', type=str, 
                                    help='Deletes the time record for given time record ID',
                                    action=DeleteRecordAction)
    
    # parse and perform the search action
    group.add_argument('--search', nargs='+', metavar='keywords', type=str, 
                                    help='Returns the id of the job that contains any of the search keywords', action=SearchAction)

    # parse and perform the search action
    group.add_argument('--list', nargs=0, help='Returns the ids of the jobs', action=ListAction)
 
    # parse and perform the start action
    group.add_argument('--start', metavar='jobid', type=int, help='register a start time for the given job id', action=StartAction)
    
    # parse and perform the end action
    group.add_argument('--end', nargs=0, help='end and save time for the given job id', action=EndAction)

    # parse and perform the add action
    group.add_argument('--add', nargs=3, 
                                    help='Adds a record for given job id, start time and end time', action=AddRecordAction)
    
    group.add_argument('--report', nargs=1, metavar='report_type',type=str,
                                    help='Reports the times, types are summary, all, allwork, allnonwork', action=ReportAction)

    group.add_argument('--reportmonth', nargs=2, type=str,
                                    help='Reports the times of the month: report_type month(mm/yyyy)',
                                    action=ReportMonthAction)
                                    
    group.add_argument('--reportyear', nargs=2, type=str,
                                    help='Reports the times of the year: report_type year(yyyy)',
                                    action=ReportYearAction)
    
    
    # note that calling this function will also perform the actions specified with arguments.
    args = parser.parse_args()

if __name__ == '__main__':
    main(sys.argv)

def target(*args):
    return main, None