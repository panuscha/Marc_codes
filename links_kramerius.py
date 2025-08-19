from pymarc import MARCReader, map_xml
import pandas as pd
import re

periodika = {'001': [],
            'title': [], 
             'issn': [],
             'link': [],
             'domain': [],
             'uuid': [] }

periodika_nk = {'001':[],
            'title': [], 
             'issn': [] }

def condition(field):
    subfields = field.subfields_as_dict()
    return subfields['u'][0] if 'y' in subfields and subfields['y'][0].lower() == 'kramerius' else None 

def get_periodika(record, periodika):
    leader = record.leader
    
    if 'b' in leader[7]:
        try: 
            subfields = record['773'].subfields_as_dict()
            magazin_title =  subfields['t'][0] if 't' in subfields else None
            issn = subfields['x'][0] if 'x' in subfields else record.issn
            periodika['title'].append(magazin_title)
            periodika['issn'].append(issn)
        except: print('Nestandardní záznam')    
    return periodika    

def main():
    periodika = {'title': [], 'issn': []}
    d = 'all'
    database = f'data/ucla test/ucla_{d}.mrc'
    with open(database, 'rb') as data:
        # Nacteni marcu
        reader = MARCReader(data)
        for record in reader: 
            periodika = get_periodika(record, periodika)
    df_periodika = pd.DataFrame(periodika)
    #df_periodika.to_excel(f'data/periodika_{d}.xlsx')
    freq = {'title': [df_periodika[df_periodika.issn == x].title.iloc[0]
        if not df_periodika[df_periodika.issn == x].empty else None
        for x in df_periodika[~df_periodika.issn.isna()].issn.unique()], 

        'issn': list(df_periodika[~df_periodika.issn.isna()].issn.unique()), 

        'frekvence': [len(df_periodika[df_periodika['issn'] == x]) 
                      for x in df_periodika[~df_periodika.issn.isna()].issn.unique()]}

    freq2 = {'title': list(df_periodika[df_periodika.issn.isna()].title.unique()), 
             
            'issn': [ None
        for _ in df_periodika[df_periodika.issn.isna()].title.unique()], 

        'frekvence': [len(df_periodika[(df_periodika.issn.isna()) & (df_periodika['title'] == x)]) 
                      for x in df_periodika[df_periodika.issn.isna()].title.unique()]}
    
    freq['title'].extend(freq2['title'])
    freq['issn'].extend(freq2['issn'])
    freq['frekvence'].extend(freq2['frekvence'])
    df_freq = pd.DataFrame.from_dict(freq)
    df_freq.to_excel(f'data/freq_{d}.xlsx')

def do_it(record):
    uuid_text = '/uuid:'
    global periodika
    leader = record.leader
    links = [f.subfields_as_dict()['u'][0] if 'u' in f.subfields_as_dict() else None for f in record.get_fields('911')]
    links_856 = [f.subfields_as_dict()['u'][0] if 'u' in f.subfields_as_dict() else None for f in record.get_fields('856')]
    links.extend(links_856)
    if 's' in leader[7] and len(links)> 0 and  any(uuid_text in str(l) for l in links):
        try:
            print(record)
            l_001 = record['001'].data
            title = [f.subfields_as_dict()['a'][0].strip(' :/') if 'a' in f.subfields_as_dict() else None for f in record.get_fields('245')][0]
            issn = record.issn
            for url in links: 
                match = re.match(r'(https?://[^/]+)\.cz/.*/(uuid:.*)', url)
                if match: # There may be links without uuid
                    domain = match.group(1) + '.cz'  # https://www.ndk.cz
                    uuid = match.group(2)            # uuid:57c8a997-2793-46b1-bfd6-794d0bface74
                    periodika['001'].append(l_001)
                    periodika['title'].append(title)
                    periodika['issn'].append(issn)
                    periodika['link'].append(url)
                    periodika['domain'].append(domain)
                    periodika['uuid'].append(uuid)
                    print(f'{url}, domain: {domain}, uuid: {uuid}')
        except: print('No 001')   

def do_it_3(record):
    global periodika_nk
    leader = record.leader
    if 's' in leader[7] :
        title = [f.subfields_as_dict()['a'][0].strip(' :/') if 'a' in f.subfields_as_dict() else None for f in record.get_fields('245')][0]
        issn = record.issn
        try:
            l_001 = record['001'].data
            periodika_nk['001'].append(l_001)
            periodika_nk['title'].append(title)
            periodika_nk['issn'].append(issn)
            print(f'Title: {title}, ISSN: {issn}')
        except: 
            print('No 001')    
                   

def main_2():
    global periodika
    map_xml(do_it, 'data/skc.xml')  
    df_periodika = pd.DataFrame(periodika)
    df_periodika.to_excel(f'data/periodika_nk2.xlsx')

def main_3():
    global periodika_nk
    map_xml(do_it_3, 'data/skc.xml')  
    df_periodika_nk = pd.DataFrame(periodika_nk)
    df_periodika_nk.to_excel(f'data/periodika_nk_all.xlsx')


if __name__ == "__main__":
    main()

