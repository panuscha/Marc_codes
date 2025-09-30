""" Skript který spočítá kolik je záznamů, nejstarší a nejnovější záznam a velikost databáze vytvořené pomocí divide_databases_ucla_mrc.py"""

import pandas as pd
from pymarc import MARCReader
import os

# Cesta k jednotlivym databazim vytvorenym v divide_databases_ucla_mrc.py
path = "data/ucla test/ucla_"

out_B = 'soucasna'
out_1945 = '1945'
out_alkaro = 'alkaro'
out_ret = 'ret'
out_smz = 'smz'
out_int = 'int'
out_cle_I = 'cle_I'
out_cle_II = 'cle_II'
out_trl = 'trl'
out_mbk = 'mbk'
out_all = 'all'

databases = [out_B, out_alkaro, out_ret, out_smz, out_int, out_cle_I, out_cle_II, out_trl, out_mbk, out_all]

## https://stackoverflow.com/questions/2104080/how-do-i-check-file-size-in-python
def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

# Zjisti pocet zaznamu v kazde databazi a nejstarsi a nejmladsi zaznam
def number_of_records(database):
    
    with open(database, 'rb') as data:
        # Nacteni marcu
        reader = MARCReader(data)
        
        counter = 0
        
        # Pro urceni nejstarsiho a nejmladsiho roku
        newest = 0000
    
        # Pro urceni nejstarsiho a nejmladsiho roku
        oldest = 2025
        
        # Projdi vsechny zaznamy
        for record in reader:
            for field in record.get_fields('008'):
                
                # Rok je na pozici 7-10
                year = field.data[slice(7,11, None)]
                
                if year.isnumeric():
                    year = int(year)
                    if year < oldest:
                        oldest = year
                
                    if newest < year:
                        newest = year    
            
            counter += 1
    return (counter, oldest, newest) 


res = {'': ('Počet záznamů', 'Nejstarší','Nejnovější', 'Velikost v bajtech' )}
# Projdi vsechny databaze
for database in databases:
    # Cesta 
    path_to_database = path + database + ".mrc"
    # Velikost Databáze
    size = str(os.path.getsize(path_to_database)) 
    # Pocet zaznamu, nejstarsi a nejmladsi zaznam
    (counter, oldest, newest) = number_of_records(path_to_database)
    print("Database " + database + " has " + str(counter) + " records. Latest: " + str(newest) + "; Oldest: " + str(oldest) + "; Size: " + str(size))
    res[database] = (counter, oldest, newest, size)

# Prevod na dataframe    
df = pd.DataFrame.from_dict(res)
out_excel = 'data/out_stats.xlsx'
df.to_excel(out_excel, index=False)       
    
    