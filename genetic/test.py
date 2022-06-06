from tqdm import tqdm

import sekitoba_library as lib
import sekitoba_data_manage as dm
from simulation import Simulation

def data_create( learn_data, rate_data ):
    result = {}
    si = Simulation()
    buy_key = [ "one", "quinella", "wide" ]
    
    for ticket_kind in buy_key:
        print( ticket_kind )
        analyze_data = si.simulation( learn_data, rate_data[ticket_kind], ticket_kind )
        current_score = analyze_data[0]["score"]
        count = 0
        recovery = 0
        max_count = 0
        result[ticket_kind] = []
        
        for data in analyze_data:
            count += 1
            
            if data["score"] == current_score:
                recovery += data["odds"]
            else:
                r = recovery / count
                
                if 1.0 < r:
                    result[ticket_kind].append( { "score": current_score, "recovery": r, "count": count } )
                    
                recovery += data["odds"]
                current_score = data["score"]

    for k in result.keys():
        result[k].reverse()
        
    return result

def csv_write( file_name, data ):
    f = open( file_name, "w" )
    write_key = [ "score", "recovery", "count" ]
    write_str = ""
    
    for k in write_key:
        write_str += k + "\t"        
        
    f.write( write_str + "\n" )

    for i in range( 0, len( data ) ):
        write_str = ""
        
        for k in write_key:
            write_str += str( data[i][k] ) + "\t"

        f.write( write_str + "\n" )            

    f.close()

def main():
    users_score_rate = dm.pickle_load( "users_score_rate.pickle" )
    test_data = dm.pickle_load( "genetic_test_data.pickle" )
    
    test_result = data_create( test_data, users_score_rate )
    dir_name = "/Users/kansei/Desktop/recovery_data/"

    for k in test_result.keys():
        csv_write( dir_name + "genetic_test_" + k + "_users_score.csv", test_result[k] )
    #csv_write( "/Users/kansei/Desktop/recovery_data/genetic_test_users_score.csv", test_result )
    
    #result = data_create( key_list )
    #csv_write( "/Users/kansei/Desktop/recovery_data/genetic_users_score.csv", result )
