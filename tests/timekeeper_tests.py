# -- coding: utf-8 --
from nose.tools import *
from timekeeper import tkutil
from timekeeper.tkutil import JobType
from datetime import timedelta
from datetime import datetime

def test_get_job_type():
    assert_equal(tkutil.get_job_type("work"), JobType.WORK)
    assert_equal(tkutil.get_job_type("non-work"), JobType.NON_WORK)
    
@raises(ValueError)
def test_get_job_type_fail():
    assert_equal(tkutil.get_job_type("my_work"), JobType.WORK)
    

def test_parse_line():
    line = "=>".join(["foo", "bar\n"])
    assert_equal(tkutil.parse_line(line), ["foo", "bar"])
    
    line = "=>".join(["foo", "bar baz\n"])
    assert_equal(tkutil.parse_line(line), ["foo", "bar baz"])
    
    line = "##".join(["foo", "bar\n"])
    assert_equal(tkutil.parse_line(line,"##"), ["foo", "bar"])

def test_parse_timedelta():
    tmp_days = 3
    tmp_hours = 7
    tmp_minutes = 49
    dtxt = "%d days, %d hours, %d minutes" % (tmp_days, tmp_hours, tmp_minutes)
    assert_equal(tkutil.parse_timedelta(timedelta(days=tmp_days, hours=tmp_hours, minutes=tmp_minutes)), dtxt)
    
    tmp_days = 200
    tmp_hours = 23
    tmp_minutes = 59
    dtxt = "%d days, %d hours, %d minutes" % (tmp_days, tmp_hours, tmp_minutes)
    assert_equal(tkutil.parse_timedelta(timedelta(days=tmp_days, hours=tmp_hours, minutes=tmp_minutes)), dtxt)

def test_parse_time_details():
    # keys: record_id, jobid, start_time, end_time
    job_details = tkutil.parse_time_details("0=>0=>10/01/2012-13:30#10/01/2012-15:47")
    
    start_time = datetime(2012,1,10,13, 30)
    end_time = datetime(2012,1,10,15, 47)
    
    assert_equal(job_details["record_id"], "0")
    assert_equal(job_details["jobid"], "0")
    assert_equal(job_details["start_time"], start_time)
    assert_equal(job_details["end_time"], end_time)
    
    job_details = tkutil.parse_time_details("3=>1=>03/12/2011-10:30#03/12/2011-12:30")
    
    start_time = datetime(2011,12,3,10, 30)
    end_time = datetime(2011,12,3,12, 30)
    
    assert_equal(job_details["record_id"], "3")
    assert_equal(job_details["jobid"], "1")
    assert_equal(job_details["start_time"], start_time)
    assert_equal(job_details["end_time"], end_time)

    
    
    
    
    
    
    
    
    
    
    