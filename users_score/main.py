from tqdm import tqdm
import numpy as np

import sekitoba_library as lib
import sekitoba_data_manage as dm
from sekitoba_data_create.time_index_get import TimeIndexGet
from sekitoba_data_create.up_score import UpScore
from sekitoba_data_create.train_index_get import TrainIndexGet
from sekitoba_data_create.pace_time_score import PaceTimeScore
from sekitoba_data_create.jockey_data_get import JockeyData
from sekitoba_data_create import parent_data_get

from common.name import Name
from users_score import UsersScore

data_name = Name()

dm.dl.file_set( "race_data.pickle" )
dm.dl.file_set( "race_info_data.pickle" )
dm.dl.file_set( "horce_data_storage.pickle" )
dm.dl.file_set( "baba_index_data.pickle" )
dm.dl.file_set( "parent_id_data.pickle" )

def main( test_check = False ):
    result = {}
    key_dict = {}
    race_data = dm.dl.data_get( "race_data.pickle" )
    race_info = dm.dl.data_get( "race_info_data.pickle" )
    horce_data = dm.dl.data_get( "horce_data_storage.pickle" )
    baba_index_data = dm.dl.data_get( "baba_index_data.pickle" )
    parent_id_data = dm.dl.data_get( "parent_id_data.pickle" )
    
    us = UsersScore()
    time_index = TimeIndexGet()
    up_score_get = UpScore()
    train_index = TrainIndexGet()
    pace_time_score = PaceTimeScore()
    jockey_data = JockeyData()
    
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

        if year in lib.test_years and not test_check:
            continue
        elif not year in lib.test_years and test_check:
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

            past_rank_list = pd.rank_list()
            speed, up_speed, pace_speed = pd.speed_index( baba_index_data[horce_id] )

            if len( past_rank_list ) == 0:
                continue

            key_horce_num = str( int( cd.horce_number() ) )
            father_id = parent_id_data[horce_id]["father"]
            mother_id = parent_id_data[horce_id]["mother"]
            father_data = parent_data_get.main( horce_data, father_id, baba_index_data )
            mother_data = parent_data_get.main( horce_data, mother_id, baba_index_data )            
            current_jockey = jockey_data.data_get( horce_id, cd.birthday(), cd.race_num() )
            
            us.set_data( data_name.before_rank, past_rank_list[0] )
            us.set_data( data_name.popular, cd.popular() )
            us.set_data( data_name.limb, lib.limb_search( pd ) )
            us.set_data( data_name.time_index, max( time_index.main( horce_id, pd.past_day_list() )["max"], 0 ) )
            us.set_data( data_name.speed_index, lib.max_check( speed ) )
            us.set_data( data_name.up_score, up_score_get.score_get( pd ) )
            us.set_data( data_name.id_weight, cd.id_weight() )
            us.set_data( data_name.train_score, train_index.main( race_id, key_horce_num )["score"] )
            us.set_data( data_name.pace_time_score, pace_time_score.score_get( pd ) )
            us.set_data( data_name.up_speed, lib.max_check( up_speed ) )
            us.set_data( data_name.pace_speed, lib.max_check( pace_speed ) )
            us.set_data( data_name.money, pd.get_money() )
            us.set_data( data_name.one_rate, pd.one_rate() )
            us.set_data( data_name.two_rate, pd.two_rate() )
            us.set_data( data_name.three_rate, pd.three_rate() )
            us.set_data( data_name.best_weight, pd.best_weight() )
            us.set_data( data_name.race_interval, pd.race_interval() )
            us.set_data( data_name.three_average, pd.three_average() )
            us.set_data( data_name.before_diff, pd.diff_get() )
            us.set_data( data_name.jockey_rank, current_jockey["all"]["rank"] )
            us.set_data( data_name.jockey_one_rate, current_jockey["all"]["one"] )
            us.set_data( data_name.jockey_two_rate, current_jockey["all"]["two"] )
            us.set_data( data_name.jockey_three_rate, current_jockey["all"]["three"] )
            us.set_data( data_name.baba, cd.baba_status() )
            us.set_data( data_name.horce_number, cd.horce_number() )
            us.set_data( data_name.age, cd.year() - int( horce_id[0:4] ) )
            us.set_data( data_name.father_rank, father_data["rank"] )
            us.set_data( data_name.mother_rank, mother_data["rank"] )
            
            score = us.get_score()
            key_score = str( int( score ) )
            key_dict[key_score] = True
            lib.dic_append( result, year, {} )
            lib.dic_append( result[year], key_score, { "recovery": 0, "count": 0 } )

            result[year][key_score]["count"] += 1

            if cd.rank() == 1:
                result[year][key_score]["recovery"] += cd.odds()

    key_list = list( key_dict.keys() )
    
    for i in range( 0, len( key_list ) ):
        key_list[i] = int( key_list[i] )

    key_list = sorted( key_list, reverse = True )
    
    for year in result.keys():
        r = 0
        c = 0
        
        for k in key_list:
            k = str( k )
            try:
                r += result[year][k]["recovery"]
                c += result[year][k]["count"]
                result[year][k]["recovery"] = r / c
                result[year][k]["recovery"] = round( result[year][k]["recovery"], 2 )
                result[year][k]["count"] = c
            except:
                result[year][k] = {}
                result[year][k]["recovery"] = 0
                result[year][k]["count"] = 0

    if not test_check:
        file_name = "users_score.csv"
    elif test_check:
        file_name = "users_score_test.csv"
        
    lib.write_recovery_csv( result, file_name )            

if __name__ == "__main__":
    main( test_check = False )
    main( test_check = True )
