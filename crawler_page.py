from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
def crawl_page(url):
    # url='http://www.zoomit.ir/2017/3/27/154273/instagram-two-factor-authentication-learning/'
    html_doc = urlopen(url)
    soup = bs(html_doc, 'html.parser')
    desc = soup.find(class_='article-section')
    for div in desc.find_all("div", {'class':'larticle'}):
        div.decompose()
    source = soup.find(class_='article-source-row').find('a').get_text()
    tags = soup.find(class_='article-tag-row').find_all('a')

    print(desc)
    print(source)
    print(tags)

