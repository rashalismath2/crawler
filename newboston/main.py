import threading
from queue import Queue
from Spider import Spider
from domain import *
from functions import *

PROJECT_NAME="inexisconsulting"
HOMEPAGE="http://inexisconsulting.com/"
DOMAIN_NAME=get_domain_name(HOMEPAGE)
QUEUE_FILE=PROJECT_NAME+"/queue.txt"
CRAWLED_FILE=PROJECT_NAME+"/crawled.txt"
NUMBER_OF_THREADS=2
queue=Queue()
Spider(PROJECT_NAME,HOMEPAGE,DOMAIN_NAME,QUEUE_FILE,CRAWLED_FILE)


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t=threading.Thread(target=work)
        # making sure thread runs as a demon 
        # means this will stop when main thread stops
        t.daemon=True
        t.start()

def work():
    while True:
        url=queue.get()
        Spider.crawl_page(threading.current_thread().name,url)
        queue.task_done()

# each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()

def crawl():
    queued_links=file_to_set(QUEUE_FILE)
    if len(queued_links)>0:
        print(str(len(queued_links))+" links are queued")
        create_jobs()

create_workers()
crawl()