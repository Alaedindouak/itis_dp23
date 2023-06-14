import func_helpers

def read_predictions(results_file):
   '''
      Reads the labels assigned by BioBERT to the candidate entity pairs

      :param results_file: the predicted labels 
      :return: the list of predicted labels
   '''
   classes = []
   for ln in open(results_file, encoding='utf-8'):
      ln = ln.strip()
      classes.append(ln)
   return classes

pubTator_flname = func_helpers.fpath(
   'outputs', '426da_annotate.pubTator.txt')

semeval_flname = func_helpers.fpath(
   'outputs', 'annotated.semeval.txt')

result_flname = func_helpers.fpath(
   'outputs', 'annotated_rel.pubTator.txt')


predictions = read_predictions(
   func_helpers.fpath('outputs', 'biobert_predicted.txt'))

with open(result_flname, mode='w', encoding='utf-8') as outp:
   
   counter = 0
   visited = {}
   docid_label_map = {}

   for semeval_fl in open(semeval_flname, encoding='utf-8'):
      splits = semeval_fl.strip().split('\t') 
      
      doc_id = splits[0] # document id
      e1_id = splits[2]  # chemical mesh id
      e2_id = splits[3]  # covid mesh id

      label = predictions[counter]
      
      if label != 'CID:0': # getting positive results CID:1
         label = 'CID'

         value = doc_id + "\t" + label + "\t" + e1_id + "\t" + e2_id

         if value not in visited: 
            visited[value] = 1

            if doc_id in docid_label_map: # add relations with document id  
               entry = docid_label_map[doc_id]
               entry.append(value)

            else:
               entry = []
               entry.append(value)
               docid_label_map[doc_id] = entry               
      counter += 1

   
   doc_id = ""
   prev_doc_id = ""
   string_buffer = ""
   for line in open(pubTator_flname, encoding="utf8"):
      line = line.strip()
      if line != "":
         splits = line.split('\t')
         if '|t|' in line:
               if string_buffer != "":
                  if doc_id in docid_label_map:
                     entry = docid_label_map[doc_id]
                     for rel in entry:
                           string_buffer = string_buffer + rel + "\n"
                  outp.write("%s\n" % string_buffer)
               string_buffer = line + "\n"

         elif not(len(line.split("\t")) == 4 and 'CID' in line):
               doc_id = splits[0]
               string_buffer = string_buffer + line + "\n"
               
   if string_buffer != "":
      if doc_id in docid_label_map:
         entry = docid_label_map[doc_id]
         for rel in entry:
               string_buffer = string_buffer + rel + "\n"
      outp.write("%s\n" % string_buffer)     





# read_predictions(func_helpers.fpath('outputs', 'biobert_predicted.txt'))
