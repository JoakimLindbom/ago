#!/usr/bin/python

import time

from datetime import date, datetime


if __name__ == "__main__":

    t1 = datetime.now()
    time.sleep(2)
    t2 = datetime.now()

    print t1
    print t2-t1

    t3 =  t2-t1
    print t3.days*86400+t3.seconds
    print int(t3.total_seconds())



