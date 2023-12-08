import queue
import threading
import requests
from time import sleep

class Dispacther():
    def __init__(self):
        self.th = threading.Thread
        self.queue = queue.Queue()
    
    def schedule_job(self, job):
        print("schedule a job {}".format(job))

    def do_work(self):
        while self.keep_alive:
            print("keep alive and get a new job")
            job = self.queue.get()
            if job:
                print(job)
                print("do some work for a change")
            else:
                sleep(10)
    