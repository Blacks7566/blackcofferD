from bs4 import BeautifulSoup
import requests
import pandas as pd 

df = pd.read_csv('./input.csv')
urls = []
file_name = []
id = []
ul = []

for item in range(len(df.URL)):
    urls.append(df.URL[item])
    file_name.append(df.URL_ID[item])

for i in range(len(urls)):
    a = requests.get(urls[i])
    soup = BeautifulSoup(a.content,'html.parser')
    title = soup.find('h1',class_='entry-title')
    article = soup.find('div',class_='td-post-content')
    if title is not None:
        file_object = open(f'articles/{file_name[i]}.txt','w+',encoding="utf-8")
        file_object.write(title.text)
        file_object.write(article.text)
        file_object.close()
        ul.append(urls[i])
        id.append(file_name[i])
    else:
        continue

data = pd.DataFrame({'URL_ID':id,'URL':ul})

data.to_csv('input2.csv',index=False)