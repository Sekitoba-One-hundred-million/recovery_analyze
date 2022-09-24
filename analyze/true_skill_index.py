import os
import numpy as np
from tqdm import tqdm

import sekitoba_library as lib
import sekitoba_data_manage as dm

dm.dl.file_set( "race_data.pickle" )
dm.dl.file_set( "race_info_data.pickle" )
dm.dl.file_set( "horce_data_storage.pickle" )
dm.dl.file_set( "true_skill_data.pickle" )

name = "true_skill_index"
DATA = "recovery"
COUNT = "count"
    
def main():
    result = {}
    data_storage = []
    race_data = dm.dl.data_get( "race_data.pickle" )
    race_info = dm.dl.data_get( "race_info_data.pickle" )
    horce_data = dm.dl.data_get( "horce_data_storage.pickle" )
    true_skill_data = dm.dl.data_get( "true_skill_data.pickle" )
    
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


        true_skill_list = []

        for kk in race_data[k].keys():
            horce_id = kk
            current_data, past_data = lib.race_check( horce_data[horce_id],
                                                     year, day, num, race_place_num )#今回と過去のデータに分ける
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )

            if not cd.race_check():
                continue

            try:
                true_skill_list.append( true_skill_data[race_id][horce_id] )
            except:
                continue

        true_skill_list = sorted( true_skill_list, reverse = True )
        
        for kk in race_data[k].keys():
            horce_id = kk
            current_data, past_data = lib.race_check( horce_data[horce_id],
                                                     year, day, num, race_place_num )#今回と過去のデータに分ける
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )

            if not cd.race_check():
                continue

            try:
                true_skill_score = true_skill_data[race_id][horce_id]
                score = true_skill_list.index( true_skill_score )
            except:
                score = -1

            key = str( int( score ) )
            lib.dic_append( result, year, {} )
            lib.dic_append( result[year], key, { DATA: 0, COUNT: 0 } )
            
            result[year][key][COUNT] += 1

            if cd.rank() == 1:
                result[year][key][DATA] += cd.odds()

    for year in result.keys():
        for k in result[year].keys():
            result[year][k][DATA] /= result[year][k][COUNT]
            result[year][k][DATA] = round( result[year][k][DATA], 2 )

    lib.write_recovery_csv( result, name + ".csv" )
 

if __name__ == "__main__":
    main()
        
