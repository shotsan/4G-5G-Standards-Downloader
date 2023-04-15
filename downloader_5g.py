## Author: Santosh Ganji
## Downloads all the 5G ETSI standards in one shot


## necessary libraries
import requests
import re
from bs4 import BeautifulSoup
import concurrent.futures
import multiprocessing
import os

# change the URL to download other specifications

URL = 'https://www.etsi.org/deliver/etsi_ts/138100_138199/'


# scraps all the url links
pdfs=[]
def get_pdf_links(url):
    reguest = requests.get(url)
    soup = BeautifulSoup(reguest.text, 'html.parser')
    for l in soup.find_all('a', href=True):
        if l['href'].endswith('.pdf'):
            pdfs.append('www.etsi.org'+l['href'])
            return 
            

def get_urls(url):
    reguest = requests.get(url)

    soup = BeautifulSoup(reguest.text, 'html.parser')
    urls=[]
    for l in soup.find_all('a', href=True):
        urls.append('https://www.etsi.org'+l['href'])
    
    #print(urls)
    return urls



# change URL for other locations
spec_urls=get_urls(URL)
spec_urls=spec_urls[1:-1]

spec_urls_inner=[]
for items in spec_urls:
    spec_urls_inner.extend(get_urls(items))


for l in spec_urls:
    try:
        #print('ts_'+l.split('/')[-2])
        os.mkdir('ts_'+l.split('/')[-2])
    except:
        pass

# collects all the URLs
 
with concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
    executor.map(get_pdf_links, spec_urls_inner)
 
# saves the PDFs in the right folders

def save_pdf(link):
    folder_name='ts_'+link.split('/')[-3]
    print(folder_name)
    reguest = requests.get('https://'+link)
    with open(folder_name+'/'+link.split('/')[-1], 'wb') as f:
        f.write(reguest.content)
        print('saved '+link.split('/')[-1])
# Parallel execution of the downloads

with concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
    executor.map(save_pdf, pdfs)
