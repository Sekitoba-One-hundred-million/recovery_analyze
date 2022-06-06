from tqdm import tqdm
import numpy as np

import sekitoba_library as lib
import sekitoba_data_manage as dm

from once_data import OnceData

dm.dl.file_set( "race_data.pickle" )

def use_key_list( key_list ):
    result = []
    
    for k in key_list:
        race_id = lib.id_get( k )
        year = race_id[0:4]

        if year in lib.test_years:
            result.append( k )

    return result

def main():
    race_data = dm.dl.data_get( "race_data.pickle" )
    od = OnceData()
    bet_rate = 0.08
    money = 1000
    score_line = 2170
    recovery = 0
    win_count = 0
    count = 0
    key_list = use_key_list( list( race_data.keys() ) )

    for k in tqdm( key_list ):
        race_id = lib.id_get( k )
        year = race_id[0:4]
        
        if not year in lib.test_years:
            continue

        data = od.create( k )

        for i in range( 0, len( data ) ):
            rank = data[i]["rank"]
            odds = data[i]["odds"]
            score = data[i]["score"]
            
            if score < score_line:
                continue

            count += 1

            if rank == 1:
                recovery += odds
                win_count += 1

    recovery /= count
    win_count /= count
    print( "recovery:{}".format( round( recovery, 3 ) ) )
    print( "win:{}".format( round( win_count, 3 ) ) )
    print( "count:{}".format( count ) )
    print( "money:{}".format( money ) )

if __name__ == "__main__":
    main()
