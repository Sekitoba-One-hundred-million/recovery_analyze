import sekitoba_library as lib
import sekitoba_data_manage as dm

class DataSet:
    def __init__( self ):
        self.rank_data = {}
        self.odds_data = {}
        self.users_data = {}
        self.year = ""
        self.odds = 0
        self.race_id = ""
        self.horce_id = ""

    def set_all_data( self, users_data, rank_data, odds_data ):
        self.rank_data = rank_data
        self.users_data = users_data
        self.odds_data = odds_data

    def set_yo( self, year, odds ):
        self.year = year
        self.odds = odds

    def set_id( self, race_id, horce_id ):
        self.race_id = race_id
        self.horce_id = horce_id
        lib.dic_append( self.users_data, self.race_id, {} )
        lib.dic_append( self.users_data[self.race_id], self.horce_id, {} )
        lib.dic_append( self.rank_data, self.race_id, {} )
        lib.dic_append( self.odds_data, self.race_id, {} )

    def set_users_data( self, name, data ):
        self.users_data[self.race_id][self.horce_id][name] = data
        #self.users_data[self.race_id][self.horce_id][name+"_minus"] = data 

    def set_rank_data( self, rank ):
        self.rank_data[self.race_id][self.horce_id] = rank

    def set_odds_data( self, odds ):
        self.odds_data[self.race_id][self.horce_id] = odds

    def data_upload( self ):
        dm.pickle_upload( "users_odds_data.pickle", self.odds_data )
        dm.pickle_upload( "users_rank_data.pickle", self.rank_data )
        dm.pickle_upload( "users_data.pickle", self.users_data )
