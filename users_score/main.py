from tqdm import tqdm
from mpi4py import MPI

import sekitoba_library as lib
import sekitoba_data_manage as dm
from analyze import UsersAnalyze
from common.name import Name

data_name = Name()

dm.dl.file_set( "users_data.pickle" )

def key_list_search( rank, size, key_list ):
    n = int( len( key_list ) / ( size - 1 ) )
    s1 = int( ( rank - 1 ) * n )

    if not rank + 1 == size:
        s2 = s1 + n
    else:
        s2 = len( key_list ) + 1

    return key_list[s1:s2]

def data_connect( base, add_data ):
    for year in add_data.keys():
        lib.dic_append( base, year, {} )
        for score in add_data[year].keys():
            lib.dic_append( base[year], score, { "recovery": 0, "count": 0 } )
            base[year][score]["count"] += add_data[year][score]["count"]
            base[year][score]["recovery"] += add_data[year][score]["recovery"]

def recovery_check( data ):
    result = {}
    result["all"] = {}
    score_key = {}
    
    for year in data.keys():
        result[year] = {}
        current_data = sorted( data[year], key = lambda x:x["score"], reverse = True )

        if len( current_data ) == 0:
            continue

        current_score = current_data[0]["score"]            
            
        for i in range( 0, len( current_data ) ):
            score = current_data[i]["score"]
            key_score = str( int( score ) )
            lib.dic_append( result["all"], key_score, { "recovery": 0, "count": 0 } )
            lib.dic_append( result[year], key_score, { "recovery": 0, "count": 0 } )
            
            score_key[key_score] = score
            result[year][key_score]["count"] += 1
            result[year][key_score]["recovery"] += current_data[i]["odds"]
            result["all"][key_score]["recovery"] += current_data[i]["odds"]
            result["all"][key_score]["count"] += 1                    

    for k in result.keys():
        for key_score in result[k].keys():
            result[k][key_score]["recovery"] /= result[k][key_score]["count"]
            result[k][key_score]["recovery"] = round( result[k][key_score]["recovery"], 2 )

    return result, score_key

def write( recovery_data, score_key, test = False ):
    first = True
    write_score = "year/score\t"
    key_list = []
        
    for sk in score_key.keys():
        key_list.append( int( sk ) )

    key_list = sorted( key_list )

    if test:
        file_name = "/Volumes/Gilgamesh/sekitoba-recovery/test_users_score_one.csv"
    else:
        file_name = "/Volumes/Gilgamesh/sekitoba-recovery/users_score_one.csv"
            
    f = open( file_name, "w" )
        
    for year in recovery_data.keys():
        write_recovery = year + "\t"
        write_count = year + "\t"

        for key in key_list:
            score = str( key )
                
            if first:
                write_score += score + "\t"

            try:
                write_recovery += str( recovery_data[year][score]["recovery"] ) + "\t"
                write_count += str( recovery_data[year][score]["count"] ) + "\t"
            except:
                write_recovery += "0\t"
                write_count += "0\t"

        if first:
            #print( write_score )
            write_score += "\n"
            f.write( write_score )

        #print( write_recovery )
        #print( write_count + "\n" )
        write_recovery += "\n"
        write_count += "\n\n"
        f.write( write_recovery )
        f.write( write_count )            
        first = False
        
    f.close()            

def main():
    ua = UsersAnalyze()
    buy_result = ua.users_analyze()
    recovery_data, score_key = recovery_check( buy_result )
    write( recovery_data, score_key )

    buy_result = ua.users_analyze( test = True )
    recovery_data, score_key = recovery_check( buy_result )
    write( recovery_data, score_key, test = True )

    dm.pickle_upload( "users_score_data.pickle", ua.users_score_data )
    
    
if __name__ == "__main__":
    main()
