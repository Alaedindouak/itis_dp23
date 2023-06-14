import func_helpers

predicted_results = func_helpers.fpath('biobert/RE_output', 'test_results.tsv')

with open(func_helpers.fpath('outputs', 'biobert_predicted.txt'), mode='w' ,encoding='utf-8') as out:
   for ln in open(predicted_results, encoding='utf-8'):
      ln = ln.strip()

      if ln != "":
         predCPR0 = float(ln.split("\t")[0])
         predCPR1 = float(ln.split("\t")[1])

         if predCPR0 > predCPR1:
            label = "CID:0"
         else:
            label = "CID:1"

         out.write(label + '\n')
