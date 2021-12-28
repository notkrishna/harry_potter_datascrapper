import pandas as pd
from bs4 import BeautifulSoup as s
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

r = requests.get('https://www.goodreads.com/search?utf8=%E2%9C%93&q=harry+potter&search_type=books&search%5Bfield%5D=title')
soup = s(r.content, 'html.parser')

links = []
title = []
for i in soup.findAll('a',{'class':'bookTitle'})[:8]:
    links.append('https://goodreads.com'+i.get('href'))
    title.append(i.get_text().strip())


def scrapper(w,d,ls):
    fi = soup.findAll(w,d)
    if fi:
        for i in fi: 
            ls.append(i.get_text())
    else:
        ls.append('')

r = []
rdesc = []
r2 = []
like_count = []
title = []

b = webdriver.Chrome(ChromeDriverManager().install())

for l in links:
    rs2 = requests.get(l)
    b.get(l)
    seconds = 5 + (random.random() * 5)
    b.implicitly_wait(30)
    
    
    for i in range(3):
        h = b.page_source
        soup = s(h, 'html.parser')
        for t in range(30):
            title.append(soup.find('h1',{'id':'bookTitle'}).get_text())
        scrapper('div',{'class':'reviewHeader'},r)
        scrapper('div',{'class':'review'},r2)
        scrapper('div',{'class':'reviewText'},rdesc)
        
        for r in soup.select('div.review span.likesCount'):
            like_count.append(r.get_text())

        e = b.find_element(By.CLASS_NAME,'next_page')
        b.execute_script('arguments[0].click()',e)
        time.sleep(seconds)

rde2 = rdesc.copy()
rde2 = [i.strip().replace('\xa0','').replace('...more','') for i in rde2]
rc = r.copy()
rc = [i.strip().replace(' ','').split('\n') for i in rc]

rdate = []
rname = []
rrating = []
recc = []
shelves = []
rev = []
likes = []
comm = []


for i in rc:
    rname.append(i[2])
    rdate.append(i[0])
    if i[5]=='ratedit':
        rrating.append(i[6])
    else:
        rrating.append('')

title = [i.strip() for i in title]

dt = pd.DataFrame({'book':title,'name':rname,'date':rdate,'rating':rrating,'likes':like_count,'description':rde2})

def stars(t):
    d = {'itwasamazing':5,'reallylikedit':4,'likedit':3,'itwasok':2,'didnotlikeit':1, '':''}
    return d[t]

dt2 = dt.rating
dt['stars_given'] = dt2.apply(lambda x: stars(x))
dt.to_csv('lightning.csv')

pd.read_csv('lightning.csv')