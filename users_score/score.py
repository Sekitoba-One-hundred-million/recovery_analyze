from common.name import Name

data_name = Name()

class UsersScoreFunction:
    def __init__( self ):
        self.function = {}
        self.plus_score = {}

        self.plus_score[data_name.age] = [2, 4, 5]
        self.plus_score[data_name.all_horce_num] = [8, 9, 10, 11]
        self.plus_score[data_name.baba] = [1]
        self.plus_score[data_name.before_rank] = [4, 6, 7]
        self.plus_score[data_name.before_continue_not_three_rank] = [5, 6, 7]
        self.plus_score[data_name.before_diff] = [2, 3, 7]
        self.plus_score[data_name.before_first_passing_rank] = [2, 3, 4, 5, 6]
        self.plus_score[data_name.before_id_weight] = [-2, -1]
        self.plus_score[data_name.before_last_passing_rank] = [1, 2, 3, 4, 6]
        self.plus_score[data_name.before_pace] = [0, 2]
        self.plus_score[data_name.before_popular] = [3, 6]
        self.plus_score[data_name.before_speed] = [58, 59, 61, 63]
        self.plus_score[data_name.best_weight] = [1, 3, 4, 5, 6, 11, 15, 16, 17, 18]
        self.plus_score[data_name.burden_weight] = [5, 6]
        self.plus_score[data_name.diff_load_weight] = [-2, 1, 2, 4]
        self.plus_score[data_name.dist_kind_count] = [2, 3, 6, 10, 14, 16]
        self.plus_score[data_name.father_blood_type] = [15, 18, 22, 34, 38, 42]
        self.plus_score[data_name.foot_used] = [1, 3, 4, 5, 6, 9]
        self.plus_score[data_name.horce_jockey_true_skill_index] = [1, 3, 5, 7, 9, 10, 13, 15]
        self.plus_score[data_name.horce_num] = [2, 4, 6, 8, 10, 14]
        self.plus_score[data_name.horce_sex] = [1]
        self.plus_score[data_name.horce_sex_month] = [11, 21, 31, 62, 72]
        self.plus_score[data_name.horce_true_skill] = [23, 26, 28, 30, 31, 32, 33]
        self.plus_score[data_name.jockey_true_skill] = [26, 33, 34, 35, 36]
        self.plus_score[data_name.jockey_rank] = [5, 6, 7]
        self.plus_score[data_name.jockey_year_rank] = [1, 2, 3]
        self.plus_score[data_name.level_score] = [3, 4]
        self.plus_score[data_name.limb] = [1, 3]
        self.plus_score[data_name.limb_horce_number] = [401, 402, 403, 404, 405, 602]
        self.plus_score[data_name.match_rank] = [1, 2, 3, 4, 6]
        self.plus_score[data_name.money] = [5, 7, 10, 11, 14, 16]
        self.plus_score[data_name.mother_rank] = [0, 4, 11]
        self.plus_score[data_name.my_limb_count] = [1, 3, 4, 5, 10]
        self.plus_score[data_name.omega] = [17, 18, 19]
        self.plus_score[data_name.place] = [3]
        self.plus_score[data_name.popular_rank] = [-11, -6, 3, 5, 6, 7, 8, 10, 11]
        self.plus_score[data_name.race_deployment] = [4, 7]
        self.plus_score[data_name.race_num] = [3, 11, 12]
        self.plus_score[data_name.race_money] = [3, 4]
        self.plus_score[data_name.race_interval] = [10, 11, 13, 14]
        self.plus_score[data_name.race_level_check] = [3, 4]
        self.plus_score[data_name.speed_index] = [0, 1, 4, 5, 9, 11, 12]
        self.plus_score[data_name.straight_flame] = [103, 202, 203]
        self.plus_score[data_name.straight_slope] = [1, 2]
        self.plus_score[data_name.three_average] = [7, 8, 11, 14, 15]
        self.plus_score[data_name.train_score] = [-4, -3, -2]
        self.plus_score[data_name.trainer_rank] = [5, 6]
        self.plus_score[data_name.trainer_true_skill] = [24, 29, 30, 31, 32, 33, 34]
        self.plus_score[data_name.up3_standard_value] = [-3, -2, -1, 1, 2, 3, 7]
        self.plus_score[data_name.weather] = [1]
        self.plus_score[data_name.weight] = [50, 51, 53]
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
