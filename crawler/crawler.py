
import json
import requests
import re
import sys
from bs4 import BeautifulSoup
from markdown import markdown

import html2text
from urllib.parse import urlparse

class PyCrawler(object):
    def __init__(self, starting_url):
        self.starting_url = starting_url
        self.visited = set()

    def get_html(self, url):
        try:
            html = requests.get(url)
        except Exception as e:
            print(e)
            return ""
        return html.content.decode('utf-8')

    def get_links(self, url):
        html = self.get_html(url)
        parsed = urlparse(url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        links = re.findall('''<a\s+(?:[^>]*?\s+)?href="([^"]*)"''', html)
        for i, link in enumerate(links):
            if not urlparse(link).netloc:
                link_with_base = base + link
                links[i] = link_with_base

        return set(filter(lambda x: 'mailto' not in x, links))

    def extract_info(self, url):
        #dont know any better methord
        html = self.get_html(url)
        data=""
        try:
            soup = BeautifulSoup(html, "html.parser")
            tag = soup.body
            for string in tag.strings:
            	data+=str(string)
        except:pass
        return data.replace("\n","").replace("/n","")

    def crawl(self, url):
        for link in self.get_links(url):
            if "http://" in link or "https://" in link:
                if link in self.visited:
                    continue
                self.visited.add(link)
                info = self.extract_info(link)
                regex = re.compile(
                        r'^(?:http|ftp)s?://' # http:// or https://
                        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                        r'localhost|' #localhost...
                        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                        r'(?::\d+)?' # optional port
                        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
                if "?" not in link and len(re.findall("/^javascript/i",link))==0 and re.match(regex, link) is not None:
                    with open("data.json",'r') as file:
                        print(link)
                        json_data=json.load(file)
                        if link in json_data:
                            #for some reason this is necessary
                            try:json_data[link]["ref"]+=1
                            except KeyError:json_data[link]={"ref":1,"des":info}
                        else:
                            json_data[link]={"ref":1,"des":info }
                        json.dump(json_data, open("data.json",'w'),indent=4)
                    self.crawl(link)

    def start(self):
        self.crawl(self.starting_url)

if __name__ == "__main__":
    url= "https://github.com/"
    with open("data.json",'r') as file:
        json_data=json.load(file)
        x=list(json_data.keys())
        print("Curr size = ",len(x))
        if len(x)!=0:url=x[-1]
    if len(sys.argv)>1:
        url=sys.argv[1]
    print("Start url = ",url)
    crawler = PyCrawler(url)
    crawler.start()
