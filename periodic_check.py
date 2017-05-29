import checks
from lifx import Lifx
import sys

'''

Usage:
$ python periodic_check.py [morning|afternoon|night]

'''
if __name__ == "__main__":

    lifx = Lifx()
    time = sys.argv[2]

    settings = {
        "time": time
    }

    print "Running all main functions in the modules in checks:"
    for key in checks.__dict__:
        if '__' not in key:
            task = checks.__dict__[key].Task(settings)
            task.main(lifx)

    
