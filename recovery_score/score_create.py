import json

import sekitoba_library as lib
from data_set import DataSet

DATA = "recovery"
COUNT = "count"

class ScoreCreate:
    def __init__( self, ds :DataSet ):
        self.ds = ds
        self.plus_score = {}
        self.minus_score = {}

    def create( self, key ):
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

        self.plus_score[key], self.minus_score[key] = lib.recovery_best_select( check_data, show = False )

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

