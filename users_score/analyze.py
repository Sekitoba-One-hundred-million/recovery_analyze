import sekitoba_library as lib
import sekitoba_data_manage as dm
from score import UsersScoreFunction
from common.name import Name

data_name = Name()

dm.dl.file_set( "odds_data.pickle" )
dm.dl.file_set( "split_data.pickle" )
dm.dl.file_set( "users_data.pickle" )
dm.dl.file_set( "users_rank_data.pickle" )
dm.dl.file_set( "recovery_score_data.pickle" )
#dm.dl.file_set( "users_score_rate.pickle" )

class UsersAnalyze:
    def __init__( self ):
        self.data = {}
        self.function = {}
        self.buy_function = {}
        self.users_score_data = {}
        self.key_list = []
        self.odds_key = { "one": "単勝", "quinella": "馬連", "wide": "ワイド", "triple": "三連複" }
        self.odds_data = dm.dl.data_get( "odds_data.pickle" )
        self.users_data = dm.dl.data_get( "users_data.pickle" )
        self.user_rank_data = dm.dl.data_get( "users_rank_data.pickle" )
        #self.users_score_rate = dm.dl.data_get( "users_score_rate.pickle" )
        self.users_score_function = UsersScoreFunction()
        self.set_function()

    def set_function( self ):
        self.buy_function["one"] = self.one
        self.buy_function["quinella"] = self.quinella
        self.buy_function["wide"] = self.wide
        self.buy_function["triple"] = self.triple

        self.users_score_function.set_function()

    def get_score( self, race_id, horce_id ):
        score = 0
        lib.dic_append( self.users_score_data, race_id, {} )
        lib.dic_append( self.users_score_data[race_id], horce_id, {} )
        self.data = self.users_data[race_id][horce_id]
        
        for k in self.data.keys():
            s = self.users_score_function.function[k]( self.data[k] )
            self.users_score_data[race_id][horce_id][k] = s
            score += s

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

    def quinella( self, race_score_data, rank_data, odds ):
        result = []
        key_list = list( race_score_data.keys() )

        for i in range( 0, len( key_list ) ):
            horce_id_1 = key_list[i]
            rank_1 = rank_data[horce_id_1]
            
            for r in range( i + 1, len( key_list ) ):
                horce_id_2 = key_list[r]
                rank_2 = rank_data[horce_id_2]
                score = int( race_score_data[horce_id_1] + race_score_data[horce_id_2] )
                instance = { "score": score, "odds": 0 }

                if rank_1 <= 2 and rank_2 <= 2:
                    instance["odds"] = odds / 100

                result.append( instance )

        return result

    def wide( self, race_score_data, rank_data, wide_odds ):
        result = []
        key_list = list( race_score_data.keys() )

        for i in range( 0, len( key_list ) ):
            horce_id_1 = key_list[i]
            rank_1 = rank_data[horce_id_1]
            
            for r in range( i + 1, len( key_list ) ):
                horce_id_2 = key_list[r]
                rank_2 = rank_data[horce_id_2]
                score = int( race_score_data[horce_id_1] + race_score_data[horce_id_2] )
                instance = { "score": score, "odds": 0 }

                if rank_1 <= 3 and rank_2 <= 3:
                    index = int( rank_1 + rank_2 - 3 )
                    #print( wide_odds, index )
                    if index < len( wide_odds ):
                        instance["odds"] = wide_odds[index] / 100

                result.append( instance )

        return result

    def triple( self, race_score_data, rank_data, odds ):
        result = []
        key_list = list( race_score_data.keys() )

        for i in range( 0, len( key_list ) ):
            horce_id_1 = key_list[i]
            rank_1 = rank_data[horce_id_1]
            
            for r in range( i + 1, len( key_list ) ):
                horce_id_2 = key_list[r]
                rank_2 = rank_data[horce_id_2]

                for t in range( r + 1, len( key_list ) ):
                    horce_id_3 = key_list[t]
                    rank_3 = rank_data[horce_id_3]

                    score = int( race_score_data[horce_id_1] + race_score_data[horce_id_2] + race_score_data[horce_id_3] )
                    instance = { "score": score, "odds": 0 }

                    if rank_1 <= 3 and rank_2 <= 3 and rank_3 <= 3:
                        instance["odds"] = odds / 100

                    result.append( instance )

        return result

    def buy_simulation( self, race_score_data, race_id ):
        result = {}

        try:
            current_odds = self.odds_data[race_id]
        except:
            return None

        for kind in self.odds_key.keys():
            result[kind] = self.buy_function[kind]( race_score_data, \
                                                   self.user_rank_data[race_id], \
                                                   current_odds[self.odds_key[kind]] )

        return result

    def users_analyze( self ):
        result = {}
        test_result = {}
        score_data = {}
        
        for race_id in self.users_data.keys():
            score_data[race_id] = {}
            
            for horce_id in self.users_data[race_id].keys():
                score = int( self.get_score( race_id, horce_id ) )
                score_data[race_id][horce_id] = score
            
        for race_id in score_data.keys():
            year = race_id[0:4]
            
            if year in lib.test_years:
                continue

            lib.dic_append( result, year, {} )
            buy_result = self.buy_simulation( score_data[race_id], race_id )

            if buy_result == None:
                continue

            for kind in self.odds_key.keys():
                lib.dic_append( result[year], kind, [] )
                result[year][kind].extend( buy_result[kind] )

        return result
