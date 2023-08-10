import sekitoba_library as lib
import sekitoba_data_manage as dm
from score import UsersScoreFunction
#from three_score import UsersThreeScoreFunction
from common.name import Name

data_name = Name()

dm.dl.file_set( "odds_data.pickle" )
dm.dl.file_set( "split_data.pickle" )
dm.dl.file_set( "users_data.pickle" )
dm.dl.file_set( "users_rank_data.pickle" )
dm.dl.file_set( "recovery_score_data.pickle" )
#dm.dl.file_set( "users_score_rate.pickle" )

ONE = "one"
THREE = "three"

class UsersAnalyze:
    def __init__( self ):
        self.data = {}
        self.function = {}
        self.buy_function = {}
        self.users_score_data = {}
        self.key_list = []
        self.odds_key = { ONE: "単勝" }
        self.odds_data = dm.dl.data_get( "odds_data.pickle" )
        self.users_data = dm.dl.data_get( "users_data.pickle" )
        self.user_rank_data = dm.dl.data_get( "users_rank_data.pickle" )
        self.users_score_function = UsersScoreFunction()
        
    def get_one_score( self, race_id, horce_id ):
        score = 0
        lib.dic_append( self.users_score_data, race_id, {} )
        lib.dic_append( self.users_score_data[race_id], horce_id, {} )
        self.data = self.users_data[race_id][horce_id]
        
        for k in self.users_score_function.plus_score.keys():
            math_data = int( self.data[k] )
            
            if math_data in self.users_score_function.plus_score[k]:
                self.users_score_data[race_id][horce_id][k] = 1
                score += 1

            if math_data in self.users_score_function.minus_score[k]:
                self.users_score_data[race_id][horce_id][k] = -1
                score -= 1

        return score

    def one( self, race_score_data, rank_data, odds ):
        result = []

        for horce_id in race_score_data.keys():
            instance = { "score": int( race_score_data[horce_id] ), "odds": 0 }
            rank = rank_data[horce_id]

            if rank == 1:
                instance["odds"] = odds / 100

            result.append( instance )

        return result
    
    def buy_simulation( self, race_score_data, race_id ):
        result = []

        try:
            current_odds = self.odds_data[race_id]
        except:
            return None

        result = self.one( race_score_data, \
                          self.user_rank_data[race_id], \
                          current_odds[self.odds_key[ONE]] )

        return result

    def users_analyze( self, test = False ):
        result = {}
        test_result = {}
        score_data = {}
        
        for race_id in self.users_data.keys():
            score_data[race_id] = {}
            
            for horce_id in self.users_data[race_id].keys():
                score_data[race_id][horce_id] = int( self.get_one_score( race_id, horce_id ) )
            
        for race_id in score_data.keys():
            year = race_id[0:4]
            
            if ( year in lib.test_years and not test ) or ( not year in lib.test_years and test ):
                continue

            buy_result = self.buy_simulation( score_data[race_id], race_id )

            if buy_result == None:
                continue

            lib.dic_append( result, year, [] )
            result[year].extend( buy_result )

        return result
