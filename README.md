# Timekeeper - Command line time management without need for a database

Timeekeeper is a Python 3 application to manage your time. It does not need for a
database, it works on plain text files with a command line interface.

## How to Use

First you need to define jobs and their types for future use.
($ for commands)

### For a work related job with name "timekeeper project":

    $ python timekp.py --addjob work timekeeper project

     timekeeper project added as work with id 0

### For a non-work related job with name "play tennis":

    $ python timekp.py --addjob non-work play tennis

     play tennis added as non-work with id 1

### Then list the previously saved jobs:

    $ python timekp.py --list

     Job ID  Job Name
     0       timekeeper project
     1       play tennis


### Or search for a job:

    $ python timekp.py --search project

     Job ID  Job Name
     0       timekeeper project


### Start timer for the "timekeeper project" job

    $ python timekp.py --start 0

     Timer started for timekeeper project


### Stop timer for the job previously started and save it

    $ python timekp.py --end

     The job "timekeeper project" has ended and saved

### Add a time record for know start and end time

    $ python timekp.py --add 0 10/01/2012-13:30 10/01/2012-15:47

     Time record for the job "timekeeper project" has been saved


### Report the summary of time records
    $ python timekp.py --report summary

     Time spent for work related things:      0 days, 2 hours, 17 minutes
     Time spent for non-work related things:  0 days, 2 hours, 0 minutes
     Total time spent:                        0 days, 4 hours, 17 minutes


### Report work related time record details
    $ python timekp.py --report allwork

     id     job name                   start time                  end time                     time spent
     1      timekeeper project         Tue, 10 Jan 2012 13:30      Tue, 10 Jan 2012 15:47       0 days, 2 hours, 17 minutes
     0      timekeeper project         Tue, 10 Jan 2012 18:19      Tue, 10 Jan 2012 18:19       0 days, 0 hours, 0 minutes



### Report non-work related time record details
    $ python timekp.py --report allnonwork

     id     job name                   start time                   end time                    time spent
     2      play tennis                Sun, 08 Jan 2012 10:30       Sun, 08 Jan 2012 12:30      0 days, 2 hours, 0 minutes


### Report everything
    $ python timekp.py --report all

     id     job name                   start time                   end time                    time spent
     2      play tennis                Sun, 08 Jan 2012 10:30       Sun, 08 Jan 2012 12:30      0 days, 2 hours, 0 minutes
     1      timekeeper project         Tue, 10 Jan 2012 13:30       Tue, 10 Jan 2012 15:47      0 days, 2 hours, 17 minutes
     0      timekeeper project         Tue, 10 Jan 2012 18:19       Tue, 10 Jan 2012 18:19      0 days, 0 hours, 0 minutes

### Delete a time record
    $ python timekp.py --deleterecord 0

     Following record has been deleted:
     0      timekeeper project         Tue, 10 Jan 2012 18:19       Tue, 10 Jan 2012 18:19      0 days, 0 hours, 0 minutes

### Delete a job category
    $ python timekp.py --deletejob 1

     Following job category has been deleted: 1 => play tennis

### Help
    $ python timekp.py --help

