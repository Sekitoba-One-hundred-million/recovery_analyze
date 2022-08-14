import copy

import sekitoba_library as lib
import sekitoba_data_manage as dm

class Data:
    def __init__( self, users_score_data ):
        self.learn_data = {}
        self.test_data = {}
        self.name_list = []
        self.N = 0

        f = open( "common/score_data_name.txt", "r" )
        str_data_list = f.readlines()

        for str_data in str_data_list:
            self.name_list.append( lib.text_replace( str_data ) )

        self.N = len( self.name_list )

        for race_id in users_score_data.keys():
            year = race_id[0:4]

            for horce_id in users_score_data[race_id].keys():
                instance = []
                
                for score_name in self.name_list:
                    instance.append( users_score_data[race_id][horce_id][score_name] )

                if year in lib.test_years:
                    lib.dic_append( self.test_data, race_id, {} )
                    self.test_data[race_id][horce_id] = copy.deepcopy( instance )
                else:
                    lib.dic_append( self.learn_data, race_id, {} )
                    self.learn_data[race_id][horce_id] = copy.deepcopy( instance )
