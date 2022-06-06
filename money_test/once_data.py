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
lib.name.set_name( "rank" )

dm.dl.file_set( "race_data.pickle" )
dm.dl.file_set( "race_info_data.pickle" )
dm.dl.file_set( "horce_data_storage.pickle" )
dm.dl.file_set( "baba_index_data.pickle" )
dm.dl.file_set( "parent_id_data.pickle" )
dm.dl.file_set( "omega_index_data.pickle" )
#dm.dl.file_set( lib.name.score_name() )

class OnceData:
    def __init__( self ):
        self.race_data = dm.dl.data_get( "race_data.pickle" )
        self.race_info = dm.dl.data_get( "race_info_data.pickle" )
        self.horce_data = dm.dl.data_get( "horce_data_storage.pickle" )
        self.baba_index_data = dm.dl.data_get( "baba_index_data.pickle" )
        self.parent_id_data = dm.dl.data_get( "parent_id_data.pickle" )
        self.omega_index_data = dm.dl.data_get( "omega_index_data.pickle" )
        #self.rank_score = dm.dl.data_get( lib.name.score_name() )
        
        self.us = UsersScore()
        self.time_index = TimeIndexGet()
        self.up_score_get = UpScore()
        self.train_index = TrainIndexGet()
        self.pace_time_score = PaceTimeScore()
        self.jockey_data = JockeyData()
        self.data = {}

    def clear( self ):
        dm.dl.data_clear()

    def create( self, k ):
        race_id = lib.id_get( k )
        year = race_id[0:4]
        race_place_num = race_id[4:6]
        day = race_id[9]
        num = race_id[7]
        result = []

        key_place = str( self.race_info[race_id]["place"] )
        key_dist = str( self.race_info[race_id]["dist"] )
        key_kind = str( self.race_info[race_id]["kind"] )
        key_baba = str( self.race_info[race_id]["baba"] )
        
        #芝かダートのみ
        if key_kind == "0" or key_kind == "3":
            return None, None

        for kk in self.race_data[k].keys():
            horce_id = kk
            current_data, past_data = lib.race_check( self.horce_data[horce_id],
                                                     year, day, num, race_place_num )#今回と過去のデータに分ける
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )

            if not cd.race_check():
                continue

            before_cd = pd.before_cd()

            if before_cd == None:
                continue

            speed, up_speed, pace_speed = pd.speed_index( self.baba_index_data[horce_id] )

            horce_num = int( cd.horce_number() )
            key_horce_num = str( horce_num )
            current_jockey = self.jockey_data.data_get( horce_id, cd.birthday(), cd.race_num() )
            father_id = self.parent_id_data[horce_id]["father"]
            mother_id = self.parent_id_data[horce_id]["mother"]
            father_data = parent_data_get.main( self.horce_data, father_id, self.baba_index_data )
            mother_data = parent_data_get.main( self.horce_data, mother_id, self.baba_index_data )
            p1, p2 = before_cd.pace()

            try:
                omega_index = self.omega_index_data[race_id][horce_num-1]
                #rank_score = self.rank_score[race_id][key_horce_num]["score"]
            except:
                continue

            odds = cd.odds() if cd.rank() == 1 else 0
            self.us.set_data( data_name.before_rank, before_cd.rank() )
            self.us.set_data( data_name.popular, cd.popular() )            
            self.us.set_data( data_name.limb, lib.limb_search( pd ) )
            self.us.set_data( data_name.baba, cd.baba_status() )
            self.us.set_data( data_name.horce_number, cd.horce_number() )
            self.us.set_data( data_name.age, cd.year() - int( horce_id[0:4] ) )
            self.us.set_data( data_name.weather, cd.weather() )
            self.us.set_data( data_name.popular_rank, before_cd.rank() - before_cd.popular() )            
            self.us.set_data( data_name.time_index, max( self.time_index.main( horce_id, pd.past_day_list() )["max"], 0 ) )
            self.us.set_data( data_name.speed_index, lib.max_check( speed ) ) 
            self.us.set_data( data_name.up_score, self.up_score_get.score_get( pd ) )            
            self.us.set_data( data_name.id_weight, cd.id_weight() )
            self.us.set_data( data_name.train_score, self.train_index.main( race_id, key_horce_num )["score"] )
            self.us.set_data( data_name.pace_time_score, self.pace_time_score.score_get( pd ) )
            self.us.set_data( data_name.up_speed, lib.max_check( up_speed ) )
            self.us.set_data( data_name.pace_speed, lib.max_check( pace_speed ) )
            self.us.set_data( data_name.money, pd.get_money() )
            self.us.set_data( data_name.one_rate, pd.one_rate() )
            self.us.set_data( data_name.two_rate, pd.two_rate() )
            self.us.set_data( data_name.three_rate, pd.three_rate() )
            self.us.set_data( data_name.best_weight, pd.best_weight() )
            self.us.set_data( data_name.race_interval, pd.race_interval() )
            self.us.set_data( data_name.three_average, pd.three_average() )
            self.us.set_data( data_name.before_diff, pd.diff_get() )
            self.us.set_data( data_name.jockey_rank, current_jockey["all"]["rank"] )
            self.us.set_data( data_name.jockey_one_rate, current_jockey["all"]["one"] )
            self.us.set_data( data_name.jockey_two_rate, current_jockey["all"]["two"] )
            self.us.set_data( data_name.jockey_three_rate, current_jockey["all"]["three"] )
            self.us.set_data( data_name.father_rank, father_data["rank"] )
            self.us.set_data( data_name.mother_rank, mother_data["rank"] )
            self.us.set_data( data_name.before_up3, before_cd.up_time() )
            self.us.set_data( data_name.before_speed, before_cd.speed() )
            self.us.set_data( data_name.before_pace, p1 - p2 )
            self.us.set_data( data_name.omega, omega_index )
            #self.us.set_data( data_name.rank_score_odds, rank_score * cd.odds() )
            
            score = self.us.get_score_dict()
            result.append( { "rank": cd.rank(), "odds": cd.odds(), "score": score } )

        return result
