from pymarc import map_xml, MARCWriter, MARCReader
from collections import defaultdict
import pandas as pd

m = set()
b = set()
b_cle = set()
m_alkaro = {'Almanach':[], 'Rok vydání': []}

with open('data/ucla test/ucla_smz.mrc', 'rb') as data:
    # Nacteni marcu
    reader = MARCReader(data)
    for record in reader: 
        leader = record.leader
        l_8 = leader[7]
        if l_8 == 'm':
            m.add(record.title.strip(' /'))
        if l_8 == 's':
            m.add(record.title.strip(' /'))    
        if l_8 == 'b': 
            magazin = record['773']['t']
            if '[samizdat]' in magazin: magazin = magazin[:-11]
            b.add(magazin)    

with open('data/ucla test/ucla_alkaro.mrc', 'rb') as data:
    # Nacteni marcu
    reader = MARCReader(data)
    for record in reader: 
        leader = record.leader
        l_8 = leader[7]
        if l_8 == 'm' or l_8 == 's':
            m_alkaro['Almanach'].append(record.title.strip(' /.'))
            try:
                m_alkaro['Rok vydání'].append(record['264']['c'].strip('.[]')) 
            except:     
                m_alkaro['Rok vydání'].append('Not found')

with open('data/ucla test/ucla_cle_I.mrc', 'rb') as data:
    # Nacteni marcu
    reader = MARCReader(data)
    for record in reader: 
        leader = record.leader
        l_8 = leader[7]
        if l_8 == 'b': 
            magazin = record['773']['t']
            b_cle.add(magazin)       

print(f'Počet sborníků SMZ {len(m)}')
alkaro_n = len(m_alkaro['Almanach'])
print(f'Počet almanachů v ALKARO {alkaro_n}')
print(f'Počet časopisů SMZ {len(b)}')
print(f'Počet časopisů CLE {len(b_cle)}')
print(b_cle)
m = list(m)
b = list(b)
max_len = max(len(m), len(b))
m += [None] * (max_len - len(m))
b += [None] * (max_len - len(b))
df = pd.DataFrame({'Sborníky': m, 'Časopisy':b})
df.to_excel('data/SMZ_Sborníky_Casopisy.xlsx')

df = pd.DataFrame({'Časopisy':list(b_cle)})
df.to_excel('data/CLE_Casopisy.xlsx')

df = pd.DataFrame(m_alkaro)
df.to_excel('data/ALKARO_Almanachy.xlsx', index = False)

