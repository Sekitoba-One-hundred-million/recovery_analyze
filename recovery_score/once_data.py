from tqdm import tqdm
import numpy as np

import sekitoba_library as lib
import sekitoba_data_manage as dm

from sekitoba_data_create.time_index_get import TimeIndexGet
#from sekitoba_data_create.up_score import UpScore
from sekitoba_data_create.train_index_get import TrainIndexGet
#from sekitoba_data_create.pace_time_score import PaceTimeScore
from sekitoba_data_create.jockey_data_get import JockeyData
from sekitoba_data_create.trainer_data_get import TrainerData
from sekitoba_data_create.high_level_data_get import RaceHighLevel
from sekitoba_data_create.race_type import RaceType
from sekitoba_data_create.before_data import BeforeData
#from sekitoba_data_create import parent_data_get

from data_set import DataSet
from common.name import Name

data_name = Name()

dm.dl.file_set( "race_data.pickle" )
dm.dl.file_set( "odds_data.pickle" )
dm.dl.file_set( "race_info_data.pickle" )
dm.dl.file_set( "horce_data_storage.pickle" )
dm.dl.file_set( "baba_index_data.pickle" )
dm.dl.file_set( "parent_id_data.pickle" )
dm.dl.file_set( "race_day.pickle" )
dm.dl.file_set( "parent_id_data.pickle" )
dm.dl.file_set( "horce_sex_data.pickle" )
dm.dl.file_set( "horce_blood_type_data.pickle" )
dm.dl.file_set( "race_jockey_id_data.pickle" )
dm.dl.file_set( "race_trainer_id_data.pickle" )
dm.dl.file_set( "true_skill_data.pickle" )
dm.dl.file_set( "race_cource_info.pickle" )
dm.dl.file_set( "race_money_data.pickle" )
dm.dl.file_set( "up3_true_skill_data.pickle" )

class OnceData:
    def __init__( self ):
        self.race_data = dm.dl.data_get( "race_data.pickle" )
        self.odds_data = dm.dl.data_get( "odds_data.pickle" )
        self.race_info = dm.dl.data_get( "race_info_data.pickle" )
        self.horce_data = dm.dl.data_get( "horce_data_storage.pickle" )
        self.baba_index_data = dm.dl.data_get( "baba_index_data.pickle" )
        self.parent_id_data = dm.dl.data_get( "parent_id_data.pickle" )
        self.race_day = dm.dl.data_get( "race_day.pickle" )
        self.parent_id_data = dm.dl.data_get( "parent_id_data.pickle" )
        self.horce_sex_data = dm.dl.data_get( "horce_sex_data.pickle" )
        self.horce_blood_type_data = dm.dl.data_get( "horce_blood_type_data.pickle" )
        self.race_jockey_id_data = dm.dl.data_get( "race_jockey_id_data.pickle" )
        self.race_trainer_id_data = dm.dl.data_get( "race_trainer_id_data.pickle" )
        self.true_skill_data = dm.dl.data_get( "true_skill_data.pickle" )
        self.race_cource_info = dm.dl.data_get( "race_cource_info.pickle" )
        self.race_money_data = dm.dl.data_get( "race_money_data.pickle" )
        self.up3_true_skill_data = dm.dl.data_get( "up3_true_skill_data.pickle" )
        
        self.ds = DataSet()
        self.race_high_level = RaceHighLevel()
        self.race_type = RaceType()
        self.time_index = TimeIndexGet()
        self.trainer_data = TrainerData()
        self.jockey_data = JockeyData()
        self.before_data = BeforeData()
        #self.up_score_get = UpScore()
        self.train_index = TrainIndexGet()
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

        if int( key_place ) == 8:
            return

        #芝かダートのみ
        if key_kind == "0" or key_kind == "3":
            return

        if "out_side" in self.race_info[race_id] and self.race_info[race_id]["out_side"]:
            key_dist += "外"
        
        try:
            straight_dist = int( self.race_cource_info[key_place][key_kind][key_dist]["dist"][0] / 100 )
        except:
            straight_dist = -1

        count = 0
        race_limb = {}
        current_race_data = {}
        current_race_data[data_name.speed_index] = []
        current_race_data[data_name.horce_jockey_true_skill_index] = []
        current_race_data[data_name.my_limb_count] = {}
        
        for kk in self.race_data[k].keys():
            horce_id = kk
            current_data, past_data = lib.race_check( self.horce_data[horce_id],
                                                     year, day, num, race_place_num )#今回と過去のデータに分ける
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )

            if not cd.race_check():
                continue

            limb_math = lib.limb_search( pd )
            key_limb = str( int( limb_math ) )
            lib.dic_append( current_race_data[data_name.my_limb_count], key_limb, 0 )
            current_race_data[data_name.my_limb_count][key_limb] += 1
            race_limb[kk] = limb_math
            
            current_time_index = self.time_index.main( kk, pd.past_day_list() )
            speed, up_speed, pace_speed = pd.speed_index( self.baba_index_data[horce_id] )
            current_race_data[data_name.speed_index].append( lib.max_check( speed ) + current_time_index["max"] )

            try:
                horce_true_skill = int( self.true_skill_data["horce"][race_id][horce_id] )
            except:
                horce_true_skill = 25

            try:
                jockey_id = self.race_jockey_id_data[race_id][horce_id]
                jockey_true_skill = int( self.true_skill_data["jockey"][race_id][jockey_id] )
            except:
                jockey_true_skill = 25

            current_race_data[data_name.horce_jockey_true_skill_index].append( horce_true_skill + jockey_true_skill )


        sort_speed_index = sorted( current_race_data[data_name.speed_index], reverse = True )

        for kk in self.race_data[k].keys():
            horce_id = kk
            current_data, past_data = lib.race_check( self.horce_data[horce_id],
                                                     year, day, num, race_place_num )#今回と過去のデータに分ける
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )

            if not cd.race_check():
                continue                

            place_num = int( race_place_num )
            current_year = cd.year()
            horce_birth_day = int( horce_id[0:4] )
            horce_num = int( cd.horce_number() )
            key_horce_num = str( horce_num )

            before_cd = pd.before_cd()

            if before_cd == None:
                continue

            before_id_weight_score = self.division( min( max( before_cd.id_weight(), -10 ), 10 ), 2 )
            before_speed_score = int( before_cd.speed() )
            before_diff_score = int( max( before_cd.diff(), 0 ) * 10 )
            before_popular = before_cd.popular()
            before_passing_list = before_cd.passing_rank().split( "-" )
            
            try:
                before_last_passing_rank = int( before_passing_list[-1] )
            except:
                before_last_passing_rank = 0

            try:
                before_first_passing_rank = int( before_passing_list[0] )
            except:
                before_first_passing_rank = 0

            p1, p2 = before_cd.pace()
            up3 = before_cd.up_time()
            up3_standard_value = max( min( ( up3 - p2 ) * 5, 15 ), -10 )
            popular_rank_score = before_cd.rank() - before_cd.popular()
            before_rank = before_cd.rank()
            horce_true_skill = 25
            jockey_true_skill = 25
            trainer_true_skill = 25
            up3_horce_true_skill = 25

            jockey_id = ""
            trainer_id = ""

            if race_id in self.race_jockey_id_data and \
              horce_id in self.race_jockey_id_data[race_id]:
                jockey_id = self.race_jockey_id_data[race_id][horce_id]

            if race_id in self.race_trainer_id_data and \
              horce_id in self.race_trainer_id_data[race_id]:
                trainer_id = self.race_trainer_id_data[race_id][horce_id]
            
            if race_id in self.true_skill_data["horce"] and \
              horce_id in self.true_skill_data["horce"][race_id]:
                horce_true_skill = int( self.true_skill_data["horce"][race_id][horce_id] )

            if race_id in self.true_skill_data["jockey"] and \
              jockey_id in self.true_skill_data["jockey"][race_id]:
                jockey_true_skill = int( self.true_skill_data["jockey"][race_id][jockey_id] )

            if race_id in self.true_skill_data["trainer"] and \
              trainer_id in self.true_skill_data["trainer"][race_id]:
                trainer_true_skill = int( self.true_skill_data["trainer"][race_id][trainer_id] )

            if race_id in self.up3_true_skill_data["horce"] and \
              horce_id in self.up3_true_skill_data["horce"][race_id]:
                up3_horce_true_skill = int( self.up3_true_skill_data["horce"][race_id][horce_id] )

            try:
                father_blood_type = self.horce_blood_type_data[race_id][key_horce_num]["father"]
            except:
                father_blood_type = 0

            straight_flame_score = 0
            
            if cd.horce_number() < cd.all_horce_num() / 3:
                straight_flame_score = int( 100 + straight_dist )
            elif ( cd.all_horce_num() / 3 ) * 2 <= cd.horce_number():
                straight_flame_score = int( 200 + straight_dist )

            before_year = int( year ) - 1
            key_before_year = str( int( before_year ) )
            father_id = self.parent_id_data[horce_id]["father"]
            mother_id = self.parent_id_data[horce_id]["mother"]
            
            #father_score = self.match_rank_score( cd, father_id )
            mother_score = self.match_rank_score( cd, mother_id )
            stright_slope_score = self.race_type.stright_slope( cd, pd )
            foot_used_score = self.race_type.foot_used_score_get( cd, pd )
            high_level_score = self.race_high_level.data_get( cd, pd, ymd )
            limb_math = race_limb[kk]#lib.limb_search( pd )
            key_limb = str( int( limb_math ) )
            my_limb_count_score = current_race_data[data_name.my_limb_count][key_limb]
            age = current_year - horce_birth_day
            speed_index_score = sort_speed_index.index( current_race_data[data_name.speed_index][count] )
            race_interval_score = min( max( pd.race_interval(), 0 ), 20 )
            weight_score = int( cd.weight() / 10 )
            trainer_rank_score = self.trainer_data.rank( race_id, horce_id )
            jockey_rank_score = self.jockey_data.rank( race_id, horce_id )
            limb_horce_number = int( limb_math * 100 + int( cd.horce_number() / 2 ) )
            macth_rank_score = pd.match_rank()
            money_score = pd.get_money()

            if not money_score == 0:
                money_score += 100
                
            money_score = min( int( money_score / 200 ), 30 )
            burden_weight_score = int( max( cd.burden_weight() - 50, 0 ) )
            before_continue_not_three_rank = pd.before_continue_not_three_rank()
            #limb_place_score = int( cd.place() * 10 + limb_math )
            horce_sex = self.horce_sex_data[horce_id]
            horce_sex_month = int( self.race_day[race_id]["month"] * 10 + horce_sex )
            dist_kind_count = min( pd.dist_kind_count(), 20 )
            jockey_year_rank_score = int( self.jockey_data.year_rank( race_id, horce_id, key_before_year ) / 10 )
            baba = cd.baba_status()
            train_score = self.train_index.score_get( race_id, horce_num )
            deployment_score = self.race_type.deploypent( pd )
            father_blood_type_score = int( cd.dist_kind() * 10 + father_blood_type )
            horce_jockey_true_skill_index = current_race_data[data_name.horce_jockey_true_skill_index].index( horce_true_skill + jockey_true_skill )
            foot_used_count = -1
            diff_load_weight = int( cd.burden_weight() - before_cd.burden_weight() )
            race_num = cd.race_num()

            try:
                race_money = lib.money_class_get( self.race_money_data[race_id] )
            except:
                race_money = -1

            count += 1
            odds = cd.odds() if cd.rank() == 1 else 0
            
            self.ds.set_yo( year, odds )
            self.ds.set_id( race_id, horce_id )
            self.ds.set_rank_data( cd.rank() )
            self.ds.set_odds_data( cd.odds() )

            self.ds.set_users_data( data_name.age, age )
            self.ds.set_users_data( data_name.all_horce_num, cd.all_horce_num() )
            self.ds.set_users_data( data_name.baba, baba )
            self.ds.set_users_data( data_name.before_rank, before_rank )
            self.ds.set_users_data( data_name.before_continue_not_three_rank, before_continue_not_three_rank )
            self.ds.set_users_data( data_name.before_diff, before_diff_score )
            self.ds.set_users_data( data_name.before_first_passing_rank, before_first_passing_rank )
            self.ds.set_users_data( data_name.before_id_weight, before_id_weight_score )
            self.ds.set_users_data( data_name.before_last_passing_rank, before_last_passing_rank )
            self.ds.set_users_data( data_name.before_pace, self.before_data.pace( before_cd.race_id() ) )
            self.ds.set_users_data( data_name.before_popular, before_popular )
            self.ds.set_users_data( data_name.before_speed, before_speed_score )
            self.ds.set_users_data( data_name.best_weight, pd.best_weight() )
            self.ds.set_users_data( data_name.burden_weight, burden_weight_score )
            self.ds.set_users_data( data_name.diff_load_weight, diff_load_weight )
            self.ds.set_users_data( data_name.dist_kind_count, dist_kind_count )
            self.ds.set_users_data( data_name.father_blood_type, father_blood_type_score )
            self.ds.set_users_data( data_name.foot_used, foot_used_score )
            self.ds.set_users_data( data_name.horce_jockey_true_skill_index, horce_jockey_true_skill_index )
            self.ds.set_users_data( data_name.horce_num, horce_num )
            self.ds.set_users_data( data_name.horce_true_skill, horce_true_skill )
            self.ds.set_users_data( data_name.horce_sex, horce_sex )
            self.ds.set_users_data( data_name.horce_sex_month, horce_sex_month )
            self.ds.set_users_data( data_name.jockey_true_skill, jockey_true_skill )
            self.ds.set_users_data( data_name.jockey_rank, jockey_rank_score )
            self.ds.set_users_data( data_name.jockey_year_rank, jockey_year_rank_score )
            self.ds.set_users_data( data_name.level_score, pd.level_score() * 10 )
            self.ds.set_users_data( data_name.limb, limb_math )
            self.ds.set_users_data( data_name.limb_horce_number, limb_horce_number )
            self.ds.set_users_data( data_name.match_rank, macth_rank_score )
            self.ds.set_users_data( data_name.money_score, money_score )
            self.ds.set_users_data( data_name.mother_rank, mother_score )
            self.ds.set_users_data( data_name.my_limb_count, my_limb_count_score )
            self.ds.set_users_data( data_name.place, cd.place() )
            self.ds.set_users_data( data_name.popular_rank, popular_rank_score )
            self.ds.set_users_data( data_name.race_deployment, deployment_score )
            self.ds.set_users_data( data_name.race_num, race_num )
            self.ds.set_users_data( data_name.money_class, race_money )
            self.ds.set_users_data( data_name.race_interval, race_interval_score )
            self.ds.set_users_data( data_name.high_level_score, high_level_score )
            self.ds.set_users_data( data_name.speed_index_index, speed_index_score )
            self.ds.set_users_data( data_name.straight_flame, straight_flame_score )
            self.ds.set_users_data( data_name.straight_slope, stright_slope_score )
            self.ds.set_users_data( data_name.three_average, pd.three_average() )
            self.ds.set_users_data( data_name.train_score, train_score )
            self.ds.set_users_data( data_name.trainer_rank, trainer_rank_score )
            self.ds.set_users_data( data_name.trainer_true_skill, trainer_true_skill )
            self.ds.set_users_data( data_name.up3_standard_value, up3_standard_value )
            self.ds.set_users_data( data_name.up3_horce_true_skill, up3_horce_true_skill )
            self.ds.set_users_data( data_name.weather, cd.weather() )
            self.ds.set_users_data( data_name.weight, weight_score )
