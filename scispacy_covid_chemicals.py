import spacy

import func_helpers

class SciSpacyCovidChemicals:
   def __init__(self) -> None:
      print('initilizing SciSpacy...')

      # загрузить модель scispaCy
      self.covid_chemicals_nlp = spacy.load('en_core_sci_lg')
      self.chemicals_vocabs = self.chs_vocabs()
      self.covid_syns = self.covid_synonyms()

   def tokenize(self, text):

        annotatedDocument = [] 

        doc = self.covid_chemicals_nlp(text)
        
        token_index = 0
        sentence = []
        for token in doc:
            if token.is_sent_start == True and len(sentence) != 0:
                annotatedDocument.append(sentence)
                sentence = []

            row = [token_index, token.idx, token.idx + len(token.text), token.text]
            sentence.append(row)
            token_index = token_index + 1

        annotatedDocument.append(sentence)

        return annotatedDocument
   
   
   def analyze_covid19(self, text):
      recognized_entities = [] 
      doc = self.covid_chemicals_nlp(text)

      entity = []
      for token in doc:

         entity_iob = token.ent_iob_

         if entity_iob == "B":
               if entity != []:
                  mesh_id = None
                  entity_type = None
                  if entity[2].lower() in self.chemicals_vocabs:
                     mesh_id = self.chemicals_vocabs[entity[2].lower()]
                     entity_type = "Chemical"
                  elif entity[2].lower() in self.covid_syns:
                     mesh_id = self.covid_syns[entity[2].lower()]
                     entity_type = "Disease"
                  if mesh_id != None:
                     entity[3] = entity_type
                     entity[4] = mesh_id
                     recognized_entities.append(entity.copy())
               entity = [token.idx, token.idx + len(token.text), token.text, None, None]
         elif entity_iob == "I":
               entity = [entity[0], token.idx + len(token.text), entity[2] + " " + token.text, None, None]
         else:
               if entity != []:
                  mesh_id = None
                  entity_type = None
                  if entity[2].lower() in self.chemicals_vocabs:
                     mesh_id = self.chemicals_vocabs[entity[2].lower()]
                     entity_type = "Chemical"
                  elif entity[2].lower() in self.covid_syns:
                     mesh_id = self.covid_syns[entity[2].lower()]
                     entity_type = "Disease"
                  if mesh_id != None:
                     entity[3] = entity_type
                     entity[4] = mesh_id
                     recognized_entities.append(entity.copy())
                  entity = []

      return recognized_entities

   def chs_vocabs(self):
      chs = {} 

      with open(func_helpers.fpath('ctd_database', 'ctd_chemicals.txt'), encoding='utf-8') as fl:
         for ln in fl.readlines():
            ch = ln.strip().split('\t')
            chs[ch[1]] = ch[0]

      return chs

   
   def covid_synonyms(self):
      csyns = {}

      with open(func_helpers.fpath('ctd_database', 'ctd_covid.txt'), encoding='utf-8') as fl:
         for ln in fl.readlines():
            csyn = ln.strip().split('\t')
            csyns[csyn[1]] = csyn[0]
      
      return csyns
