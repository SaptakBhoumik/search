import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
def crawl(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
    f = requests.get(url, headers = headers)
    link_lst = []
    soup = BeautifulSoup(f.content, 'lxml')
    links = soup.find_all('a')
    for anchor in links:
        urls=""
        try:
            href=anchor['href'] 
            if "?" not in href:
                if "https://" in href or "http://" in href:
                    urls=href
                else:
                    urls = urljoin(url, anchor['href'])
        except:pass
        
        link_lst.append(urls)
    return link_lst
def main():
    x=crawl("https://en.wikipedia.org/")
    for y in x:
        print(y)
        try:
            z=crawl(y)
            for i in z:print(i)
        except:pass
main()