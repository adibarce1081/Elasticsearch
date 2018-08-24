from bs4 import BeautifulSoup
import requests
import re
import json
from elasticsearch import Elasticsearch
h = 0
headers1 = {"User-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"}
src_url = 'https://health.usnews.com/doctors/city-index/new-jersey'
src0 = requests.get(src_url,headers=headers1).text

cities = BeautifulSoup(src0,'lxml')
city_div = cities.find_all('div',class_='Content-o0f126-0 content kteJom')
city_div = city_div[2]
for a in range(0,5):
    city_list = city_div.find_all('li',class_='List__ListItem-dl3d8e-1 kfaWAY')
    city_list = city_list[a]
    city_list_link = 'https://health.usnews.com' + city_list.a['href']
    #print city_list_link
    src3 = requests.get(city_list_link,headers=headers1).text
    spl = BeautifulSoup(src3,'lxml')
    sp_div = spl.find_all('div',class_='Content-o0f126-0 content kteJom')
    sp_div = sp_div[2]
    
    for b in range(0,5):
        
        sp_list=sp_div.find_all('li',class_='List__ListItem-dl3d8e-1 kfaWAY')
        sp_list = sp_list[b]
        sp_list_link = 'https://health.usnews.com' + sp_list.a['href']  
        print sp_list_link
        print '\n'
        url = sp_list_link
        src = requests.get(url,headers=headers1).text
        soup = BeautifulSoup(src,'lxml')
        for c in range(0,5):
            
            doc_list = soup.find_all('li', class_ = 'block-normal block-loose-for-large-up')
            doc_list = doc_list[c]
            doc_link = doc_list.h3.a['href']
            doc_link1 = 'https://health.usnews.com' + doc_link
                

            src1 = requests.get(doc_link1,headers=headers1).text
            soup1 = BeautifulSoup(src1,'lxml')
           
            doc_ref = soup1.find('div', class_ ='flex-row relative' ).h1.text
            doc_name = re.findall('[a-zA-Z0-9]\S*',str(doc_ref))
            doc_name = ' '.join(doc_name)
            print doc_name

           
            doc_ov1 =' '
            doc_ov = soup1.find('div', class_ ='block-normal clearfix' ).p.text
            doc_ov = re.findall('[a-zA-Z0-9]\S*',str(doc_ov))
            doc_ov = doc_ov1.join(doc_ov)
            print doc_ov
            
            doc_ex = soup1.find_all('span', class_ ='text-large heading-normal-for-small-only right-for-medium-up')
            doc_ex = doc_ex[1]
            doc_ex = doc_ex.text.strip()
            
             
            doc_lan = soup1.find('span', class_ ='text-large heading-normal-for-small-only right-for-medium-up text-right showmore').text.strip()
            print doc_lan
            
            
            doc_loc1 =' '
            doc_loc = soup1.find('div', class_ ='flex-small-12 flex-medium-6 flex-large-5').p.span.text.strip()
            doc_loc = re.findall('[a-zA-Z0-9]\S*',str(doc_loc))
            doc_loc = doc_loc1.join(doc_loc)
            pin_code =  re.findall('[0-9]\S*',str(doc_loc))
            print pin_code[-1]
            print doc_loc
            
            
            try:
                
                doc_aff = soup1.find('a', class_ ='heading-larger block-tight').text
                
            except:
                doc_aff = ['no affiliation found']
                
            print doc_aff
            
            
            try:
                
                doc_sp = soup1.find('div', class_ ='flex-row small-between').a.text.strip()
            except:
                doc_sp = ['no speciality found']
               
            print doc_sp         

           
            
            
            try:
                doc_subsp = soup1.find('p', class_ ='text-large block-tight').text
                   
            except:
                doc_subsp = ['no speciality found']
               
            print doc_subsp
            
            print ' '
            
            doc_ed = soup1.find_all(class_ ="block-loosest")[5]
            doc_ed1 = doc_ed.find_all('li')
            doc_ed6 = list()
            doc_ed5 = ' '
            for i in doc_ed1:
                doc_ed2 = str(i.text)
                doc_ed2 = re.findall('[a-zA-Z0-9]\S*',doc_ed2)
                doc_ed2 = doc_ed5.join(doc_ed2)
                doc_ed6.append(doc_ed2)
            print doc_ed6
            print ' '
            doc_cert2 = []
            doc_cert1 = ' '  
            doc_ed3 = soup1.find_all(class_ ="block-loosest")[6]
            doc_ed14 = doc_ed3.find_all('li')
            for i in doc_ed14:
                doc_cert = str(i.text)
                doc_cert = re.findall('[a-zA-Z0-9]\S*',doc_cert)
                doc_cert = doc_cert1.join(doc_cert)
                doc_cert2.append(doc_cert)
            print doc_cert2
            doc_profile = {
                'Cities':str(city_list.a.text),
                'Name': str(doc_name),
                'Overview': str(doc_ov),
                'Years_of_experience': str(doc_ex),
                'Location':str(doc_loc),
                'Pin_code':str(pin_code[-1]),
                'Affiliation':str(doc_aff),
                'Speciality': str(doc_sp),
                'Sub_speciality':str(doc_subsp),
                'Education':str(doc_ed6),
                'Certification':str(doc_cert2),
                }
            print doc_profile 
            print '\n'
            es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
            x = json.dumps(doc_profile)
            res = es.index(index='a', doc_type='a', id=h, body=json.loads(x))
            print res["result"]
            req = es.get(index='a', doc_type='a', id=h)
            print req
            h += 1
            c += 1
        b += 1
    a += 1
