import re
import func_helpers

from scispacy_covid_chemicals import SciSpacyCovidChemicals

class PubtatorSemevalFormatter: 

   annotator = None

   def __init__(self):
        print("Initializing Pubtator Semeval Formater...")
        self.annotator = SciSpacyCovidChemicals()

   def run(self, input_file, output_file):
      title = ''
      abstract = ''
      entities = []

      fl = open(input_file, encoding='utf-8')
      fl_outs = open(output_file, mode='w', encoding='utf-8')

      for ln in fl:
         ln = ln.rstrip()
         
         #  GET Title
         if re.match("^[0-9a-z]+\|t\|", ln):
            title = ln

         # GET Abstract
         elif re.match("^[0-9a-z]+\|a\|", ln):
            abstract = ln

         # GET the list of Entities
         elif re.match("^[0-9a-z]+\t[0-9]+\t[0-9]*\t.+\t.+\t[DC0-9|\-]+", ln):
            matcher = re.match("^([0-9a-z])+\t([0-9])+\t([0-9]*)\t(.+)\t(.+)\t([DC0-9|\-]+)", ln)
            entity_id = matcher.group(6)

            if entity_id != '-1':
               entities.append(ln)

         # GET the list of relation among entities
         elif re.match('^[0-9a-z]+\tCID\t[DC0-9|\-]+\t[DC0-9|]+', ln):
            pass  

      doc = re.match("^[0-9a-z]+\|t\|(.*)($)", title).group(1) + ' ' + \
         re.match('^[0-9a-z]+\|a\|(.*)($)', abstract).group(1)
      
      tokenized_txt = self.annotator.tokenize(doc)

      # Generating the canditate Chemical-Disease pairs
      for ent1 in entities:
         ent1_match = re.match("^([0-9a-z]+)\t([0-9]+)\t([0-9]+)\t(.+)\t(.+)\t([DC0-9|]+)", ent1)

         ent1_document_id = ent1_match.group(1)
         ent1_start = int(ent1_match.group(2))
         ent1_end = int(ent1_match.group(3))
         ent1_name = re.sub('[ ]', '#', ent1_match.group(4))
         ent1_type = ent1_match.group(5)
         ent1_id = ent1_match.group(6)

         for ent2 in entities:
            ent2_match = re.match("^([0-9a-z]+)\t([0-9]+)\t([0-9]+)\t(.+)\t(.+)\t([DC0-9|]+)", ent2)
            ent2_start = int(ent2_match.group(2))
            ent2_end = int(ent2_match.group(3))
            ent2_name = re.sub('[ ]', '#', ent2_match.group(4))
            ent2_type = ent2_match.group(5)
            ent2_ids = ent2_match.group(6)

            for ent2_id in ent2_ids.split('|'):
               if 'Chemical' in ent1_type and 'Disease' in ent2_type:
                  sentence, ent1_position_id, ent2_position_id = self.get_sentence(
                     tokenized_txt, 
                     ent1_start,
                     ent1_end,
                     ent2_start,
                     ent2_end,
                     ent1_name,
                     ent2_name 
                  )

                  '''
                  удалить длинные предложения (т. е. предложения длиннее 218 слов, 
                  что является максимальным количеством слов в предложении в наборе данных, 
                  используемом для обучения системы)
                  '''
                  if len(sentence) != 0 and len(sentence.split(' ')) <= 218:

                     fl_outs.write(
                        ent1_document_id +"\t" + "CID:0" + 
                           "\t" + ent1_id + "\t" + ent2_id + 
                           "\t" + ent1_name + "\t" + ent2_name +
                           "\t" + str(ent1_position_id) + "\t" + 
                           str(ent2_position_id) + "\t" + sentence + "\n")
                     

      fl.close()
      fl_outs.close()


   def get_sentence(self, text, e1_start, e1_end, e2_start, e2_end, e1_name, e2_name):
      out_sentence = ""

      e1_position_id = None
      e2_position_id = None

      e1_in_sentence = False
      e2_in_sentence = False

      if e1_start == e2_start:
         return out_sentence, e1_position_id, e2_position_id
      
      for in_sentence in text:
         out_sentence = ""

         id = 0
         for token in in_sentence:
            start = token[1]
            end = token[2]
            form = token[3]

            if e1_name in form and e1_start >= start and e1_end <= end:
               e1_in_sentence = True
               e1_position_id = id
               id = id + 1
               out_sentence = out_sentence + " " + form

            elif form in e1_name and start >= e1_start and end <= e1_end:
               e1_in_sentence = True
               if not out_sentence.endswith(e1_name):
                  e1_position_id = id
                  id = id + 1
                  out_sentence = out_sentence + " " + e1_name

            elif e2_name in form and e2_start >= start and e2_end <= end:
               e2_in_sentence = True
               e2_position_id = id
               id = id + 1
               out_sentence = out_sentence + " " + form
            
            elif form in e2_name and start >= e2_start and end <= e2_end:
               e2_in_sentence = True
               if not out_sentence.endswith(e2_name):
                  e2_position_id = id
                  id = id + 1
                  out_sentence = out_sentence + " " + e2_name

            else:
               out_sentence = out_sentence + " " + form
               id = id + 1

         if e1_in_sentence == True and e2_in_sentence == True:
            break

         out_sentence = ""
         e1_position_id = None
         e2_position_id = None
         e1_in_sentence = False
         e2_in_sentence = False

      return out_sentence.lstrip(), e1_position_id, e2_position_id


pubtator_semeval_formatter = PubtatorSemevalFormatter()
pubtator_semeval_formatter.run(
   func_helpers.fpath('outputs', '426da_annotate.pubTator.txt'),
   func_helpers.fpath('outputs', '426da_annotate.semeval.txt')
)

   