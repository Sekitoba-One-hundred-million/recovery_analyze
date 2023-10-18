import json
import math
import random
import copy

import sekitoba_library as lib
from data_set import DataSet

USERS_SCORE = "users_score"
RANK = "rank"
ODDS = "odds"
RECOVERY = "recovery"
COUNT = "count"
    
class ScoreCreate:
    def __init__( self, ds :DataSet ):
        self.ds = ds
        self.plus_score = {}
        self.minus_score = {}

    def plus_recovery_select( self, data, users_score_list = None ):
        def base10int(value, base):
            if (int(value / base)):
                return base10int(int(value / base), base) + str(value % base)
            return str(value % base)

        def str_hexadecimal( value, base, l ):
            str_data = base10int( value, base )
            
            if l < len( str_data ):
                return None
    
            return int( l - len( str_data ) ) * '0' + str_data

        best_select = []
        best_score = -100
        best_recovery = 0

        if users_score_list == None:
            users_score_list = []
            key_data = {}

            for race_id in data.keys():
                for users_score in data[race_id].keys():
                    lib.dic_append( key_data, users_score, 0 )
                    key_data[users_score] += data[race_id][users_score][COUNT]

            key_data = sorted( key_data.items(), key = lambda x:x[1] ,reverse = True )
    
            for i in range( 0, len( key_data ) ):
                if key_data[i][1] < 3000 or len( users_score_list ) == 10:
                    break
        
                users_score_list.append( key_data[i][0] )

        c = 2
        l = len( users_score_list )
        check = pow( c, l )
        race_id_list = list( data.keys() )

        for i in range( 0, pow( c, l ) ):
            use_users_score_data = []
            str_check = str_hexadecimal( i, c, l )

            if str_check == None:
                continue

            for r, s in enumerate( str_check ):
                if not s == "1":
                    continue

                use_users_score_data.append( users_score_list[r] )

            if len( use_users_score_data ) == 0:
                continue

            search_length = 10
            score_list = []
            
            for _ in range( 5 ):
                recovery_list = []
                random_race_id_list = random.sample( race_id_list, len( race_id_list ) )
                recovery = 0
                bet_count = 0
                count = 0
                length = int( len( race_id_list ) / search_length )

                while not random_race_id_list == []:
                    race_id = random_race_id_list.pop()
                    
                    if count == length:
                        if not bet_count == 0:
                            recovery_list.append( recovery / bet_count )
                            
                        count = 0
                        bet_count = 0
                        recovery = 0

                    count += 1
                    for users_score in use_users_score_data:
                        if not users_score in data[race_id]:
                            continue
                        
                        bet_count += data[race_id][users_score]["count"]
                        recovery += data[race_id][users_score]["recovery"]

                if bet_count > 20:
                    recovery_list.append( recovery / bet_count )

                recovery_list = sorted( recovery_list )
                ave_recovery = sum( recovery_list ) / len( recovery_list )
                median_recovery = recovery_list[int(len(recovery_list)/2)]
                conv = 0
                median_conv = 0
                min_recovery = 10
                max_recovery = -10

                for recovery in recovery_list:
                    conv += math.pow( recovery - ave_recovery, 2 )
                    median_conv += math.pow( recovery - median_recovery, 2 )
                    min_recovery = min( min_recovery, recovery )
                    max_recovery = max( max_recovery, recovery )

                conv = math.sqrt( conv / len( recovery_list ) )
                recovery_score = ( ( median_recovery + ave_recovery ) / 2 )# - ( 1 - min_recovery ) - ( 1 - max_recovery )
                conv_score = ( conv + median_conv ) / 2
                #print( recovery_score, conv_score, use_users_score_data )

                if recovery_score - conv_score < 0.65:
                    score_list = []
                    break
                
                score_list.append( recovery_score - conv_score )

            if len( score_list ) == 0:
                continue

            score = ( sum( score_list ) / len( score_list ) ) + score_list[int(len(score_list)/2)]
            
            if best_score < score:
                best_score = score
                best_select = copy.deepcopy( use_users_score_data )

        return best_select, users_score_list

    def recovery_best_select( self, data ):
        plus_best_select, users_score_list = self.plus_recovery_select( data )
        #print( plus_best_select )

        for plus_score in plus_best_select:
            users_score_list.remove( plus_score )
        
        middle_best_select, users_score_list = self.plus_recovery_select( data, users_score_list = users_score_list )
        #print( middle_best_select )

        for middle_score in middle_best_select:
            users_score_list.remove( middle_score )

        #print( users_score_list )
        return plus_best_select, users_score_list

    def create( self, key ):
        check_data = {}
        
        for race_id in self.ds.users_data.keys():
            year = race_id[0:4]

            if year in lib.test_years:
                continue

            check_data[race_id] = {}
            
            for horce_id in self.ds.users_data[race_id].keys():
                score = int( self.ds.users_data[race_id][horce_id][key] )
                lib.dic_append( check_data[race_id], score, { RECOVERY: 0, COUNT: 0 } )
                check_data[race_id][score][COUNT] += 1

                if self.ds.rank_data[race_id][horce_id] == 1:
                    check_data[race_id][score][RECOVERY] += self.ds.odds_data[race_id][horce_id]
                
        self.plus_score[key], self.minus_score[key] = self.recovery_best_select( check_data )

    def json_create( self ):
        if len( self.plus_score ) == 0 or len( self.minus_score ) == 0:
            print( "not found score" )
            return False

        f = open( "plus_score.json", "w" )
        json.dump( self.plus_score, f, indent = 4 )
        f.close()

        f = open( "minus_score.json", "w" )
        json.dump( self.minus_score, f, indent = 4 )
        f.close()
