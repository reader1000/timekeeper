# -- coding: utf-8 --
from nose.tools import *
from timekeeper import tkutil
from timekeeper.tkutil import JobType
from datetime import timedelta

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
    _days = 3
    _hours = 7
    _minutes = 49
    dtxt = "%d days, %d hours, %d minutes" % (_days,_hours,_minutes)
    assert_equal(tkutil.parse_timedelta(timedelta(days=_days, hours=_hours, minutes=_minutes)), dtxt)
    
    _days = 200
    _hours = 23
    _minutes = 59
    dtxt = "%d days, %d hours, %d minutes" % (_days,_hours,_minutes)
    assert_equal(tkutil.parse_timedelta(timedelta(days=_days, hours=_hours, minutes=_minutes)), dtxt)
    