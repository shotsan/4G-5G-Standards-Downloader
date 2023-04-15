## Author: Santosh Ganji
## Downloads all the 4G ETSI standards in one shot


## necessary libraries
import requests
import re
from bs4 import BeautifulSoup
import concurrent.futures
import multiprocessing
import os

# scraps all the url links

def get_pdf_links(url):
    reguest = requests.get(url)

    soup = BeautifulSoup(reguest.text, 'html.parser')
    links=[]
    for link in soup.find_all('a', href=True):
        links.append('https://www.etsi.org/'+link['href'])
    
    pdfs=[]
    for link in links:
        reguest = requests.get(link)
        soup = BeautifulSoup(reguest.text, 'html.parser')
        for inner_link in soup.find_all('a', href=True):
            if inner_link['href'].endswith('.pdf'):
                print('www.etsi.org'+inner_link['href'])
                pdfs.append('www.etsi.org'+inner_link['href'])
                break
            # get the pdf
           
    return pdfs

#  4G URLs from the ETSI

url='https://www.etsi.org/deliver/etsi_ts/136100_136199/'
url_list=['136101','136104','136106','136111','136113','136116','136117','136124','136133','136141','136143','136171']

for l in url_list:
    try:
        os.mkdir('ts_'+l)
    except:
        pass 



# collects all the URLs
final_list=[]
pdfs=[]
for list in url_list:
    final_list.append(url+list)

for url in final_list:
    pdfs.extend(get_pdf_links(url))



# saves the URLs in the right folders

def save_pdf(link):
    reguest = requests.get('https://'+link)
    file_name=link.split('/')[-1]
    
    for url in url_list:
        if re.search(url,link.split('/')[-1]):
            with open('ts_'+url+'/'+link.split('/')[-1], 'wb') as f:
                f.write(reguest.content)
                print('saved '+link.split('/')[-1])

# Parallel execution of the downloads

with concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
    executor.map(save_pdf, pdfs)
 
