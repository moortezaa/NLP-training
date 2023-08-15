import datetime
from time import sleep

start = datetime.datetime.now()
for i in range(300):
    sleep(.01)
    progress = (i+1)/300*100
    intprog = int(progress)
    now =   datetime.datetime.now()
    elapsed = now - start
    print('[\033[01m\033[32m'+'■'*intprog+'\033[0m\033[37m'+'-'*(100 - intprog)+'\033[0m]','%.2f%%'%progress,'elapsed: ',elapsed,'remaining:',datetime.timedelta(seconds=int(elapsed.total_seconds()/progress*(100-progress))),end='\r')
print()