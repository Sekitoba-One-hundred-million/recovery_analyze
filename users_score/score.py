from common.name import Name

data_name = Name()

class UsersScoreFunction:
    def __init__( self ):
        self.function = {}

    def set_function( self ):
        self.function[data_name.before_rank] = self.before_rank
        self.function[data_name.race_level_check] = self.race_level_check
        self.function[data_name.straight_slope] = self.straight_slope
        self.function[data_name.foot_used] = self.foot_used
        self.function[data_name.limb] = self.limb
        self.function[data_name.age] = self.age
        self.function[data_name.speed_index] = self.speed_index
        self.function[data_name.race_interval] = self.race_interval
        self.function[data_name.weight] = self.weight
        self.function[data_name.before_id_weight] = self.before_id_weight
        self.function[data_name.omega] = self.omega
        self.function[data_name.before_speed] = self.before_speed
        self.function[data_name.popular] = self.popular
        self.function[data_name.trainer_rank] = self.trainer_rank
        self.function[data_name.jockey_rank] = self.jockey_rank
        self.function[data_name.popular_rank] = self.popular_rank
        self.function[data_name.before_diff] = self.before_diff
        self.function[data_name.limb_horce_number] = self.limb_horce_number
        self.function[data_name.father_rank] = self.father_rank
        self.function[data_name.mother_rank] = self.mother_rank
        self.function[data_name.match_rank] = self.match_rank
        
        self.use_data_write()
        print( "data count: {}".format( len( self.function ) ) )

    def use_data_write( self ):
        f = open( "score_data_name.txt", "w" )
        for name in self.function.keys():
            f.write( name + "\n" )

        f.close()

    def before_rank( self, score ):
        score = int( score )
        
        if score == 4:
            return 5

        if score == 8:
            return 5

        return 0

    def race_level_check( self, score ):
        score = int( score )

        if score == 3 or score == 4 or score == 5:
            return 10

        return 0

    def straight_slope( self, score ):
        score = int( score )

        if score == 2 or score == 3:
            return 5

        if score == 4:
            return -5

        return 0

    def foot_used( self, score ):
        score = int( score )
        
        if score == 41:
            return 5

        return 0

    def limb( self, score ):
        score = int( score )

        if score == 3:
            return 10

        #if 6 < score:
        #    return -5

        return 0

    def age( self, score ):
        score = int( score )

        if score == 5:
            return 5

        return 0

    def speed_index( self, score ):
        score = int( score )

        if score == 3:
            return 5
        elif score == 2:
            return -10

        return 0

    def race_interval( self, score ):
        score = int( score )

        if score < 3:
            return -5
        if score == 10:
            return 5

        return 0

    def weight( self, score ):
        score = int( score )

        if score == 50 or score == 51:
            return 5

        if score < 45:
            return -5

        return 0
    
    def before_id_weight( self, score ):
        score = int( score )

        if score == -5:
            return -5

        return 0

    def omega( self, score ):
        score = int( score )

        if score == 17:
            return 5

        if score < 12:
            return -10

        return 0

    def before_speed( self, score ):
        score = int( score )

        if score == 55:
            return 5

        if 64 < score:
            return -5

        return 0

    def popular( self, score ):
        score = int( score )

        if score == 5 or score == 6 or score == 7:
            return 5

        if 11 < score:
            return -5
        
        return 0

    def trainer_rank( self, score ):
        score = int( score )

        if score == 4:
            return 10

        if 8 < score:
            return -5

        return 0

    def jockey_rank( self, score ):
        score = int( score )

        if score == 4:
            return 5

        if 9 < score:
            return -5

        return 0

    def popular_rank( self, score ):
        score = int( score )

        if score == 6:
            return 5

        if score == 0:
            return -5

        return 0

    def before_diff( self, score ):
        score = int( score )

        if score == 8:
            return 5

        if score == 9 or score == 10:
            return -5

        return 0

    def limb_horce_number( self, score ):
        score = int( score )
        
        if score == 208 or score == 304 or score == 306:
            return 5

        if score == 305:
            return 10

        if score == 201 or score == 600:
            return -5

        return 0

    def father_rank( self, score ):
        score = int( score )

        if score == 2 or score == 3:
            return 5
        
        if score == 6 or score == 7:
            return -5

        return 0

    def mother_rank( self, score ):
        score = int( score )
        
        if score == 4 or score == 5:
            return 5

        if score == 12:
            return -5
        
        return 0

    def match_rank( self, score ):
        score = int( score )
        
        if score == 3:
            return 5
        
        if 9 < score:
            return -5

        return 0    
