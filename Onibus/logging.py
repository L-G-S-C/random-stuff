from datetime import date, datetime
import os
from time import time

def checkLogExist(file: str) -> None:

    now = datetime.now()
    timestamp = ''

    with open(f'{file}.txt', 'a+') as log:
        log.seek(0, 0)
        timestamp = log.readline().strip()

        if not timestamp == '':
            timestamp = datetime.strptime(timestamp, '# Log from %d %b, %Y')
        else:
            log.write(f'{now.strftime("# Log from %d %b, %Y")}\n\n')
            timestamp = now
    
    if not timestamp.date() == now.date():
        os.rename(f'{file}.txt', f'logs/[{timestamp.strftime("%d-%m-%Y")}] {file}.txt')
        checkLogExist(file)

def generateLog(msg: str, file: str = 'log-latest', timestamp: bool = True) -> None:

    if not os.path.exists('logs/'):
        print('Hi')
        os.mkdir('logs/')
    
    checkLogExist(file)

    with open(f'{file}.txt', 'a+') as log:
        now = datetime.now()
        timestamp_str = ''
        if timestamp == True:
            timestamp_str = f'[{now.strftime("%H:%M:%S")}] '

        log.write(f'{timestamp_str}{msg}\n')

if __name__ == "__main__":
    generateLog('Teste')