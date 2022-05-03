from tqdm import tqdm
import numpy as np

import sekitoba_library as lib
import sekitoba_data_manage as dm

from sekitoba_data_create.time_index_get import TimeIndexGet
from sekitoba_data_create.up_score import UpScore
from sekitoba_data_create.train_index_get import TrainIndexGet
from sekitoba_data_create.pace_time_score import PaceTimeScore
from sekitoba_data_create.jockey_data_get import JockeyData

from data_set import DataSet
from common.name import Name

data_name = Name()

dm.dl.file_set( "race_data.pickle" )
dm.dl.file_set( "race_info_data.pickle" )
dm.dl.file_set( "horce_data_storage.pickle" )
dm.dl.file_set( "baba_index_data.pickle" )
dm.dl.file_set( "parent_id_data.pickle" )

def main():
    result = {}
    key_dict = {}
    race_data = dm.dl.data_get( "race_data.pickle" )
    race_info = dm.dl.data_get( "race_info_data.pickle" )
    horce_data = dm.dl.data_get( "horce_data_storage.pickle" )
    baba_index_data = dm.dl.data_get( "baba_index_data.pickle" )
    parent_id_data = dm.dl.data_get( "parent_id_data.pickle" )
    
    ds = DataSet()
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

            past_rank_list = pd.rank_list()
            speed, up_speed, pace_speed = pd.speed_index( baba_index_data[horce_id] )

            if len( past_rank_list ) == 0:
                continue

            key_horce_num = str( int( cd.horce_number() ) )
            current_jockey = jockey_data.data_get( horce_id, cd.birthday(), cd.race_num() )
            father_id = parent_id_data[horce_id]["father"]
            mother_id = parent_id_data[horce_id]["mother"]
            father_data = dc.parent_data_get.main( horce_data, father_id, baba_index_data )
            mother_data = dc.parent_data_get.main( horce_data, mother_id, baba_index_data )
            
            odds = cd.odds() if cd.rank() == 1 else 0
            ds.set_yo( year, odds )
            
            ds.set_not_split_data( data_name.before_rank, past_rank_list[0] )            
            ds.set_not_split_data( data_name.popular, cd.popular() )            
            ds.set_not_split_data( data_name.limb, lib.limb_search( pd ) )
            ds.set_not_split_data( data_name.baba, cd.baba_status() )
            ds.set_not_split_data( data_name.horce_number, cd.horce_number() )
            ds.set_not_split_data( data_name.age, cd.year() - int( horce_id[0:4] ) )
            
            ds.set_split_data( data_name.time_index, max( time_index.main( horce_id, pd.past_day_list() )["max"], 0 ) )
            ds.set_split_data( data_name.speed_index, lib.max_check( speed ) )            
            ds.set_split_data( data_name.up_score, up_score_get.score_get( pd ) )            
            ds.set_split_data( data_name.id_weight, cd.id_weight() )
            ds.set_split_data( data_name.train_score, train_index.main( race_id, key_horce_num )["score"] )
            ds.set_split_data( data_name.pace_time_score, pace_time_score.score_get( pd ) )
            ds.set_split_data( data_name.up_speed, lib.max_check( up_speed ) )
            ds.set_split_data( data_name.pace_speed, lib.max_check( pace_speed ) )
            ds.set_split_data( data_name.money, pd.get_money() )
            ds.set_split_data( data_name.one_rate, pd.one_rate() )
            ds.set_split_data( data_name.two_rate, pd.two_rate() )
            ds.set_split_data( data_name.three_rate, pd.three_rate() )
            ds.set_split_data( data_name.best_weight, pd.best_weight() )
            ds.set_split_data( data_name.race_interval, pd.race_interval() )
            ds.set_split_data( data_name.three_average, pd.three_average() )
            ds.set_split_data( data_name.before_diff, pd.diff_get() )
            ds.set_split_data( data_name.jockey_rank, current_jockey["all"]["rank"] )
            ds.set_split_data( data_name.jockey_one_rate, current_jockey["all"]["one"] )
            ds.set_split_data( data_name.jockey_two_rate, current_jockey["all"]["two"] )
            ds.set_split_data( data_name.jockey_three_rate, current_jockey["all"]["three"] )
            ds.set_split_data( data_name.father_rank, father_data["rank"] )
            ds.set_split_data( data_name.mother_rank, mother_data["rank"] )
            
            
    ds.data_analyze()
    ds.data_upload()

if __name__ == "__main__":
    main()
