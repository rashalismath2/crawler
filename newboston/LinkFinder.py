from html.parser import HTMLParser
from urllib import parse

class LinkFiner(HTMLParser):

    def __init__(self,base_url,page_url):
        super().__init__()
        self.base_url=base_url
        self.page_url=page_url
        self.links_set=set()

    def handle_starttag(self, tag, attrs):
        if tag=='a':
            for (attribute,value) in attrs:
                if attribute=="href":
                    # this will join if only the url is relative url
                    # else it will return th full url as normally would do
                    url=parse.urljoin(self.base_url,value)
                    self.links_set.add(url)
    
    def get_page_links(self):
        return self.links_set
        
    def error(self,message):
        pass

