import pandas as pd
from pymarc import MARCReader, map_xml, MARCWriter
from collections import defaultdict 
import csv

# out_old = 'data/ucla test/ucla_old_values.mrc'
# out_old_new = 'data/ucla test/ucla_old_in_ucla.mrc'

# writer_old_values =  MARCWriter(open(out_old, 'wb'))
# writer_old_values_in_all =  MARCWriter(open(out_old_new, 'wb'))

# def get_records(database, writer): 
#     global old_values
#     counter = 0
#     with open(database, 'rb') as data:
#         reader = MARCReader(data)
#         for record in reader:
#             for field in record.get_fields('001'):
#                 if field.data in old_values.keys():
#                     writer.write(record) 
#                     print(record)
#                     counter += 1 
#     writer.close()
#     return counter                


def number_of_records(database):
    d = defaultdict(lambda: 0) 
    counter = 0
    with open(database, 'rb') as data:
        reader = MARCReader(data)
        
        for record in reader:
            for field in record.get_fields('001'):
                d[field.data] += 1 
                counter += 1
        print('Counter: ', counter) 
        return counter, d 

path = "data/ucla test/ucla_all.mrc"

path_2 = "data/ucla test/ucla_soucasna_nova.mrc"

path_3 = 'data/ucla.mrc'

counter, d = number_of_records(path)

double_values = {k: v for k,v in d.items() if float(v) > 1}

print('Number of multiple values in old dataset: ', len(double_values))
print('Unique values in old dataset: ', counter - len(double_values)) 
print('Check unique values in old dataset: ', len(d.keys())) 

# counter,d_2 = number_of_records(path_2)

# double_values_2 = {k: v for k,v in d.items() if float(v) > 1}

# print('Multiple values in new dataset: ', len(double_values_2))
# print('Unique values in new dataset: ', counter - len(double_values_2)) 

# old_values = {k: v for k,v in d.items() if k not in d_2.keys()}
# print('Number of old values: ', len(old_values))


# new_values = {k: v for k,v in d_2.items() if k not in d.keys()}
# print('Number of new values: ', len(new_values))

# length = get_records(path, writer_old_values)
# print('Number of old values in old dataset: ', length)
# length_3 = get_records(path_3, writer_old_values_in_all)
# print('Number of old values in dataset ucla: ', length_3)





