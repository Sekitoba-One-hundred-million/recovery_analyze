from common.name import Name
import sekitoba_library as lib
import sekitoba_data_manage as dm

data_name = Name()

class UsersScore:
    def __init__( self ):
        self.data = {}
        self.function = {}
        self.key_list = []
        self.recovery_score_data = dm.pickle_load( "recovery_score_data.pickle" )
        self.split_data = dm.pickle_load( "split_data.pickle" )
        self.set_function()

    def set_function( self ):
        f = open( "common/list.txt", "r" )
        name_data = f.readlines()

        for name in name_data:
            name = name.replace( "\n", "" )
            if name in self.split_data.keys():
                self.function[name] = self.split_get
            else:
                self.function[name] = self.not_split_get
        """
        self.function[data_name.before_rank] = self.not_split_get
        self.function[data_name.limb] = self.not_split_get
        self.function[data_name.popular] = self.not_split_get
        self.function[data_name.time_index] = self.split_get
        self.function[data_name.speed_index] = self.split_get
        self.function[data_name.up_score] = self.split_get
        self.function[data_name.id_weight] = self.split_get
        self.function[data_name.train_score] = self.split_get
        self.function[data_name.pace_time_score] = self.split_get
        self.function[data_name.up_speed] = self.split_get
        self.function[data_name.pace_speed] = self.split_get
        self.function[data_name.money] = self.split_get
        self.function[data_name.one_rate] = self.split_get
        self.function[data_name.two_rate] = self.split_get
        self.function[data_name.three_rate] = self.split_get
        self.function[data_name.best_weight] = self.split_get
        self.function[data_name.race_interval] = self.split_get
        self.function[data_name.three_average] = self.split_get
        self.function[data_name.before_diff] = self.split_get
        self.function[data_name.jockey_rank] = self.split_get
        self.function[data_name.jockey_one_rate] = self.split_get
        self.function[data_name.jockey_two_rate] = self.split_get
        self.function[data_name.jockey_three_rate] = self.split_get
        self.function[data_name.baba] = self.not_split_get
        self.function[data_name.horce_number] = self.not_split_get
        self.function[data_name.age] = self.not_split_get
        """
                
    def set_data( self, key, data ):
        self.data[key] = data

    def data_clear( self ):
        self.data.clear()

    def get_score( self ):
        score = 0

        for k in self.data.keys():      
            score += self.function[k]( k )

        return score

    def split_get( self, key ):
        count = len( self.split_data[key] )

        for i in range( 0, len( self.split_data[key] ) ):
            if self.split_data[key][i] < self.data[key]:
                count = i + 1

        count = min( count, len( self.split_data[key] ) - 1 )
        score = str( int( count ) )        
        return self.recovery_score_data[key][score]

    def not_split_get( self, key ):
        score = str( int( self.data[key] ) )

        try:
            return self.recovery_score_data[key][score]
        except:
            return 0
