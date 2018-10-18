from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from file_handler import FileHandler
from database_handler import DatabaseHandler

def save_data_in_db(doc):
    database_handler = DatabaseHandler()
    database_handler.prepare_query([doc['title'] , doc['link'],doc['image'], doc['desc'], doc['author'], doc['comment'], doc['digest'], str(doc['category']), doc['source'], str(doc['tags'])])
    database_handler.executor()
    database_handler.close()

def crawl_page(url):
    # url='http://www.zoomit.ir/2017/3/27/154273/instagram-two-factor-authentication-learning/'
    doc = {}
    html_doc = urlopen(url)
    soup = bs(html_doc, 'html.parser')
    desc = soup.find(class_='article-section')
    for div in desc.find_all("div", {'class':'larticle'}):
        div.decompose()
    try:
        source = soup.find(class_='article-source-row').find('a').get_text()
    except AttributeError as e:
        source=""
        filehandler = FileHandler("log_crawl.txt")
        filehandler.write('''soup.find(class_='article-source-row').find('a').get_text()''')
        filehandler.write(url)
        filehandler.write(str(e)+ "\n")
    try:
        tags = soup.find(class_='article-tag-row').find_all('a')
    except AttributeError as e:
        tags=""
        filehandler = FileHandler("log_crawl.txt")
        filehandler.write('''tags = soup.find(class_='article-tag-row').find_all('a')''')
        filehandler.write(url)
        filehandler.write(str(e)+ "\n")

    doc.update({'desc': desc,'source': source, 'tags':tags})
    return doc

url = "http://www.zoomit.ir/category/internet-learning/"
while url!="":
    data = []
    html_doc = urlopen(url)
    soup = bs(html_doc, 'html.parser')
    article= soup.find(id="ArticleDetails")
    url = soup.find('ul',class_='pagination')
    url = url.find_all('li')
    url = url[len(url)-1].find('a')['href']
    print(url)
    rows= article.find_all(class_='row')
    for row in rows:
        datarow={}
        img = row.find('img')['src']
        subject = row.find('h3')
        title = subject.get_text()
        link= subject.find('a')['href']
        auther= row.find(class_='authorlist').get_text()
        comment= row.find(class_='z-comment-block').find('span').get_text()
        categories= row.find(class_='catgroup').find('ul').find_all('li')
        digest = row.find(class_='hidden-sm').get_text()

        # print(img)
        # print(title)
        # print(link)
        # print(auther)
        # print(comment)
        # print(digest)
        # print(categories)
        cate = []
        for category in categories:
            cate.append(category.get_text())
        datarow.update({'image':img, 'title':title, 'link':link, 'author':auther, 'comment':comment, 'digest':digest, 'category':cate})
        data.append(datarow)
        # print(row.prettify())
    print(len(data))
    for i in range(len(data)):
        print(data[i]['title'])
        doc = crawl_page(data[i]['link'])
        data[i].update(doc)
        save_data_in_db(data[i])
    # [print(d) for d in data]

