import json

import sekitoba_library as lib
from data_set import DataSet

DATA = "recovery"
COUNT = "count"

class PlusScoreCreate:
    def __init__( self, ds :DataSet ):
        self.ds = ds
        self.plus_score = {}

    def target_plus( self, key ):
        check_data = {}
        
        for race_id in self.ds.users_data.keys():
            year = race_id[0:4]

            if year in lib.test_years:
                continue
            
            lib.dic_append( check_data, year, {} )
            
            for horce_id in self.ds.users_data[race_id].keys():
                score = self.ds.users_data[race_id][horce_id][key]
                key_score = str( int( score ) )
                lib.dic_append( check_data[year], key_score, { DATA: 0, COUNT: 0 } )

                check_data[year][key_score][COUNT] += 1

                if self.ds.rank_data[race_id][horce_id] == 1:
                    check_data[year][key_score][DATA] += self.ds.odds_data[race_id][horce_id]

        for year in check_data.keys():
            for score_key in check_data[year].keys():
                check_data[year][score_key][DATA] /= check_data[year][score_key][COUNT]
                check_data[year][score_key][DATA] = round( check_data[year][score_key][DATA], 2 )

        self.plus_score[key] = lib.recovery_best_select( check_data, show = False )

    def plus_json_create( self ):
        if len( self.plus_score ) == 0:
            print( "not found plus_score" )
            return False

        f = open( "plus_score.json", "w" )
        json.dump( self.plus_score, f, indent = 4 )
