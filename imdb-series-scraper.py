import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

title=[]
gener = []
rate=[]
act=[]
vote =[]
num = np.arange(1,2371,50)

# Loop for scraping Data
for i in num :
    url = "https://www.imdb.com/search/title/?title_type=tv_series&countries=tr&start=" + str(i)
    page = requests.get(url)
    soup = BeautifulSoup(page.text , "html.parser")
    movies = soup.find_all("div" , class_="lister-item mode-advanced")
    for movie in movies :
        title.append(re.findall(r"\d.+\n(\w.+)" , movie.text))
        gener.append(re.findall(r"\d.+min\n.+\n\n(.+)" , movie.text))
        rate.append(re.findall(r"10\n\s(\d.\d)" , movie.text))
        act.append(re.findall(r"Stars:\n(\w.+\n\w.+\n\w.+\n\w.+)" , movie.text))
        vote.append(re.findall(r"Votes:\n(\d.+)" , movie.text))

# Excel
data = {"Title":title , "Gener" : gener , "Rate":rate , "Stars":act , "Vote":vote}
df = pd.DataFrame(data)
writer = pd.ExcelWriter("TSeries.xlsx")
df.to_excel(writer , "sheet1")
writer.save()
