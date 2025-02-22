import math
import copy
from tqdm import tqdm
from mpi4py import MPI

import SekitobaLibrary as lib
import SekitobaDataManage as dm
import SekitobaPsql as ps

from SekitobaDataCreate.win_rate import WinRate
from SekitobaDataCreate.stride_ablity import StrideAblity
from SekitobaDataCreate.time_index_get import TimeIndexGet
from SekitobaDataCreate.jockey_data_get import JockeyAnalyze
from SekitobaDataCreate.trainer_data_get import TrainerAnalyze
from SekitobaDataCreate.high_level_data_get import RaceHighLevel
from SekitobaDataCreate.race_type import RaceType
from SekitobaDataCreate.before_race_score_get import BeforeRaceScore
from SekitobaDataCreate.get_horce_data import GetHorceData
from SekitobaDataCreate.kinetic_energy import KineticEnergy

from common.name import Name

data_name = Name()

class OnceData:
    def __init__( self ):
        self.race_data = ps.RaceData()
        self.race_horce_data = ps.RaceHorceData()
        self.horce_data = ps.HorceData()
        self.trainer_data = ps.TrainerData()
        self.jockey_data = ps.JockeyData()

        self.kinetic_energy = KineticEnergy( self.race_data )
        self.stride_ablity = StrideAblity( self.race_data )
        self.race_high_level = RaceHighLevel()
        self.time_index = TimeIndexGet( self.horce_data )
        self.trainer_analyze = TrainerAnalyze( self.race_data, self.race_horce_data, self.trainer_data )
        self.jockey_analyze = JockeyAnalyze( self.race_data, self.race_horce_data, self.jockey_data )
        self.race_type = RaceType()
        self.before_race_score = BeforeRaceScore( self.race_data )

        self.data_name_list = []
        self.write_data_list = []
        self.simu_data = {}
        self.kind_score_key_list = {}
        self.kind_score_key_list[data_name.waku_three_rate] = [ "place", "dist", "limb", "baba", "kind" ]
        self.kind_score_key_list[data_name.limb_score] = [ "place", "dist", "baba", "kind" ]
        self.result = { "answer": [], "teacher": [], "query": [], "year": [], "diff": [], "popular": [] }
        self.data_name_read()

    def data_name_read( self ):
        f = open( "common/list.txt", "r" )
        str_data_list = f.readlines()

        for str_data in str_data_list:
            self.data_name_list.append( str_data.replace( "\n", "" ) )

        self.data_name_list = sorted( self.data_name_list )

    def score_write( self ):
        f = open( "common/rank_score_data.txt", "w" )

        for data_name in self.write_data_list:
            f.write( data_name + "\n" )

        f.close()

    def data_list_create( self, data_dict ):
        result = []
        name_list = sorted( list( data_dict.keys() ) )
        
        for data_name in name_list:
            result.append( data_dict[data_name] )

        if len( self.write_data_list ) == 0:
            self.write_data_list = copy.deepcopy( name_list )

        return result

    def division( self, score, d ):
        if score < 0:
            score *= -1
            score /= d
            score *= -1
        else:
            score /= d

        return int( score )

    def match_rankScore( self, cd: lib.CurrentData, target_id ):
        try:
            target_data = self.horce_data[target_id]
        except:
            target_data = []
                
        target_pd = lib.PastData( target_data, [], self.race_data )
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

    def clear( self ):
        dm.dl.data_clear()
    
    def create( self, race_id ):
        self.race_data.get_all_data( race_id )
        self.race_horce_data.get_all_data( race_id )

        if len( self.race_horce_data.horce_id_list ) == 0:
            return

        self.horce_data.get_multi_data( self.race_horce_data.horce_id_list )
        self.trainer_data.get_multi_data( self.race_horce_data.trainer_id_list )
        self.jockey_data.get_multi_data( self.race_horce_data.jockey_id_list )

        year = race_id[0:4]
        race_place_num = race_id[4:6]
        day = race_id[9]
        num = race_id[7]

        key_place = str( self.race_data.data["place"] )
        key_dist = str( self.race_data.data["dist"] )
        key_kind = str( self.race_data.data["kind"] )      
        key_baba = str( self.race_data.data["baba"] )
        ymd = { "year": self.race_data.data["year"], \
               "month": self.race_data.data["month"], \
               "day": self.race_data.data["day"] }

        #芝かダートのみ
        if key_kind == "0" or key_kind == "3":
            return

        teacher_data = []
        answer_data = []
        popular_data = []
        diff_data = []
        horce_id_list = []
        race_limb = {}
        getHorceDataDict: dict[ str, GetHorceData ] = {}
        new_check = False

        for horce_id in self.race_horce_data.horce_id_list:
            current_data, past_data = lib.race_check( self.horce_data.data[horce_id]["past_data"], ymd )
            cd = lib.CurrentData( current_data )
            pd = lib.PastData( past_data, current_data, self.race_data )

            if not cd.race_check():
                continue

            getHorceData = GetHorceData( cd, pd )
            before_cd = pd.before_cd()
            place_num = int( race_place_num )
            horce_num = int( cd.horce_number() )

            before_id_weight_score = getHorceData.getBeforeIdWeight()
            before_popular = getHorceData.getBeforePopular()
            before_first_passing_rank, before_last_passing_rank = getHorceData.getBeforePassingRank()
            diff_load_weight = getHorceData.getDiffLoadWeight()
            high_level_score = self.race_high_level.data_get( cd, pd, ymd )
            race_interval_score = min( max( pd.race_interval(), 0 ), 20 )
            weight_score = getHorceData.getWeightScore()
            jockey_rank_score = self.jockey_analyze.rank( race_id, horce_id )
            waku_three_rate = getHorceData.getKindScore( self.race_data.data["waku_three_rate"] )
            before_continue_not_three_rank = pd.before_continue_not_three_rank()
            horce_sex = self.horce_data.data[horce_id]["sex"]
            dist_kind_count = pd.dist_kind_count()

            horce_true_skill = self.race_horce_data.data[horce_id]["horce_true_skill"]
            jockey_true_skill = self.race_horce_data.data[horce_id]["jockey_true_skill"]
            trainer_true_skill = self.race_horce_data.data[horce_id]["trainer_true_skill"]
            up3_horce_true_skill = self.race_horce_data.data[horce_id]["horce_up3_true_skill"]
            corner_true_skill = self.race_horce_data.data[horce_id]["horce_corner_true_skill"]

            jockey_year_rank_score = self.jockey_analyze.year_rank( horce_id, getHorceData.key_before_year )
            flame_evaluation_one = lib.escapeValue
            flame_evaluation_two = lib.escapeValue
            flame_evaluation_three = lib.escapeValue

            try:
                flame_evaluation_one = \
                  self.race_data.data["flame_evaluation"][getHorceData.key_place][getHorceData.key_day][getHorceData.key_flame_number]["one"]
                flame_evaluation_two = \
                  self.race_data.data["flame_evaluation"][getHorceData.key_place][getHorceData.key_day][getHorceData.key_flame_number]["two"]
                flame_evaluation_three = \
                  self.race_data.data["flame_evaluation"][getHorceData.key_place][getHorceData.key_day][getHorceData.key_flame_number]["three"]
            except:
                pass
            
            predict_netkeiba_deployment = lib.escapeValue

            for t in range( 0, len( self.race_data.data["predict_netkeiba_deployment"] ) ):
                if int( horce_num ) in self.race_data.data["predict_netkeiba_deployment"][t]:
                    predict_netkeiba_deployment = t
                    break

            t_instance = {}
            t_instance[data_name.before_continue_not_three_rank] = before_continue_not_three_rank
            t_instance[data_name.before_first_passing_rank] = before_first_passing_rank
            t_instance[data_name.before_id_weight] = before_id_weight_score
            t_instance[data_name.before_last_passing_rank] = before_last_passing_rank
            t_instance[data_name.before_popular] = before_popular
            t_instance[data_name.burden_weight] = cd.burden_weight()
            t_instance[data_name.dist_kind] = cd.dist_kind()
            t_instance[data_name.dist_kind_count] = dist_kind_count
            t_instance[data_name.flame_evaluation_one] = flame_evaluation_one
            t_instance[data_name.flame_evaluation_two] = flame_evaluation_two
            t_instance[data_name.flame_evaluation_three] = flame_evaluation_three
            t_instance[data_name.foot_used_best] = self.race_type.best_foot_used( cd, pd )
            t_instance[data_name.horce_num] = cd.horce_number()
            t_instance[data_name.horce_sex] = horce_sex
            t_instance[data_name.jockey_rank] = jockey_rank_score
            t_instance[data_name.limb] = getHorceData.limb_math
            t_instance[data_name.race_interval] = race_interval_score
            t_instance[data_name.high_level_score] = high_level_score
            t_instance[data_name.waku_three_rate] = waku_three_rate
            t_instance[data_name.diff_load_weight] = diff_load_weight
            t_instance[data_name.horce_true_skill] = self.race_horce_data.data[horce_id]["horce_true_skill"]
            t_instance[data_name.jockey_true_skill] = self.race_horce_data.data[horce_id]["jockey_true_skill"]
            t_instance[data_name.trainer_true_skill] = self.race_horce_data.data[horce_id]["trainer_true_skill"]
            t_instance[data_name.up3_horce_true_skill] = self.race_horce_data.data[horce_id]["horce_up3_true_skill"]
            t_instance[data_name.corner_true_skill] = self.race_horce_data.data[horce_id]["horce_corner_true_skill"]

            t_list = self.data_list_create( t_instance )

            if year in lib.test_years:
                key_dist_kind = str( int( cd.dist_kind() ) )
                key_popular = str( int( cd.popular() ) )
                popular_win_rate = { "one": 0, "two": 0, "three": 0 }
                
                try:
                    popular_win_rate = copy.deepcopy( self.popular_kind_win_rate_data[key_place][key_dist_kind][key_kind][key_popular] )
                except:
                    pass

                lib.dic_append( self.simu_data, race_id, {} )
                self.simu_data[race_id][horce_id] = {}
                self.simu_data[race_id][horce_id]["data"] = t_list
                self.simu_data[race_id][horce_id]["answer"] = { "rank": cd.rank(),
                                                               "odds": cd.odds(),
                                                               "popular": cd.popular(),
                                                               "horce_num": cd.horce_number(),
                                                               "race_kind": cd.race_kind(),
                                                               "popular_win_rate": popular_win_rate,
                                                               "new": new_check }

            answer_data.append( cd.rank() )
            teacher_data.append( t_list )
            diff_data.append( cd.diff() )
            popular_data.append( cd.popular() )

        if not len( answer_data ) == 0:
            self.result["answer"].append( answer_data )
            self.result["teacher"].append( teacher_data )
            self.result["year"].append( year )
            self.result["query"].append( { "q": len( answer_data ), "year": year } )
            self.result["diff"].append( diff_data )
            self.result["popular"].append( popular_data )
