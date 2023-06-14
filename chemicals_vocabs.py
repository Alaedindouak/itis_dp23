import os
import re
import gzip
import requests

DIR_PATH = os.path.dirname(os.path.abspath(__file__))

CTD_URL = 'http://ctdbase.org/reports/CTD_chemicals.tsv.gz'

flname = CTD_URL.split('/')[-1]

try:

   if not os.path.isfile(os.path.join(DIR_PATH, 'ctd_database', flname)):
      print('downloading datasets ...')
      res = requests.get(CTD_URL)

      f_out = open(os.path.join(DIR_PATH, 'ctd_database', flname), 'wb')
      f_out.write(res.content)

      f_out.close()

except requests.exceptions.RequestException as ex:
   raise SystemExit(ex)


# открыть набор данных
with gzip.open(os.path.join(DIR_PATH, 'ctd_database', flname), 'rt', encoding='utf-8') as f:
   f_out = os.path.join(DIR_PATH, 'ctd_database', re.split('\.tsv', string=flname.lower())[0] + '.txt')
   # откройте файл, в котором будут сохранены данные о химических веществах
   f_out = open(f_out, 'w', encoding='utf-8')

   for line in f.readlines():
      if not line.startswith('#'):
         field = line.rstrip('\n').split('\t')

         chemical_name = field[0] # получить химическое
         chemical_id = field[1][5:] #MeSH ID

         if len(chemical_name) > 4:
            f_out.write(f'{chemical_id}\t{chemical_name.lower()}\n')

         synonyms = field[7].split('|')
         for synonym in synonyms:
            if len(synonym) > 4:
               f_out.write(f'{chemical_id}\t{synonym.lower()}\n')

   f_out.close()

