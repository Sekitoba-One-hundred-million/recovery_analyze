from common.name import Name

data_name = Name()

class UsersScore:
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
        self.function[data_name.id_weight] = self.id_weight
        self.function[data_name.before_id_weight] = self.before_id_weight
        self.function[data_name.omega] = self.omega
        self.function[data_name.before_speed] = self.before_speed

        print( "data count: {}".format( len( self.function ) ) )

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

    def id_weight( self, score ):
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
