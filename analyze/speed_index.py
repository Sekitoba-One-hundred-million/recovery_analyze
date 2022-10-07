import os
import numpy as np
from tqdm import tqdm

import sekitoba_library as lib
import sekitoba_data_manage as dm
from sekitoba_data_create.time_index_get import TimeIndexGet

dm.dl.file_set( "race_data.pickle" )
dm.dl.file_set( "odds_data.pickle" )
dm.dl.file_set( "race_info_data.pickle" )
dm.dl.file_set( "horce_data_storage.pickle" )
dm.dl.file_set( "baba_index_data.pickle" )

name = "speed_index"
ONE = "one"
THREE = "three"
DATA = "recovery"
COUNT = "count"
    
def main():
    result = { ONE: {}, THREE: {} }
    data_storage = []
    race_data = dm.dl.data_get( "race_data.pickle" )
    odds_data = dm.dl.data_get( "odds_data.pickle" )
    race_info = dm.dl.data_get( "race_info_data.pickle" )
    horce_data = dm.dl.data_get( "horce_data_storage.pickle" )
    baba_index_data = dm.dl.data_get( "baba_index_data.pickle" )
    time_index = TimeIndexGet()
    
    for k in tqdm( race_data.keys() ):
        race_id = lib.id_get( k )
        year = race_id[0:4]
        race_place_num = race_id[4:6]
        day = race_id[9]
        num = race_id[7]

        key_place = str( race_info[race_id]["place"] )
        key_dist = str( race_info[race_id]["dist"] )
        key_kind = str( race_info[race_id]["kind"] )        
        key_baba = str( race_info[race_id]["baba"] )

        #if year in lib.test_years:
        #    continue

        #芝かダートのみ
        if key_kind == "0" or key_kind == "3":
            continue

        try:
            three_odds = odds_data[race_id]["複勝"]
        except:
            continue

        count = 0
        speed_index_list = []
        
        for kk in race_data[k].keys():
            horce_id = kk
            current_data, past_data = lib.race_check( horce_data[horce_id],
                                                     year, day, num, race_place_num )#今回と過去のデータに分ける
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )

            if not cd.race_check():
                continue

            current_time_index = time_index.main( horce_id, pd.past_day_list() )
            speed, up_speed, pace_speed = pd.speed_index( baba_index_data[horce_id] )
            speed_index_list.append( lib.max_check( speed ) + current_time_index["max"] )

        sort_speed_index = sorted( speed_index_list, reverse = True )
        
        for kk in race_data[k].keys():
            horce_id = kk
            current_data, past_data = lib.race_check( horce_data[horce_id],
                                                     year, day, num, race_place_num )#今回と過去のデータに分ける
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )

            if not cd.race_check():
                continue

            score = sort_speed_index.index( speed_index_list[count] )
            key = str( int( score ) )
            rank = cd.rank()
            lib.dic_append( result[ONE], year, {} )
            lib.dic_append( result[ONE][year], key, { DATA: 0, COUNT: 0 } )
            lib.dic_append( result[THREE], year, {} )
            lib.dic_append( result[THREE][year], key, { DATA: 0, COUNT: 0 } )
            
            result[ONE][year][key][COUNT] += 1
            result[THREE][year][key][COUNT] += 1

            if rank == 1:
                result[ONE][year][key][DATA] += cd.odds()

            if rank <= len( three_odds ):
                result[THREE][year][key][DATA] += three_odds[int(rank-1)] / 100

    for year in result[ONE].keys():
        for k in result[ONE][year].keys():
            result[ONE][year][k][DATA] /= result[ONE][year][k][COUNT]
            result[ONE][year][k][DATA] = round( result[ONE][year][k][DATA], 2 )
            result[THREE][year][k][DATA] /= result[THREE][year][k][COUNT]
            result[THREE][year][k][DATA] = round( result[THREE][year][k][DATA], 2 )

    lib.write_recovery_csv( result[ONE], name + ".csv" )
    lib.write_recovery_csv( result[THREE], THREE + "_" + name + ".csv" )
 

if __name__ == "__main__":
    main()
        
