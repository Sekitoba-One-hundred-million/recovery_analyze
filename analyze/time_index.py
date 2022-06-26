import os
import numpy as np
from tqdm import tqdm

import sekitoba_library as lib
import sekitoba_data_manage as dm
from sekitoba_data_create.time_index_get import TimeIndexGet

dm.dl.file_set( "race_data.pickle" )
dm.dl.file_set( "race_info_data.pickle" )
dm.dl.file_set( "horce_data_storage.pickle" )

name = "time_index"

def main():
    result = {}
    race_data = dm.dl.data_get( "race_data.pickle" )
    race_info = dm.dl.data_get( "race_info_data.pickle" )
    horce_data = dm.dl.data_get( "horce_data_storage.pickle" )
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

        if year in lib.test_years:
            continue

        #芝かダートのみ
        if key_kind == "0" or key_kind == "3":
            continue

        time_index_list = []
        count = 0
        
        for kk in race_data[k].keys():
            horce_id = kk
            current_data, past_data = lib.race_check( horce_data[horce_id],
                                                     year, day, num, race_place_num )#今回と過去のデータに分ける
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )

            if not cd.race_check():
                continue

            current_time_index = time_index.main( kk, pd.past_day_list() )
            time_index_list.append( current_time_index["max"] )

        for kk in race_data[k].keys():
            horce_id = kk
            current_data, past_data = lib.race_check( horce_data[horce_id],
                                                     year, day, num, race_place_num )#今回と過去のデータに分ける
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )

            if not cd.race_check():
                continue

            score = time_index_list.index( time_index_list[count] )
            key = str( int( score ) )
            lib.dic_append( result, year, {} )
            lib.dic_append( result[year], key, { "recovery": 0, "count": 0 } )

            count += 1
            result[year][key]["count"] += 1

            if cd.rank() == 1:
                result[year][key]["recovery"] += cd.odds()

    for year in result.keys():
        for k in result[year].keys():
            result[year][k]["recovery"] /= result[year][k]["count"]
            result[year][k]["recovery"] = round( result[year][k]["recovery"], 2 )

    score = lib.recovery_score_check( result )
    lib.write_recovery_csv( result,  name + ".csv" )

if __name__ == "__main__":
    main()
        
