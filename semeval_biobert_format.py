import func_helpers

# def create_training_dataset(file_in, file_out):
#    output_file = open(file_out, 'w', encoding='utf-8')

#    for line in open(file_in, encoding='utf-8'):

#       splits = line.strip().split('\t')

#       label = splits[1]
#       new_label = None
#       if label == "CID:0":
#          new_label = "0"
#       else:
#          new_label = "1"

#       entity1_pos = int(splits[6])
#       entity2_pos = int(splits[7])

#       example = ""
#       if entity1_pos == entity2_pos:
#          example = "@GENE$ @DISEASE$\t0"

#       else:
#          sentence = splits[8].split(" ")
#          sentence[entity1_pos] = "@GENE$"
#          sentence[entity2_pos] = "@DISEASE$"

#          example = ' '.join(sentence) + "\t" + new_label

#       output_file.write(example + "\n")

#    output_file.close()


def create_test_dataset(file_input, file_output):
   """
   Creates the dataset to be annotaed in the BioBERT format

   :param file_input: the dataset in Semeval format
   :param file_output: the dataset in BioEBRT format

   """

   output_file = open(file_output, 'w', encoding='utf-8')
   output_file.write("index	sentence	label\n")

   counter = 0
   for line in open(file_input, encoding='utf-8'):

      splits = line.strip().split('\t')

      label = splits[1]
      new_label = None
      if label == "CID:0":
         new_label = "0"
      else:
         new_label = "1"

      docId = splits[0]
      entity1_pos = int(splits[6])
      entity2_pos = int(splits[7])

      example = ""
      if entity1_pos == entity2_pos:
         example = str(counter) + "\t" + "@GENE$ @DISEASE$\t0"

      else:

         sentence = splits[8].split(" ")
         sentence[entity1_pos] = "@GENE$"
         sentence[entity2_pos] = "@DISEASE$"

         example = str(counter) + "\t" +  ' '.join(sentence) + "\t" + new_label

      output_file.write(example + "\n")

      counter = counter + 1

   output_file.close()

input_file = func_helpers.fpath('outputs', '426da_annotate.semeval.txt')
output_file = func_helpers.fpath('outputs', input_file.split('/')[-1].split('.')[0] + '.biobert.txt')

create_test_dataset(input_file, output_file)