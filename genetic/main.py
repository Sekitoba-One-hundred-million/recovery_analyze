import sys
import json
import math
import copy
import random
from tqdm import tqdm

import sekitoba_library as lib
import sekitoba_data_manage as dm

from genetic_algorithm import GA

DATA = "data"
COUNT = "count"
MIN_COUNT = 15000

def genetic_score_create( learn_data, users_rank_data, users_odds_data, check_data ):
    check_recovery = 1.05
    genetic_score_ensemble_count = 200
    genetic_score_ensemble_rate = 0
    genetic_score_ensemble_rate = 0.05
        
    best_data = []
    users_score_data_list = []
    users_score_key = {}
    
    recovery_data = {}
    score_key_data = {}

    for race_id in learn_data.keys():
        year = race_id[0:4]
        lib.dic_append( recovery_data, year, {} )
        for horce_id in learn_data[race_id].keys():
            score = 0

            for sk in learn_data[race_id][horce_id].keys():
                if check_data[sk]:
                    score += learn_data[race_id][horce_id][sk]

            score_key = str( int( score ) )
            lib.dic_append( recovery_data[year], score_key, { DATA: 0, COUNT: 0 } )
            recovery_data[year][score_key][COUNT] += 1
            score_key_data[score_key] = int( score )

            if users_rank_data[race_id][horce_id] == 1:
                recovery_data[year][score_key][DATA] += users_odds_data[race_id][horce_id]
            
    for year in recovery_data.keys():
        for score_key in recovery_data[year].keys():
            recovery_data[year][score_key][DATA] /= recovery_data[year][score_key][COUNT]

    score_values = list( score_key_data.keys() )

    for i in range( 0, len( score_values ) ):
        score_values[i] = int( score_values[i] )

    score_values = sorted( score_values, reverse = True )
    instance_recovery_data = {}
    best_score = -100
    best_recovery = -100
    best_score_key = ""
    
    for score in score_values:
        score_key = str( int( score ) )
        current_recovery_list = []        
        #score_recovery_data[key_score] = { DATA: 0, COUNT: 0 }
        count = 0

        for year in recovery_data.keys():
            lib.dic_append( instance_recovery_data, year, { DATA: 0, COUNT: 0 } )
            
            if not score_key in recovery_data[year]:
                continue

            instance_recovery_data[year][DATA] += recovery_data[year][score_key][DATA] * recovery_data[year][score_key][COUNT]
            instance_recovery_data[year][COUNT] += recovery_data[year][score_key][COUNT]
            current_recovery_list.append( instance_recovery_data[year][DATA] / instance_recovery_data[year][COUNT] )
            count += instance_recovery_data[year][COUNT]

        if len( current_recovery_list ) == 0:
            continue

        if count < MIN_COUNT:
            continue

        conv_recovery = 0
        ave_recovery = sum( current_recovery_list ) / len( current_recovery_list )

        for cr in current_recovery_list:
            conv_recovery += math.pow( ave_recovery - cr, 2 )

        conv_recovery = math.sqrt( conv_recovery ) / len( current_recovery_list )
        recovery_score = ave_recovery - conv_recovery
        #print( score_values[0], score_key, ave_recovery, conv_recovery )

        if best_score < recovery_score:
            best_score = recovery_score
            best_score_key = score_key
            best_recovery = round( ave_recovery, 2 )
    
    return best_score, best_score_key, best_recovery

def pm_score_get( users_score_data ):
    users_score_pm_data = {}
    f = open( "plus_score.json", "r" )
    plus_score = json.load( f )
    f.close()

    f = open( "minus_score.json", "r" )
    minus_score = json.load( f )
    f.close()

    for race_id in users_score_data.keys():
        users_score_pm_data[race_id] = {}
        for horce_id in users_score_data[race_id].keys():
            users_score_pm_data[race_id][horce_id] = {}

            for score_key in users_score_data[race_id][horce_id].keys():
                users_score_pm_data[race_id][horce_id][score_key] = 0

                if users_score_data[race_id][horce_id][score_key] in plus_score[score_key]:
                    users_score_pm_data[race_id][horce_id][score_key] = 1

                if users_score_data[race_id][horce_id][score_key] in minus_score[score_key]:
                    users_score_pm_data[race_id][horce_id][score_key] = -1

    return users_score_pm_data

def main():
    N = 100
    population = 20
    ensemble_count = 1

    users_data = dm.pickle_load( "users_data.pickle" )
    users_rank_data = dm.pickle_load( "users_rank_data.pickle" )
    users_odds_data = dm.pickle_load( "users_odds_data.pickle" )
    best_key_data = {}
    learn_data = {}
    test_data = {}

    users_score_plus_data = pm_score_get( users_data )
    
    for race_id in users_score_plus_data.keys():
        year = race_id[0:4]

        if year in lib.test_years:
            test_data[race_id] = copy.deepcopy( users_score_plus_data[race_id] )
        else:
            learn_data[race_id] = copy.deepcopy( users_score_plus_data[race_id] )

    instance_race_id = list( users_data.keys() )[0]
    instance_horce_id = list( users_data[instance_race_id].keys() )[0]
    score_key_list = list( users_data[instance_race_id][instance_horce_id].keys() )
    best_users_rate_data = {}
    users_score_rate_list = []

    ga = GA( population, score_key_list )
    
    for n in range( 0, N ):
        score_list = []
        recovery_list = []

        for i in range( 0, ga.population ):
            score, key, recovery = genetic_score_create( learn_data, \
                                               users_rank_data, \
                                               users_odds_data, \
                                               ga.parent[i] )
            score_list.append( score )
            #print( score, recovery )

        ga.scores_set( score_list )
        ga.next_genetic()
        print( "{}: best_score:{}".format( n + 1, ga.best_score ) )

    print( ga.best_score )
    print( len( ga.best_population ) )
    print( ga.best_population )
    f = open( "use_score_data.json", "w" )
    json.dump( ga.best_population, f, indent = 4 )
    f.close()

    print( genetic_score_create( learn_data, \
                                users_rank_data, \
                                users_odds_data, \
                                ga.best_population ) )
    print( genetic_score_create( test_data, \
                                users_rank_data, \
                                users_odds_data, \
                                ga.best_population ) )

if __name__ == "__main__":
    main()
