__author__ = 'henrikmm'
import json
import time
import datetime
income = raw_input("Brukernavn: ")

testrec = {"request": "login", "content": income}
obj = json.dumps(testrec)
jrec = json.loads(obj)
body = jrec["content"]

tid = time.time()
thisTime = datetime.datetime.fromtimestamp(tid).strftime('%H:%M:%S')

print thisTime





