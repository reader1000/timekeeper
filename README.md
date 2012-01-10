# Timekeeper - Command line time management without need for a database

Timeekeeper is a Python application to manage your time. It does not need a
database, it works on plain text files with a command line interface.

Timekeeper should be working with both Python 2.7 and Python 3
Compatibility Python 3 is well tested. It seems to be compatible with Python 2.7 also.

## Basic Setup

* Download the timekeeper.tar.gz
* Extract it to folder with read/write permissions
* Run the following commands (do not run as root but use sudo)
* cd timekeeper
* sudo python setup.py install

Note: In the future a nicer way will be provided.

## How to Use

First you need to define jobs and their types for future use.
($ for commands)

### Add a work related job with name "timekeeper project":

    $ timekp --addjob work timekeeper project

     timekeeper project added as work with id 0

### Add a non-work related job with name "play tennis":

    $ timekp --addjob non-work play tennis

     play tennis added as non-work with id 1

### Then list the previously saved jobs:

    $ timekp --list

     Job ID  Job Name
     0       timekeeper project
     1       play tennis


### Or search for a job:

    $ timekp --search project

     Job ID  Job Name
     0       timekeeper project


### Start timer for the "timekeeper project" job

    $ timekp --start 0

     Timer started for timekeeper project


### Stop timer for the job previously started and save it

    $ timekp --end

     The job "timekeeper project" has ended and saved

### Add a time record for know start and end time

    $ timekp --add 0 10/01/2012-13:30 10/01/2012-15:47

     Time record for the job "timekeeper project" has been saved

### Report the summary of the time records for the month

    $ timekp --reportmonth summary 01/2012

     Time spent for work related things:      0 days, 3 hours, 19 minutes
     Time spent for non-work related things:  0 days, 2 hours, 0 minutes
     Total time spent:                        0 days, 5 hours, 19 minutes

### Report the summary of the time recods for the year
    $ timekp --reportyear summary 2012

     Time spent for work related things:      0 days, 3 hours, 19 minutes
     Time spent for non-work related things:  0 days, 2 hours, 0 minutes
     Total time spent:                        0 days, 5 hours, 19 minutes

### Report the summary of all time records
    $ timekp --report summary

     Time spent for work related things:      0 days, 4 hours, 41 minutes
     Time spent for non-work related things:  0 days, 7 hours, 0 minutes
     Total time spent:                        0 days, 11 hours, 41 minutes

### Report work related time records details for the month

    $ timekp --reportmonth allwork 01/2012

     id     job name                   start time                  end time                     time spent
     0      timekeeper project         Tue, 10 Jan 2012 13:30       Tue, 10 Jan 2012 15:47      0 days, 2 hours, 17 minutes
     1      timekeeper project         Tue, 10 Jan 2012 18:19       Tue, 10 Jan 2012 19:21      0 days, 1 hours, 2 minutes

### Report work related time records for the year

     $ timekp --reportyear allwork 2011

     id     job name                   start time                  end time                     time spent     
     6      timekeeper project         Thu, 24 Nov 2011 14:19       Thu, 24 Nov 2011 14:30      0 days, 0 hours, 11 minutes
     5      timekeeper project         Fri, 30 Dec 2011 18:19       Fri, 30 Dec 2011 19:30      0 days, 1 hours, 11 minutes


### Report all work related time record details
    $ timekp --report allwork

     id     job name                   start time                  end time                     time spent
     6      timekeeper project         Thu, 24 Nov 2011 14:19       Thu, 24 Nov 2011 14:30      0 days, 0 hours, 11 minutes
     5      timekeeper project         Fri, 30 Dec 2011 18:19       Fri, 30 Dec 2011 19:30      0 days, 1 hours, 11 minutes
     0      timekeeper project         Tue, 10 Jan 2012 13:30       Tue, 10 Jan 2012 15:47      0 days, 2 hours, 17 minutes
     1      timekeeper project         Tue, 10 Jan 2012 18:19       Tue, 10 Jan 2012 19:21      0 days, 1 hours, 2 minutes

### Report non-work related time records details for the month
     $ timekp --reportmonth allnonwork 01/2012
     id     job name                   start time                   end time                    time spent
     2      play tennis                Sun, 08 Jan 2012 10:30       Sun, 08 Jan 2012 12:30      0 days, 2 hours, 0 minutes

### Report non-work related time records for the year
     $ timekp --reportyear allnonwork 2011
     id     job name                   start time                   end time                    time spent
     4      play tennis                Thu, 03 Nov 2011 10:30       Thu, 03 Nov 2011 13:30      0 days, 3 hours, 0 minutes
     3      play tennis                Sat, 03 Dec 2011 10:30       Sat, 03 Dec 2011 12:30      0 days, 2 hours, 0 minutes

### Report non-work related time record details
    $ timekp --report allnonwork

     id     job name                   start time                   end time                    time spent
     4      play tennis                Thu, 03 Nov 2011 10:30       Thu, 03 Nov 2011 13:30      0 days, 3 hours, 0 minutes
     3      play tennis                Sat, 03 Dec 2011 10:30       Sat, 03 Dec 2011 12:30      0 days, 2 hours, 0 minutes
     2      play tennis                Sun, 08 Jan 2012 10:30       Sun, 08 Jan 2012 12:30      0 days, 2 hours, 0 minutes


### Report everything
    $ timekp --report all

     id     job name                   start time                   end time                    time spent
     4      play tennis                Thu, 03 Nov 2011 10:30       Thu, 03 Nov 2011 13:30      0 days, 3 hours, 0 minutes
     6      timekeeper project         Thu, 24 Nov 2011 14:19       Thu, 24 Nov 2011 14:30      0 days, 0 hours, 11 minutes
     3      play tennis                Sat, 03 Dec 2011 10:30       Sat, 03 Dec 2011 12:30      0 days, 2 hours, 0 minutes
     5      timekeeper project         Fri, 30 Dec 2011 18:19       Fri, 30 Dec 2011 19:30      0 days, 1 hours, 11 minutes
     2      play tennis                Sun, 08 Jan 2012 10:30       Sun, 08 Jan 2012 12:30      0 days, 2 hours, 0 minutes
     0      timekeeper project         Tue, 10 Jan 2012 13:30       Tue, 10 Jan 2012 15:47      0 days, 2 hours, 17 minutes
     1      timekeeper project         Tue, 10 Jan 2012 18:19       Tue, 10 Jan 2012 19:21      0 days, 1 hours, 2 minutes


### Delete a time record
    $ timekp --deleterecord 0

     Following record has been deleted:
     0      timekeeper project         Tue, 10 Jan 2012 18:19       Tue, 10 Jan 2012 18:19      0 days, 0 hours, 0 minutes

### Delete a job category
    $ timekp --deletejob 1

     Following job category has been deleted: 1 => play tennis

### Help
    $ timekp --help

