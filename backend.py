from datetime import datetime
from datetime import timedelta
from tkutil import DateFormat
from tkutil import JobType
import tkutil
import fileinput
import sys

# files for storage
job_category_file = 'job_categories.txt'
completed_jobs_file = 'completed_jobs.txt'
current_job_file = 'current_job.txt'
last_id_file = 'last_id.txt'

def rollback(filename, lines):
    """In case of a failure, writes all lines back to the file. 
    Argument lines must be list that contains the lines deleted from the file and lines must not contain new line character
    """
    with open(filename, 'a') as outf:
        for line in lines:
            outf.write(line + "\n")

def add_job_category(jobtype, jobname):
    """Adds a new job category to job_category_file and return the id of the inserted job.
    If the job with exact match exists, then it raises an exception.
    New job will be given a job id which is (max_id_of_previous_jobs + 1)
    """
    jobid = -1
    try:
        with open(job_category_file,'r') as inf:
            for line in inf:
                data = tkutil.parse_line(line)
                if data[1] == jobname:
                    msg = 'The job "%s" is already exists with id: %s' % (jobname, data[0])
                    raise ValueError(msg) # find a better exception
                    
                jobid = max(jobid, int(data[0]))
    except IOError:
        pass # so first time it is running not important
    
    jobid += 1 # next job id to use
    with open(job_category_file,'a') as outf:   
        outf.write(str(jobid) + "=>" + jobname + "=>" + str(jobtype) + "\n")
    
    return jobid

def get_categories():
    """Returns the all job category details.
    Returning element is a dictionary whose keys are job ids and values are tuples with format (jobname, jobtype)
    """
    job_categories = {}
    with open(job_category_file) as inf:
        for line in inf:
            data = tkutil.parse_line(line)
            job_categories[data[0]] = ((data[1], JobType.WORK if data[2] == '1' else JobType.NON_WORK))
    return job_categories

def get_job_details(jobid):
    """Returns the details of the job with given jobid. Returning element is a tuple with format (jobname, jobtype)"""
    job_categories = get_categories()
    return job_categories[jobid]
    
def delete_from_job_category(jobid):
    """Deletes the job category and the time records with this job category for given jobid
    and returns the job name for given id
    """
    try:
        details = get_job_details(jobid)
        delete_elements(job_category_file,jobid, 0) # returning element is not important for here
        delete_elements(completed_jobs_file, jobid, 1) # returning element is not important for here
        return details[0] # job names
    except KeyError:
        msg = "There is no job corresponding to this jobid %s" % jobid
        raise ValueError(msg) # find a better exception

def delete_elements(filename, elem_id, elem_id_index):
    """Helper function for deleting elements from files.
    Arguments are elem_id to delete and elem_id_index which indicates the index of the id element in the file after splitting.
    It returns the lines deleted from the file.
    """
    elements_deleted = []
    for line in fileinput.input(filename, inplace=1):
        line = line.rstrip('\n')
        data =line.split('=>')
        
        if data[elem_id_index] == elem_id:
            sys.stdout.write("")
            elements_deleted.append(line)
        else:
            print(line)
    
    return elements_deleted

def delete_from_records(record_id):
    """Deletes the time records for given record id. 
    If somehow it deletes more than one entry it will rollback and raise an exception
    """
    elements_deleted = delete_elements(completed_jobs_file, record_id, 0)
    if len(elements_deleted) <= 0: # no element is deleted which means there is no corresponding record for given id
        msg = "There is no time record corresponding to this record_id %s" % record_id
        raise ValueError(msg) # find a better exception
    if len(elements_deleted) > 1: # something wrong, there should only be 1 record for given id, rollback
        rollback(completed_jobs_file, elements_deleted)
        msg = "Something wrong with the following id %s, please check the records" % record_id
        raise ValueError(msg)
    
    time_details = tkutil.parse_time_details(elements_deleted[0])
    job_details = get_job_details(time_details["jobid"])
    time_details["jobname"] = job_details[0]
    
    return time_details

def contains_any(line, search_words):
    """Searchs for words in the line.
    If any of words in the search_words list can be found in the line it returns True, otherwise False
    """
    for word in search_words:
        if line.find(word) >= 0:
            return True
    return False
    
def search_jobs_for_ids(search_words):
    """Searchs for jobs whose name matches any of the given search words.
    It searches eagerly, not for exact match.
    It returns a list that contains tuples with format (jobid, jobname )
    """
    joblist = []
    with open(job_category_file,'r') as inf:
        for line in inf:
            data = tkutil.parse_line(line)
            
            if contains_any(data[1],search_words):
                joblist.append((data[0], data[1]))
            
    return joblist

def list_all_jobs_ids():
    """Returns all the job ids and names in the job_category_file.
    It returns a list that contains tuples with format (jobid, jobname )
    """
    return search_jobs_for_ids(['']) # may not be efficient but less code is better for now.
    
def insert_job_to_currents(jobid, start_time):
    """Inserts the job to current jobs with given jobid and start_time
    It clears the previous data on the current job file so that only one job can be started.
    """
    with open(current_job_file,'w') as outf:
        try:
            details = get_job_details(jobid)
            outf.write(jobid + "=>" + start_time.strftime(DateFormat.COMPACT) + "\n")
            return details[0] # job name
        except KeyError:
            msg = "There is no job corresponding to this jobid %s" % jobid
            raise ValueError(msg) # find a better exception
        
        
def insert_completed_job(jobid, start_time, end_time):
    """Inserts a completed job to completed_jobs_file for given jobid, start_time, end_time
    It will raise an exception:
    -if new entry overlaps any of the time records saved previously.
    -if there is no element in the job_category_file for corresponding jobid
    
    This function stores the id of the last inserted time record so that next time it can use it (autoincrement id)
    It will return the job name for inserted jobid
    """
    
    try:
        details = get_job_details(jobid)
    except KeyError:
        msg = "There is no job corresponding to this jobid %s" % jobid
        raise ValueError(msg) # find a better exception

    check_for_overlaps(start_time, end_time) # this will raise an exception if new entry overlaps with any record
    
    record_id = -1
    try:
        with open(last_id_file,'r') as inf:
            data = inf.read()
            record_id = int(data)
    except IOError:
        pass # so first time pass
    
    record_id += 1
    record_id = str(record_id)
    # TODO change the file name with something constituted from month and year so that file size can stay small
    with open(completed_jobs_file,'a') as outf:
        outf.write(record_id + "=>" + jobid + "=>" + start_time.strftime(DateFormat.COMPACT) + "#" + end_time.strftime(DateFormat.COMPACT) + "\n")
    
    with open(last_id_file, 'w') as outf:
        outf.write(record_id)
    return details[0] # job name

def is_overlapping(record_to_check, start_time, end_time):
    """This function checks whether given record and time intervals are overlapping"""
    if  start_time > record_to_check['end_time'] or end_time < record_to_check['start_time']:
        return False
    else:
        return True

def check_for_overlaps(start_time, end_time):
    """This function checks if any of the previously saved time records overlaps with given time interval.
    In case of overlap, this method will raise an exception
    """
    try:
        with open(completed_jobs_file) as inf:
            for line in inf:
                record_to_check = tkutil.parse_time_details(line)
                if is_overlapping(record_to_check, start_time, end_time):
                    job_details = get_job_details(record_to_check["jobid"])
                    record_to_check["jobname"] = job_details[0]
                    msg = ("The time records is overlapping with the following record, please check:\n%s\n%s"
                                                            % (tkutil.get_print_header(), tkutil.get_pretty_print_record(record_to_check)))
                    raise ValueError(msg)
    except IOError:
        pass # first time so no records at all


def pop_from_currents():
    """Returns the job id and start time of the job started before and clears the file (or related storage element)"""
    details = {}
    with open(current_job_file,'r') as inf:
        try:
            line = inf.read()
            data = tkutil.parse_line(line)
            jobid = data[0]
            start_time = datetime.strptime(data[1],DateFormat.COMPACT) # to ensure that data in the file is still as we have saved.
            details["jobid"] = jobid
            details["start_time"] = start_time
        except IndexError:
            pass # so no job started before return an empty dictinary
            
    open(current_job_file,'w').close() # clear file
    return details
    
def get_all_records_with_type(job_types, start_time, end_time):
    """This function returns the time records for corresponding job types.
    Arguments job_types is a list of JobType elements
    Returning elements is a list of dictionary elements whose keys are: record_id, jobid, jobname, start_time, end_time
    """
    all_records = []
    
    with open(completed_jobs_file) as inf:
        for line in inf:
            time_details = tkutil.parse_time_details(line)
            if is_within_interval(time_details, start_time, end_time):
                job_details = get_job_details(time_details["jobid"])
                time_details["jobname"] = job_details[0]
                if job_details[1] in job_types:
                    all_records.append(time_details)
    
    return all_records

def is_within_interval(record_to_check, start_time, end_time):
    return start_time <= record_to_check["start_time"] and  record_to_check["end_time"] < end_time

def get_time_summaries(start_time, end_time):
    """Returns the summary of the time records. These are the total times spent for job types.
    Returning element is a dictionary with following keys: JobType.WORK, JobType.NON_WORK
    """
    total_time_spent = {}
    total_time_spent[JobType.WORK] = timedelta()
    total_time_spent[JobType.NON_WORK] = timedelta()
    
    with open(completed_jobs_file) as inf:
        for line in inf:
            time_details = tkutil.parse_time_details(line)
            if is_within_interval(time_details, start_time, end_time):
                job_details = get_job_details(time_details["jobid"])
                time_spent = time_details["end_time"] - time_details["start_time"]
                total_time_spent[job_details[1]] += time_spent
    
    return total_time_spent
