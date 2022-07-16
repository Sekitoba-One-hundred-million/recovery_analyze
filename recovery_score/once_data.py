from tqdm import tqdm
import numpy as np

import sekitoba_library as lib
import sekitoba_data_manage as dm

from sekitoba_data_create.time_index_get import TimeIndexGet
#from sekitoba_data_create.up_score import UpScore
#from sekitoba_data_create.train_index_get import TrainIndexGet
#from sekitoba_data_create.pace_time_score import PaceTimeScore
from sekitoba_data_create.jockey_data_get import JockeyData
from sekitoba_data_create.trainer_data_get import TrainerData
from sekitoba_data_create.high_level_data_get import RaceHighLevel
from sekitoba_data_create.race_type import RaceType
#from sekitoba_data_create import parent_data_get


from data_set import DataSet
from common.name import Name

data_name = Name()

dm.dl.file_set( "race_data.pickle" )
dm.dl.file_set( "race_info_data.pickle" )
dm.dl.file_set( "horce_data_storage.pickle" )
dm.dl.file_set( "baba_index_data.pickle" )
dm.dl.file_set( "parent_id_data.pickle" )
dm.dl.file_set( "omega_index_data.pickle" )
dm.dl.file_set( "race_day.pickle" )
dm.dl.file_set( "parent_id_data.pickle" )

class OnceData:
    def __init__( self ):
        self.race_data = dm.dl.data_get( "race_data.pickle" )
        self.race_info = dm.dl.data_get( "race_info_data.pickle" )
        self.horce_data = dm.dl.data_get( "horce_data_storage.pickle" )
        self.baba_index_data = dm.dl.data_get( "baba_index_data.pickle" )
        self.parent_id_data = dm.dl.data_get( "parent_id_data.pickle" )
        self.omega_index_data = dm.dl.data_get( "omega_index_data.pickle" )
        self.race_day = dm.dl.data_get( "race_day.pickle" )
        self.parent_id_data = dm.dl.data_get( "parent_id_data.pickle" )
        self.rank_data = {}
        
        self.ds = DataSet()
        self.race_high_level = RaceHighLevel()
        self.race_type = RaceType()
        self.time_index = TimeIndexGet()
        self.trainer_data = TrainerData()
        self.jockey_data = JockeyData()
        #self.up_score_get = UpScore()
        #self.train_index = TrainIndexGet()
        #self.pace_time_score = PaceTimeScore()

    def clear( self ):
        dm.dl.data_clear()

    def division( self, score, d ):
        if score < 0:
            score *= -1
            score /= d
            score *= -1
        else:
            score /= d

        return int( score )

    def match_rank_score( self, cd: lib.current_data, target_id ):
        try:
            target_data = self.horce_data[target_id]
        except:
            target_data = []
                
        target_pd = lib.past_data( target_data, [] )
        count = 0
        score = 0
            
        for target_cd in target_pd.past_cd_list():
            c = 0
                
            if target_cd.place() == cd.place():
                c += 1
                
            if target_cd.baba_status() == cd.baba_status():
                c += 1

            if lib.dist_check( target_cd.dist() * 1000 ) == lib.dist_check( cd.dist() * 1000 ):
                c += 1

            count += c
            score += target_cd.rank() * c

        if not count == 0:
            score /= count
                
        return int( score )

    def create( self, k ):
        race_id = lib.id_get( k )
        year = race_id[0:4]
        race_place_num = race_id[4:6]
        day = race_id[9]
        num = race_id[7]

        key_place = str( self.race_info[race_id]["place"] )
        key_dist = str( self.race_info[race_id]["dist"] )
        key_kind = str( self.race_info[race_id]["kind"] )
        key_baba = str( self.race_info[race_id]["baba"] )        
        ymd = { "y": int( year ), "m": self.race_day[race_id]["month"], "d": self.race_day[race_id]["day"] }

        #芝かダートのみ
        if key_kind == "0" or key_kind == "3":
            return

        self.rank_data[race_id] = {}
        count = 0
        race_data = {}
        race_data[data_name.speed_index] = []
        
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

            current_time_index = self.time_index.main( kk, pd.past_day_list() )
            speed, up_speed, pace_speed = pd.speed_index( self.baba_index_data[horce_id] )
            race_data[data_name.speed_index].append( lib.max_check( speed ) + lib.max_check( up_speed ) + lib.max_check( pace_speed ) + current_time_index["max"] )

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

            place_num = int( race_place_num )
            current_year = cd.year()
            horce_birth_day = int( horce_id[0:4] )
            horce_num = int( cd.horce_number() )

            try:
                omega_index_score = self.omega_index_data[race_id][horce_num-1]
            except:
                continue

            father_id = self.parent_id_data[horce_id]["father"]
            mother_id = self.parent_id_data[horce_id]["mother"]
            
            father_score = self.match_rank_score( cd, father_id )
            mother_score = self.match_rank_score( cd, mother_id )
            stright_slope_score = self.race_type.stright_slope( cd, pd )
            foot_used_score = self.race_type.foot_used( cd, pd )
            high_level_score = self.race_high_level.data_get( cd, pd, ymd )
            limb_math = lib.limb_search( pd )
            age = current_year - horce_birth_day
            speed_index_score = race_data[data_name.speed_index].index( race_data[data_name.speed_index][count] )
            race_interval_score = min( max( pd.race_interval(), 0 ), 20 )
            weight_score = int( cd.weight() / 10 )
            before_id_weight_score = self.division( min( max( before_cd.id_weight(), -10 ), 10 ), 2 )
            omega_index_score = int( omega_index_score / 5 )
            before_speed_score = int( before_cd.speed() )
            trainer_rank_score = self.trainer_data.rank( race_id, horce_id )
            jockey_rank_score = self.jockey_data.rank( race_id, horce_id )
            popular_rank = abs( before_cd.rank() - before_cd.popular() )
            before_diff_score = int( max( before_cd.diff(), 0 ) * 10 )
            limb_horce_number = int( limb_math * 100 + int( cd.horce_number() / 2 ) )
            macth_rank_score = pd.match_rank()
            
            count += 1
            odds = cd.odds() if cd.rank() == 1 else 0
            
            self.rank_data[race_id][horce_id] = cd.rank()
            self.ds.set_yo( year, odds )
            self.ds.set_id( race_id, horce_id )
            self.ds.set_rank_data( cd.rank() )
            
            self.ds.set_users_data( data_name.before_rank, before_cd.rank() )
            self.ds.set_users_data( data_name.race_level_check, high_level_score )
            self.ds.set_users_data( data_name.straight_slope, stright_slope_score )
            self.ds.set_users_data( data_name.foot_used, foot_used_score )
            self.ds.set_users_data( data_name.limb, limb_math )
            self.ds.set_users_data( data_name.age, age )
            self.ds.set_users_data( data_name.speed_index, speed_index_score )
            self.ds.set_users_data( data_name.race_interval, race_interval_score )
            self.ds.set_users_data( data_name.weight, weight_score )
            self.ds.set_users_data( data_name.before_id_weight, before_id_weight_score )
            self.ds.set_users_data( data_name.omega, omega_index_score )
            self.ds.set_users_data( data_name.before_speed, before_speed_score )
            self.ds.set_users_data( data_name.popular, cd.popular() )
            self.ds.set_users_data( data_name.trainer_rank, trainer_rank_score )
            self.ds.set_users_data( data_name.jockey_rank, jockey_rank_score )
            self.ds.set_users_data( data_name.popular_rank, popular_rank )
            self.ds.set_users_data( data_name.before_diff, before_diff_score )
            self.ds.set_users_data( data_name.limb_horce_number, limb_horce_number )
            self.ds.set_users_data( data_name.father_rank, father_score )
            self.ds.set_users_data( data_name.mother_rank, mother_score )
            self.ds.set_users_data( data_name.match_rank, macth_rank_score )
