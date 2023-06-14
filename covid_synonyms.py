import os
import requests

from bs4 import BeautifulSoup

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

CTD_COVID_SYNONYMS_PAGE = 'http://ctdbase.org/detail.go?type=disease&acc=MESH%3AD000086382'

mesh_id = ''

covid19_synonyms = []

try:

   sy_page = requests.get(CTD_COVID_SYNONYMS_PAGE)
   soup = BeautifulSoup(sy_page.text, 'html.parser')

   for sy in soup.find_all('a', attrs={'title': 'Keyword query'}):
      covid19_synonyms.append(sy.getText().lower())

   mesh_id = soup.find('td', class_='gridrow0 maxwidth acclist').get_text().strip()

except requests.exceptions.RequestException as ex:
   raise SystemExit(ex)

 
with open(os.path.join(DIR_PATH, 'ctd_database', 'covid_synoms.txt'), encoding='utf-8') as fle_in: 
   fle_out = open(os.path.join(DIR_PATH, 'ctd_database', 'ctd_covid.txt'), 'w', encoding='utf-8')

   for ln in fle_in.readlines():
      syn_covid = ln.strip()

      if syn_covid not in covid19_synonyms:
         covid19_synonyms.append(syn_covid)

   for sy in covid19_synonyms:
      fle_out.write(f'{mesh_id}\t{sy}\n')
   
   fle_out.close()
