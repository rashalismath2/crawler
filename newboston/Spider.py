from cgitb import html
from urllib import response
from urllib.request import urlopen
from LinkFinder import LinkFiner
from functions import *

class Spider:

    project_name=""
    base_url=""
    domain_name=""
    queue_file=""
    crawled_file=""
    queue_set=set()
    crawled_set=set()

    def __init__(self,project_name,base_url,domain_name,queue_file,crawled_file):
        Spider.project_name=project_name
        Spider.base_url=base_url
        Spider.domain_name=domain_name
        Spider.queue_file=queue_file
        Spider.crawled_file=crawled_file
        self.boot()
        self.crawl_page("First spider",Spider.base_url)
    
    @staticmethod
    def boot():
        create_project_dir(Spider.project_name)
        create_data_files(Spider.base_url,Spider.queue_file,Spider.crawled_file)
        Spider.queue_set=file_to_set(Spider.queue_file)
        Spider.crawled_set=file_to_set(Spider.crawled_file)

    @staticmethod
    def crawl_page(page_name,page_url):
        if page_url not in Spider.crawled_set:
            print(page_name+" - "+page_url)
            print("Queued count "+str(len(Spider.queue_set)))
            print("Crawled count "+str(len(Spider.crawled_set)))
            crawled_links=Spider.gather_links(page_url)
            Spider.add_links_to_queue(crawled_links)
            Spider.queue_set.remove(page_url)
            Spider.crawled_set.add(page_url)
            Spider.update_files()

    @staticmethod
    def gather_links(page_url):
        html_in_string=""
        try:
            response=urlopen(page_url)
            if response.getheader("Content-Type")=="text/html":
                html_bytes=response.read()
                html_in_string=html_bytes.decode("utf-8")
            finder=LinkFiner(Spider.base_url,page_url)
            finder.feed(html_in_string)
        except Exception as e:
            print("Error reading web page "+page_url+" "+str(e))
            return set()
        return finder.get_page_links()

    @staticmethod
    def add_links_to_queue(links_set):
        for url in links_set:
            if url in Spider.queue_set:
                continue
            if url in Spider.crawled_set:
                continue
            if Spider.domain_name not in url:
                continue
            Spider.queue_set.add(url)

    @staticmethod
    def update_files():
        set_to_file(Spider.queue_set,Spider.queue_file)
        set_to_file(Spider.crawled_set,Spider.crawled_file)