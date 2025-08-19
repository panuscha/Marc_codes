from pymarc import map_xml, MARCWriter, MARCReader

file_path = 'data/ucla.mrc'
file_path_ret = 'data/ucla test/retrobi.mrc'

out_alkaro = 'data/ucla test/ucla_alkaro.mrc'
out_ret = 'data/ucla test/ucla_ret.mrc'
out_smz = 'data/ucla test/ucla_smz.mrc'
out_int = 'data/ucla test/ucla_int.mrc'
out_cle_I = 'data/ucla test/ucla_cle_I.mrc'
out_cle_II = 'data/ucla test/ucla_cle_II.mrc'
out_soucasna = 'data/ucla test/ucla_soucasna.mrc'
out_all = 'data/ucla test/ucla_all.mrc'
out_trl = 'data/ucla test/ucla_trl.mrc'
out_mbk = 'data/ucla test/ucla_mbk.mrc' # Bohemisticke konsorcium

database_alkaro = 'ALKARO'
database_ret = 'RET'
database_smz = 'SMZ'
database_int = 'INT'    
database_cle = ['CLE']
database_cle_I = ['CLE1']
database_cle_II = ['CLE2']
database_trl = 'TRL'
database_mbk = 'MBK'
database_soucasna = ['B12', 'B45', 'B70', 'B80', 'B97', 'INT', 'SMZ', 'CLE1', 'CLE2', 'MBK'] # CLE1 and CLE2 was added later
database_all = ['B12', 'B45', 'B70', 'B80', 'B97', 'ALKARO','RET','INT', 'SMZ', 'CLE1', 'CLE2', 'MBK'] # CLE1 and CLE2 was added later

writer_alkaro =  MARCWriter(open(out_alkaro, 'wb'))
writer_ret =  MARCWriter(open(out_ret, 'wb'))
writer_smz =  MARCWriter(open(out_smz, 'wb'))
writer_int =  MARCWriter(open(out_int, 'wb'))
writer_cle_I =  MARCWriter(open(out_cle_I, 'wb'))
writer_cle_II =  MARCWriter(open(out_cle_II, 'wb'))
writer_mbk =  MARCWriter(open(out_mbk, 'wb'))
writer_soucasna = MARCWriter(open(out_soucasna, 'wb'))
writer_all = MARCWriter(open(out_all, 'wb'))

alkaro_count = 0
mbk_count = 0

def save_databases(r):

    not_found_soucasna = True
    not_found_all = True
    not_found_mbk = True
    # r.remove_fields('LDR')
    # for field in  r.get_fields('FMT'):
    #     r.remove_fields('FMT')
    for field in r.get_fields('964'):
        subfields = field.get_subfields('a')
        if subfields:
            if field['a'] in database_alkaro:
                try:
                    writer_alkaro.write(r)    
                except Exception as error:
                    print("Exception: " + type(error).__name__)          
                    
            if field['a'] in database_ret:
                try:
                    writer_ret.write(r)   
                except Exception as error:
                    print("Exception: " + type(error).__name__) 
                        
            if field['a'] in database_smz:
                try:
                    writer_smz.write(r)   
                except Exception as error:
                    print("Exception: " + type(error).__name__) 

            if  database_mbk in field['a']:
                try:
                    writer_mbk.write(r)  
                    print(r)
                    mbk_count += 1 
                except Exception as error:
                    print("Exception: " + type(error).__name__)         
                    
            if field['a'] in database_int:
                try:
                    writer_int.write(r)   
                except Exception as error:
                    print("Exception: " + type(error).__name__)   
                

            if field['a'] in database_cle_I:
                try:
                    writer_cle_I.write(r)

                except Exception as error:
                    print("Exception: " + type(error).__name__)    

            if field['a'] in database_cle_II:
                try:
                    writer_cle_II.write(r) 
                except Exception as error:
                    print("Exception: " + type(error).__name__) 

            if field['a'] in database_cle:
                        try:
                            
                            for cle in r.get_fields('001'): 
                                #match = re.search(pattern, str(cle.value()))
                                match = str(cle.value())
                                if match[0] == '1' or (len(match)> 2 and  match[0:3] == '001'):   
                                        writer_cle_I.write(r)  
                                        if not_found_soucasna:
                                            writer_soucasna.write(r)
                                            not_found_soucasna = False
                                        if not_found_all:
                                            writer_all.write(r)  
                                            not_found_all = False 
                                if match[0] == '2' or (len(match)> 2 and  match[0:3] == '002'):   
                                        writer_cle_II.write(r)
                                        if not_found_soucasna:
                                            writer_soucasna.write(r)
                                            not_found_soucasna = False
                                        if not_found_all:
                                            writer_all.write(r)  
                                            not_found_all = False 
                        except Exception as error:
                            print(r)
                            print("Exception: " + type(error).__name__)    

            if field['a'] in database_soucasna and not_found_soucasna:
                try:
                    writer_soucasna.write(r)  
                    not_found_soucasna = False
                except Exception as error:
                    print("Exception: " + type(error).__name__) 

            if field['a'] in database_all and not_found_all:
                try:
                    writer_all.write(r)  
                    not_found_all = False
                except Exception as error:
                    print("Exception: " + type(error).__name__) 
                                                                

                    
        
try:  
    #map_xml(save_databases, file_path)

    with open(file_path, 'rb') as data:
        # Nacteni marcu
        reader = MARCReader(data)
        counter = 0
        for record in reader:
            counter += 1
            try:
                save_databases(record)
            except:
                print('Something wrong with record')
                print(record)
    print("Count: " + str(counter))
    print(f'ALKARO in SIF: {alkaro_count}')

    print('Adding Retrobi.')
    with open(file_path_ret, 'rb') as data:
        # Nacteni marcu
        reader = MARCReader(data)
        for record in reader:
            counter += 1
            try:
                writer_ret.write(record)
                writer_all.write(record)
            except:
                print('Something wrong with record')
                print(record)
    print("Count: " + str(counter))

    print('Adding TRL.')
    with open(out_trl, 'rb') as data:
        # Nacteni marcu
        reader = MARCReader(data)
        for record in reader:
            counter += 1
            try:
                writer_all.write(record)
            except:
                print('Something wrong with record')
                print(record)
    print("Count: " + str(counter))
    
except Exception as error:
     print("Whole Error: " + type(error).__name__)      
finally:
    writer_alkaro.close()
    writer_cle_I.close()
    writer_cle_II.close()
    writer_int.close()
    writer_ret.close()
    writer_smz.close()
    writer_soucasna.close()
    writer_all.close()
    writer_mbk.close()

