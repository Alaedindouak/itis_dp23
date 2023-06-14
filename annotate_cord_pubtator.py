import os
import json

from scispacy_covid_chemicals import SciSpacyCovidChemicals

covid_chemicals_tokenizer = SciSpacyCovidChemicals()

DIR_PATH = os.path.dirname(os.path.abspath(__file__))
# getting CORD-19 datasets files
cord19_flS = [fl for _, _, fls in os.walk(os.path.join(DIR_PATH, 'cord_dataset')) for fl in fls] 

for fl in cord19_flS:
   flname = fl.split('.')[0][:5] + '_annotate.pubTator.txt'
   annotated_dt = open(os.path.join(DIR_PATH, 'outputs', flname), mode='w', encoding='utf-8')

   with open (os.path.join(DIR_PATH, 'cord_dataset', fl), encoding='utf-8') as jf:
      data = json.load(jf)

      title = data['metadata']['title'].strip()
      if not title.endswith('.'):
         title += '.'
      
      abstract = ''
      abstracts = data['abstract']

      if len(abstracts) > 0:
         for txt in abstracts:
            if not abstract:
               abstract = txt['text']
            else:
               abstract = abstract + ' ' + txt['text'].strip()
            
         if not abstract.endswith('.'):
            abstract += '.'

      for txt in data['body_text']:
         text = txt['text'].strip()

         if not abstract.endswith('.') and text[0:1].isupper():
            abstract = abstract + '. ' + text
         else:
            abstract = abstract + ' ' + text 

      processed_txt = title + '\n' + abstract

      chemical_found = False
      disease_found = False

      # 
      entities = covid_chemicals_tokenizer.analyze_covid19(processed_txt)
     

      for entity in entities:
         if entity[3] == 'Chemical':
            chemical_found = True
         if entity[3] == 'Disease':
            disease_found = True

      if chemical_found and disease_found:
         annotated_dt.write('{0}|t|{1}\n'.format(fl[:-5], title))
         annotated_dt.write('{0}|a|{1}\n'.format(fl[:-5], abstract))

         for entity in entities:
            annotated_dt.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n'.format(fl[:-5], \
               str(entity[0]), str(entity[1]), entity[2], entity[3], entity[4]))   

      annotated_dt.close()
