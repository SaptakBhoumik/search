
import json
import requests    
import re    
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
        return html.content.decode('latin-1')    

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
        html = self.get_html(url)    
        meta = re.findall("<meta .*?name=[\"'](.*?)['\"].*?content=[\"'](.*?)['\"].*?>", html)    
        return dict(meta)    

    def crawl(self, url):    
        for link in self.get_links(url):    
            if link in self.visited:    
                continue    
            self.visited.add(link)    
            info = self.extract_info(link)    
 
            if "?" not in link and ":" not in link:
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
        if len(x)!=0:url=x[-1]
    print(url) 
    crawler = PyCrawler(url)     
    crawler.start()
