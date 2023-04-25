from common.name import Name

data_name = Name()

class UsersScoreFunction:
    def __init__( self ):
        self.function = {}

    def set_function( self, write = True ):
        self.function[data_name.before_rank] = self.before_rank
        self.function[data_name.before_rank_minus] = self.before_rank_minus
        self.function[data_name.race_level_check] = self.race_level_check
        self.function[data_name.race_level_check_minus] = self.race_level_check_minus
        self.function[data_name.straight_slope] = self.straight_slope
        self.function[data_name.foot_used] = self.foot_used
        self.function[data_name.limb] = self.limb
        self.function[data_name.age] = self.age
        self.function[data_name.speed_index] = self.speed_index
        self.function[data_name.race_interval] = self.race_interval
        self.function[data_name.weight] = self.weight
        self.function[data_name.weight_minus] = self.weight_minus
        self.function[data_name.before_id_weight] = self.before_id_weight
        self.function[data_name.omega] = self.omega
        self.function[data_name.before_speed_minus] = self.before_speed_minus
        self.function[data_name.trainer_rank] = self.trainer_rank
        self.function[data_name.trainer_rank_minus] = self.trainer_rank_minus
        self.function[data_name.jockey_rank] = self.jockey_rank
        self.function[data_name.jockey_rank_minus] = self.jockey_rank_minus
        self.function[data_name.before_diff] = self.before_diff
        self.function[data_name.limb_horce_number] = self.limb_horce_number
        self.function[data_name.limb_horce_number_minus] = self.limb_horce_number_minus
        self.function[data_name.mother_rank] = self.mother_rank
        self.function[data_name.match_rank] = self.match_rank
        self.function[data_name.match_rank_minus] = self.match_rank_minus
        self.function[data_name.weather] = self.weather
        self.function[data_name.burden_weight] = self.burden_weight
        self.function[data_name.before_continue_not_three_rank] = self.before_continue_not_three_rank
        self.function[data_name.before_continue_not_three_rank_minus] = self.before_continue_not_three_rank_minus
        self.function[data_name.horce_sex] = self.horce_sex
        self.function[data_name.horce_sex_month] = self.horce_sex_month
        self.function[data_name.dist_kind_count_minus] = self.dist_kind_count_minus
        self.function[data_name.before_popular] = self.before_popular
        self.function[data_name.before_last_passing_rank] = self.before_last_passing_rank
        self.function[data_name.before_last_passing_rank_minus] = self.before_last_passing_rank_minus
        self.function[data_name.before_first_passing_rank] = self.before_first_passing_rank
        self.function[data_name.jockey_year_rank] = self.jockey_year_rank
        self.function[data_name.money] = self.money
        self.function[data_name.horce_num] = self.horce_num
        self.function[data_name.baba] = self.baba
        self.function[data_name.place] = self.place
        self.function[data_name.popular_rank] = self.popular_rank
        self.function[data_name.train_score] = self.train_score
        self.function[data_name.race_deployment] = self.race_deployment
        self.function[data_name.up3_standard_value] = self.up3_standard_value
        self.function[data_name.up3_standard_value_minus] = self.up3_standard_value_minus
        self.function[data_name.my_limb_count] = self.my_limb_count
        self.function[data_name.my_limb_count_minus] = self.my_limb_count_minus
        self.function[data_name.horce_true_skill] = self.horce_true_skill        
        self.function[data_name.father_blood_type] = self.father_blood_type
        self.function[data_name.father_blood_type_minus] = self.father_blood_type_minus
        self.function[data_name.jockey_true_skill] = self.jockey_true_skill
        self.function[data_name.jockey_true_skill_minus] = self.jockey_true_skill_minus
        self.function[data_name.trainer_true_skill] = self.trainer_true_skill
        self.function[data_name.trainer_true_skill_minus] = self.trainer_true_skill_minus
        self.function[data_name.horce_jockey_true_skill_index] = self.horce_jockey_true_skill_index
        self.function[data_name.diff_load_weight] = self.diff_load_weight
        self.function[data_name.straight_flame] = self.straight_flame
        self.function[data_name.race_num] = self.race_num
        self.function[data_name.race_money] = self.race_money

        if write:
            self.use_data_write( list( self.function.keys() ) )

    def use_data_write( self, key_list ):
        name_dict = {}
        print( "data count: {}".format( len( self.function ) ) )
        f = open( "score_data_name.txt", "w" )
    
        for name in key_list:
            name = name.replace( "_minus", "" )
            name_dict[name] = True

        for name in name_dict.keys():
            f.write( name + "\n" )

        f.close()

    def before_rank( self, score ):
        score = int( score )
        
        if score == 4 or score == 7 or score == 8:
            return 5

        return 0

    def before_rank_minus( self, score ):
        score = int( score )
        
        if 14 < score:
            return -5
        return 0

    def race_level_check( self, score ):
        score = int( score )

        if score == 3 or score == 4 or score == 6 or score == 8:
            return 5

        return 0
    
    def race_level_check_minus( self, score ):
        score = int( score )
        
        if 14 < score and score < 100:
            return -5

        return 0

    def straight_slope( self, score ):
        score = int( score )

        if score == 2:
            return 5

        return 0

    def foot_used( self, score ):
        score = int( score )

        if score == 4:
            return 10

        return 0

    def limb( self, score ):
        score = int( score )

        if score == 3:
            return 5

        return 0

    def age( self, score ):
        score = int( score )

        if score == 5:
            return 5

        return 0

    def speed_index( self, score ):
        score = int( score )

        if score == 1 or score == 2 or score == 3 or score == 4:
            return 5

        return 0

    def race_interval( self, score ):
        score = int( score )

        if score == 10:
            return 5

        return 0
    
    def weight( self, score ):
        score = int( score )

        if score == 50:
            return 5

        return 0

    def weight_minus( self, score ):
        score = int( score )

        if score < 45:
            return -5

        return 0
    
    def before_id_weight( self, score ):
        score = int( score )

        if score == -2:
            return 5

        return 0

    def omega( self, score ):
        score = int( score )

        if score == 17:
            return 5

        return 0

    def before_speed_minus( self, score ):
        score = int( score )

        if 65 < score:
            return -5

        return 0

    def trainer_rank( self, score ):
        score = int( score )

        if score == 5 or score == 6:
            return 5

        return 0

    def trainer_rank_minus( self, score ):
        score = int( score )

        if 8 < score:
            return -5

        return 0

    def jockey_rank( self, score ):
        score = int( score )

        if score == 7:
            return 5

        return 0

    def jockey_rank_minus( self, score ):
        score = int( score )

        if 9 < score:
            return -5

        return 0

    def before_diff( self, score ):
        score = int( score )

        if score == 7 or score == 8:
            return 5

        return 0

    def limb_horce_number( self, score ):
        score = int( score )
        
        if score == 304 or score == 305 or score == 306:
            return 5

        return 0

    def limb_horce_number_minus( self, score ):
        score = int( score )

        if score == 300 or score == 600:
            return -5

        return 0

    def mother_rank( self, score ):
        score = int( score )
        
        if score == 4:
            return 5

        return 0

    def match_rank( self, score ):
        score = int( score )
        
        if score == 6:
            return 5

        return 0

    def match_rank_minus( self, score ):
        score = int( score )
        
        if 10 < score:
            return -5

        return 0

    def weather( self, score ):
        score = int( score )
        
        if score == 3:
            return 5

        return 0

    def burden_weight( self, score ):
         score = int( score )

         if score == 6:
             return 5

         return 0

    def before_continue_not_three_rank( self, score ):
        score = int( score )

        if score == 6:
            return 5

        return 5

    def before_continue_not_three_rank_minus( self, score ):
        score = int( score )

        if score == 10:
            return -5

        return 0

    def horce_sex( self, score ):
        score = int( score )

        if score == 0:
            return 5

        return 0

    def horce_sex_month( self, score ):
        score = int( score )

        if score == 11 or score == 31:
            return 5

        return 0

    def dist_kind_count_minus( self, score ):
        score = int( score )

        if score == 20:
            return -5

        return 0

    def before_popular( self, score ):
        score = int( score )

        if score == 5 or score == 6 or score == 9:
            return 5

        return 0

    def before_last_passing_rank( self, score ):
        score = int( score )

        if score == 2 or score == 3:
            return 5

        return 0

    def before_last_passing_rank_minus( self, score ):
        score = int( score )

        if score == 17 or score == 18:
            return -5

        return 0

    def before_first_passing_rank( self, score ):
        score = int( score )

        if score == 2 or score == 3:
            return 5

        return 0

    def jockey_year_rank( self, score ):
        score = int( score )

        if score == 2:
            return 5

        return 0

    def money( self, score ):
        score = int( score )

        if score == 13 or score == 18:
            return 5

        return 0

    def horce_num( self, score ):
        score = int( score )

        if score == 4 or score == 10 or score == 14:
            return 5

        return 0

    def baba( self, score ):
        score = int( score )

        if score == 4:
            return 5

        return 0

    def place( self, score ):
        score = int( score )

        if score == 3:
            return 5

        return 0

    def popular_rank( self, score ):
        score = int( score )

        if score == 3 or score == 7:
            return 5

        return 0

    def train_score( self, score ):
        score = int( score )

        if score == 1:
            return 5

        return 0

    def race_deployment( self, score ):
        score = int( score )

        if score == 7:
            return 5

        return 0

    def up3_standard_value( self, score ):
        score = int( score )

        if score == 4 or score == 7:
            return 5

        return 0

    def up3_standard_value_minus( self, score ):
        score = int( score )

        if 10 <= score:
            return -5

        return 0

    def my_limb_count( self, score ):
        score = int( score )

        if score == 2 or score == 3 or score == 4:
            return 5        

        return 0

    def my_limb_count_minus( self, score ):
        score = int( score )

        if score == 7 or score == 8:
            return -5

        return 0

    def horce_true_skill( self, score ):
        score = int( score )

        if score <= 41 and 36 <= score:
            return 5

        return 0

    def jockey_true_skill( self, score ):
        score = int( score )

        if score <= 34 and 31 <= score:
            return 5

        return 0

    def jockey_true_skill_minus( self, score ):
        score = int( score )

        if score < 20:
            return -5

        return 0

    def trainer_true_skill( self, score ):
        score = int( score )

        if 34 <= score and score <= 36:
            return 5

        return 0

    def trainer_true_skill_minus( self, score ):
        score = int( score )

        if score <= 17:
            return -5

        return 0

    def father_blood_type( self, score ):
        score = int( score )

        if score == 15 or score == 22:
            return 5

        return 0

    def father_blood_type_minus( self, score ):
        score = int( score )

        if score == 12 or score == 23:
            return -5

        return 0

    def horce_jockey_true_skill_index( self, score ):
        score = int( score )

        if score == 3:
            return 5

        return 0

    def diff_load_weight( self, score ):
        score = int( score )

        if score == -2:
            return 5

        return 0

    def straight_flame( self, score ):
        score = int( score )
        
        if score == 101 or score == 103 or score == 202:
            return 5

        return 0

    def race_num( self, score ):
        score = int( score )

        if score == 3 or score == 10:
            return 5

        return 0

    def race_money( self, score ):
        score = int( score )

        if score == 4:
            return 5

        return 0
