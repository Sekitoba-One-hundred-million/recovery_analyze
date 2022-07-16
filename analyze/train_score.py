import os
import numpy as np
from tqdm import tqdm

import sekitoba_library as lib
import sekitoba_data_manage as dm
#from sekitoba_data_create.train_index_get import TrainIndexGet

dm.dl.file_set( "race_data.pickle" )
dm.dl.file_set( "race_info_data.pickle" )
dm.dl.file_set( "horce_data_storage.pickle" )
dm.dl.file_set( "baba_index_data.pickle" )

name = "train_score"

dm.dl.file_set( "train_time_data.pickle" )
dm.dl.file_set( "train_ave_data.pickle" )
dm.dl.file_set( "train_ave_key_data.pickle" )

class TrainIndexGet:
    def __init__( self ):
        self.train_time_data = dm.dl.data_get( "train_time_data.pickle" )
        self.train_ave_data = dm.dl.data_get( "train_ave_data.pickle" )
        self.train_ave_key_data = dm.dl.data_get( "train_ave_key_data.pickle" )
        self.base_time = self.train_ave_data["美"]["坂"]["馬也"]["time"]
        self.base_wrap = self.train_ave_data["美"]["坂"]["馬也"]["wrap"]

    def main( self, race_id, key_horce_num ):
        result = 100

        try:
            load = self.train_time_data[race_id][key_horce_num]["load"]
            cource = self.train_time_data[race_id][key_horce_num]["cource"] 
            t_time = self.train_time_data[race_id][key_horce_num]["time"]
            wrap = self.train_time_data[race_id][key_horce_num]["wrap"]
        except:
            return result

        if len( t_time ) == 0 or len( wrap ) == 0:
            return result

        if not len( cource ) == 2:
            return result
        
        place_key = ""
        cource_key = ""
        load_key = ""

        for key in self.train_ave_key_data["place"]:
            if cource[0] in key:
                place_key = key
                break
            
        for key in self.train_ave_key_data["cource"]:
            if cource[1] in key:
                cource_key = key
                break

        for key in self.train_ave_key_data["load"]:
            if load in key:
                load_key = key
                break

        if len( place_key ) == 0 or len( cource_key ) == 0 or len( load_key ) == 0:
            return result

        ave_time = self.train_ave_data[place_key][cource_key][load_key]["time"]
        ave_wrap = self.train_ave_data[place_key][cource_key][load_key]["wrap"]
        time_score = ( self.base_time / ave_time )
        wrap_score = ( self.base_wrap / ave_wrap )
        result = wrap_score + time_score

        return result

def main():
    result = {}
    race_data = dm.dl.data_get( "race_data.pickle" )
    race_info = dm.dl.data_get( "race_info_data.pickle" )
    horce_data = dm.dl.data_get( "horce_data_storage.pickle" )
    baba_index_data = dm.dl.data_get( "baba_index_data.pickle" )
    train_index = TrainIndexGet()
    
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

        score_list = []
        count = 0
        
        for kk in race_data[k].keys():
            horce_id = kk
            current_data, past_data = lib.race_check( horce_data[horce_id],
                                                     year, day, num, race_place_num )#今回と過去のデータに分ける
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )

            if not cd.race_check():
                continue

            key_horce_num = str( int( cd.horce_number() ) )
            current_train_score = train_index.main( race_id, key_horce_num )

            if current_train_score == 100:
                continue
            
            score_list.append( current_train_score )            

        for kk in race_data[k].keys():
            horce_id = kk
            current_data, past_data = lib.race_check( horce_data[horce_id],
                                                     year, day, num, race_place_num )#今回と過去のデータに分ける
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )

            if not cd.race_check():
                continue

            key_horce_num = str( int( cd.horce_number() ) )
            current_train_score = train_index.main( race_id, key_horce_num )

            if current_train_score == 100:
                continue
            
            score = score_list.index( current_train_score )
            key = str( int( score ) )
            lib.dic_append( result, year, {} )
            lib.dic_append( result[year], key, { "recovery": 0, "count": 0 } )
            
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
        
