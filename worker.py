import psycopg2
import time
from math import ceil, sqrt
from datetime import datetime

from models import *
from sqlalchemy.orm import scoped_session
from database import Session, engine

database = Session()

def find_prime_factors(n):
    n = int(n)
    ans = []
    pos = False
    for i in range(2, ceil(sqrt(n))):
        if n % i == 0:
            for j in range(2, ceil(sqrt(i)) + 1):
                if i % j == 0:
                    pos = False
                    break
                if j == ceil(sqrt(i)):
                    pos = True
            for j in range(2, ceil(sqrt(n / i)) + 1):
                if (n / i) % j == 0:
                    pos = False
                    break
                if j == ceil(sqrt(i)):
                    pos = True
            if pos:
                ans.append(i)
                ans.append(n / i)
            break
    if pos:
        if n == 1:
            return None
        elif len(ans) == 0:
            result = [int(sqrt(n)), int(sqrt(n))]
            return result
        else:
            result = [int(ans[0]), int(ans[1])]
            return result
    else:
        return None

def worker(n):
    start_num = int(n)
    new_num = start_num
    multi = 1
    added = 2
    length = len(str(start_num))
    while True:
        result = find_prime_factors(new_num)
        if result is not None and str(new_num)[:length] == str(start_num)[:length]:
            return result
        else:
            if added < multi - 1:
                new_num += 1
                added += 1
            else:
                multi *= 10
                new_num = multi * start_num
                added = 0
            if new_num > 10 ** 10:
                return None

while True:
    print('############ next cycle')
    answer = database.query(Worker).filter_by(status='queued')
    for att in answer:
        att.status = 'Progressing'
        database.add(att)
        database.commit()
        time_started = time.time()
        res = worker(att.n)
        p, q = res[0], res[1]
        time_end = time.time()
        elapsed = round(time_end - time_started, 8)
        att.time_end, att.status, att.p, att.q, = elapsed, 'Done', p, q
        print(time_end)
        database.add(att)
        database.commit()
        time_t = time.time()
        time_end = time.time()
    time.sleep(5)