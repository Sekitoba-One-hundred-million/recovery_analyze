import os
import numpy as np
from tqdm import tqdm

import sekitoba_library as lib
import sekitoba_data_manage as dm
from sekitoba_data_create import parent_data_get

dm.dl.file_set( "race_data.pickle" )
dm.dl.file_set( "race_info_data.pickle" )
dm.dl.file_set( "horce_data_storage.pickle" )
dm.dl.file_set( "baba_index_data.pickle" )
dm.dl.file_set( "parent_id_data.pickle" )

name = "father_rank"

def main():
    result = {}
    data_storage = []
    race_data = dm.dl.data_get( "race_data.pickle" )
    race_info = dm.dl.data_get( "race_info_data.pickle" )
    horce_data = dm.dl.data_get( "horce_data_storage.pickle" )
    baba_index_data = dm.dl.data_get( "baba_index_data.pickle" )
    parent_id_data = dm.dl.data_get( "parent_id_data.pickle" )
    
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

        for kk in race_data[k].keys():
            horce_id = kk
            current_data, past_data = lib.race_check( horce_data[horce_id],
                                                     year, day, num, race_place_num )#今回と過去のデータに分ける
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )

            if not cd.race_check():
                continue

            father_id = parent_id_data[horce_id]["father"]
            mother_id = parent_id_data[horce_id]["mother"]
            
            try:
                father_data = horce_data[father_id]
            except:
                continue
            
            father_pd = lib.past_data( father_data, [] )
            count = 0
            score = 0
            
            for father_cd in father_pd.past_cd_list():
                c = 0
                
                if father_cd.place() == cd.place():
                    c += 1

                if father_cd.baba_status() == cd.baba_status():
                    c += 1

                if lib.dist_check( father_cd.dist() * 1000 ) == lib.dist_check( cd.dist() * 1000 ):
                    c += 1

                count += c
                score += father_cd.rank() * c

            if not count == 0:
                score /= count
                
            score = int( score )
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
    lib.write_recovery_csv( result, name + ".csv" )
            
if __name__ == "__main__":
    main()
        
