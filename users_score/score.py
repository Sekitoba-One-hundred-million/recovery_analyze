import json
from common.name import Name

data_name = Name()

class UsersScoreFunction:
    def __init__( self ):
        self.function = {}
        self.plus_score = {}
        self.minus_score = {}
        self.score_set()

    def score_set( self ):
        f = open( "plus_score.json", "r" )
        plus_score_instance = json.load( f )
        f.close()

        f = open( "minus_score.json", "r" )
        minus_score_instance = json.load( f )
        f.close()

        f = open( "use_score_data.json", "r" )
        plus_ga_use = json.load( f )
        f.close()

        for k in plus_ga_use.keys():
            #if not plus_ga_use[k]:
            #    continue

            self.plus_score[k] = plus_score_instance[k]
            self.minus_score[k] = minus_score_instance[k]
            
        self.use_data_write( list( self.plus_score.keys() ) )

    def use_data_write( self, key_list ):
        name_dict = {}
        print( "data count: {}".format( len( self.plus_score ) ) )
        f = open( "score_data_name.txt", "w" )
    
        for name in key_list:
            name = name.replace( "_minus", "" )
            name_dict[name] = True

        for name in name_dict.keys():
            f.write( name + "\n" )

        f.close()

    def age( self, score ):
        score = int( score )

        if score == 5:
            return 5

        if 7 <= score:
            return -5

        return 0

    def baba( self, score ):
        score = int( score )

        if score == 4:
            return 5

        return 0

    def before_continue_not_three_rank( self, score ):
        score = int( score )

        if 9 <= score:
            return -5

        return 5

    def before_diff( self, score ):
        score = int( score )

        if score == 2 or score == 7:
            return 5

        return 0

    def before_first_passing_rank( self, score ):
        score = int( score )

        if 14 <= score:
            return -5

        return 0

    def before_id_weight( self, score ):
        score = int( score )

        if score == -5:
            return -5

        return 0
    
    def before_last_passing_rank( self, score ):
        score = int( score )

        if score == 2:
            return 5

        if 13 <= score:
            return -5

        return 0

    def before_popular( self, score ):
        score = int( score )

        if 3 <= score and score <= 6:
            return 5

        if 15 <= score:
            return -5

        return 0
    
    def before_rank( self, score ):
        score = int( score )
        
        if score == 4:
            return 5

        if 13 <= score:
            return -5

        return 0

    def before_speed( self, score ):
        score = int( score )

        if 66 <= score:
            return -5

        return 0

    def burden_weight( self, score ):
        score = int( score )

        if score == 6:
            return 5

        if score == 1:
            return -5
        
        return 0
     
    def father_blood_type( self, score ):
        score = int( score )

        if score == 15:
            return 5

        if score == 12 or score == 23:
            return -5

        return 0
    
    def foot_used( self, score ):
        score = int( score )

        if score == 3 or score == 4:
            return 5

        if 11 <= score:
            return -5

        return 0

    def horce_sex( self, score ):
        score = int( score )

        if score == 2:
            return -5

        return 0

    def horce_sex_month( self, score ):
        score = int( score )

        if score == 31:
            return 5

        return 0

    def jockey_rank( self, score ):
        score = int( score )

        if score == 7:
            return 5

        if 9 <= score:
            return -5

        return 0

    def jockey_year_rank( self, score ):
        score = int( score )

        if score == 2:
            return 5

        if 10 <= score:
            return -5

        return 0

    def level_score( self, score ):
        score = int( score )

        if score == 5:
            return 5

        if score == 0:
            return -5

        return 0

    def limb( self, score ):
        score = int( score )

        if score == 1:
            return 5

        if score == 6 or score == 7 or score == 8:
            return -5

        return 0

    def match_rank( self, score ):
        score = int( score )
        
        if score == 6:
            return 5

        if 11 <= score:
            return -5

        return 0

    def my_limb_count( self, score ):
        score = int( score )

        if score == 2 or score == 3 or score == 4:
            return 5        

        if score == 7 or score == 8:
            return -5

        return 0

    def omega( self, score ):
        score = int( score )

        if 17 <= score and score <= 19:
            return 5

        if score <= 11:
            return -5

        return 0

    def popular_rank( self, score ):
        score = int( score )

        if score == 3 or score == 7:
            return 5

        return 0

    def race_deployment( self, score ):
        score = int( score )

        if score == 7:
            return 5

        return 0

    def race_interval( self, score ):
        score = int( score )

        if score == 10 or score == 11:
            return 5

        if 0 <= score and score <= 3:
            return -5

        return 0

    def race_level_check( self, score ):
        score = int( score )

        if score == 4:
            return 5

        if 13 <= score and score < 100:
            return -5

        return 0

    def race_money( self, score ):
        score = int( score )

        if score == 4:
            return 5

        return 0

    def race_num( self, score ):
        score = int( score )

        if score == 3 or score == 10:
            return 5

        return 0

    def speed_index( self, score ):
        score = int( score )

        if score == 1:
            return 5

        if 11 <= score:
            return -5

        return 0

    def straight_flame( self, score ):
        score = int( score )
        
        if score == 101 or score == 103 or score == 202:
            return 5

        return 0

    def straight_slope( self, score ):
        score = int( score )

        if score == 2 or score == 3:
            return 5

        return 0

    def train_score( self, score ):
        score = int( score )

        if score == 1:
            return 5

        return 0

    def trainer_rank( self, score ):
        score = int( score )

        if score == 6:
            return 5

        if 8 <= score and score <= 10:
            return -5

        return 0

    def weight( self, score ):
        score = int( score )

        if score == 50 or score == 51:
            return 5

        if score < 45:
            return -5

        return 0

    def weather( self, score ):
        score = int( score )
        
        if score == 3:
            return 5

        return 0

    def trainer_true_skill( self, score ):
        score = int( score )

        if 34 <= score and score <= 36:
            return 5

        if score <= 17:
            return -5

        return 0

    def up3_standard_value( self, score ):
        score = int( score )

        if score == 4 or score == 7:
            return 5

        if 10 <= score:
            return -5

        return 0
