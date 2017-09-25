#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""dirblower.py: A simple multi-threaded file and directory bruteforcer in Python"""

__author__ = "@martijn0x76"
__email__ = "martijn@compiledknowledge.nl"
__license__ = "GPL"
__version__ = "1.0"

import argparse
from Queue import Queue
from pathlib import Path
from colorama import init, Fore, Back, Style
from threading import Thread, Lock
import urllib3
import time

list = 'newlist.txt'
ua = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'}

# Init. Colorama
init(autoreset=True)

lock = Lock()

# Handle the arguments
parser = argparse.ArgumentParser(description='A simple multi-threaded file and directory bruteforcer in Python')
parser.add_argument('-u','--url', help='The URL to test', required=True)
parser.add_argument('-p','--proxy', help='The proxy to use', required=False)
parser.add_argument('-t','--threads', help='The number of threads to spin', default=10, required=False)
parser.add_argument('-o','--out', help='Log output to a file', required=False)

args = parser.parse_args()

print('DirBlower v1.0 by @martijn0x76\n\n')
print('URL: %s' % args.url)

def test(i, q):
    while True:
        item = q.get()
        if not item[:1] == '/':
            item = '/' + item
        if args.proxy is not None:
            http = urllib3.ProxyManager(args.proxy, headers=ua)
        else:
            http = urllib3.PoolManager(1,headers=ua)
        url = args.url + item
        try:
            r = http.request('HEAD', url, retries=False)
            if r.status == 200:
                lock.acquire()
                print(Style.DIM + Fore.GREEN + 'Found: %s' % url)
                lock.release()
        except:
            pass
        finally:
            time.sleep(0.05)
            q.task_done()

# Init. queue
q = Queue()

list_file = Path(list)

if not list_file.is_file():
    print('The list with the name %s is not found' % list)

with open(list, 'r') as l:
    for line in l:
        q.put(line.rstrip('\r\n'))

print('Items to test: %d' % q.qsize())
print('Workers: %s\n\n' % args.threads)

start = time.time()

for i in range(int(args.threads)):
    worker = Thread(target=test, args=(i, q,))
    worker.setDaemon(True)
    worker.start()

print(Fore.MAGENTA + 'You can anytime exit this script by pressing CTRL + \\\n')
q.join()

end = time.time()
elapsed = end - start

print('\nElapsed time: %s s' % elapsed)
print('That\'s all Folks!')
