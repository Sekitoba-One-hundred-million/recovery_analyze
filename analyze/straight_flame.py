import os
import numpy as np
from tqdm import tqdm

import sekitoba_library as lib
import sekitoba_data_manage as dm

dm.dl.file_set( "race_data.pickle" )
dm.dl.file_set( "race_info_data.pickle" )
dm.dl.file_set( "horce_data_storage.pickle" )
dm.dl.file_set( "baba_index_data.pickle" )
dm.dl.file_set( "race_cource_info.pickle" )

name = "straight_flame"

def main():
    result = {}
    race_data = dm.dl.data_get( "race_data.pickle" )
    race_info = dm.dl.data_get( "race_info_data.pickle" )
    race_cource_info = dm.dl.data_get( "race_cource_info.pickle" )
    horce_data = dm.dl.data_get( "horce_data_storage.pickle" )
    
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

        if "out_side" in race_info[race_id] and race_info[race_id]["out_side"]:
            key_dist += "外"

        try:
            straight_dist = int( race_cource_info[key_place][key_kind][key_dist]["dist"][0] / 100 )
        except:
            continue
        
        for kk in race_data[k].keys():
            horce_id = kk
            current_data, past_data = lib.race_check( horce_data[horce_id],
                                                     year, day, num, race_place_num )#今回と過去のデータに分ける
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )

            if not cd.race_check():
                continue

            before_cd = pd.before_cd()

            if before_cd == None:
                continue

            score = 0

            if cd.horce_number() < cd.all_horce_num() / 3:
                score = 100 + straight_dist
            elif ( cd.all_horce_num() / 3 ) * 2 <= cd.horce_number():
                score = 200 + straight_dist
                
            key_score = str( int( score ) )
            lib.dic_append( result, year, {} )
            lib.dic_append( result[year], key_score, { "recovery": 0, "count": 0 } )

            result[year][key_score]["count"] += 1

            if cd.rank() == 1:
                result[year][key_score]["recovery"] += cd.odds()


    for year in result.keys():
        for k in result[year].keys():
            result[year][k]["recovery"] /= result[year][k]["count"]
            result[year][k]["recovery"] = round( result[year][k]["recovery"], 2 )

    lib.write_recovery_csv( result, name + ".csv" )
    lib.recovery_best_select( result )

if __name__ == "__main__":
    main()
        
