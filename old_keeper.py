import sys
import argparse

class JobType:
  WORK=1
  NON_WORK=2

def get_job_type(string):
  if string == "work":
    return JobType.WORK
  elif string == "non-work":
    return JobType.NON_WORK
  else:
    msg = "%s is not a valid job type" % string
    raise argparse.ArgumentTypeError(msg)

def add_job_category(jobname, jobtype):
  print(jobname + " added as " + ("work" if jobtype == JobType.WORK else "non-work"))

parser = argparse.ArgumentParser(description='Time keeper for the thing you do.')
parser.add_argument('--add', dest='add_job_category', action='store_const', const=add_job_category)
parser.add_argument('--jobname', dest='jobname', nargs='+', 
    metavar='job_name', type=str, help='A job category name for future use')
parser.add_argument('--jobtype',dest='jobtype', type=get_job_type)

args = parser.parse_args()
print(args)
args.add_job_category(' '.join(args.jobname), args.jobtype)