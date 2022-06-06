from common.name import Name
import sekitoba_library as lib
import sekitoba_data_manage as dm

data_name = Name()
dm.dl.file_set( "recovery_score_data.pickle" )
dm.dl.file_set( "split_data.pickle" )

class UsersScore:
    def __init__( self ):
        self.data = {}
        self.function = {}
        self.key_list = []
        self.recovery_score_data = dm.dl.data_get( "recovery_score_data.pickle" )
        self.split_data = dm.dl.data_get( "split_data.pickle" )
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
                
    def set_data( self, key, data ):
        self.data[key] = data

    def data_clear( self ):
        self.data.clear()

    def get_score_dict( self ):
        score = {}

        for k in self.data.keys():      
            score[k] = self.function[k]( k )

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
