# -- coding: utf-8 --

from nose.tools import *
from timekeeper import tkutil
from timekeeper.tkutil import JobType

def test_get_job_type():
    assert_equal(tkutil.get_job_type("work"), JobType.WORK)
    assert_equal(tkutil.get_job_type("non-work"), JobType.NON_WORK)
    
@raises(ValueError)
def test_get_job_type_fail():
    assert_equal(tkutil.get_job_type("my_work"), JobType.WORK)
    


