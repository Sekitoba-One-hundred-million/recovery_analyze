import random

import SekitobaLibrary as lib
from SekitobaLibrary import ManageRecoveryScore

def main( learn_data, manage_recovery_score: ManageRecoveryScore, recovery_len = 30, escape_year_list = lib.test_years ):
    N = 3
    win_count = 0
    recovery_data = []
    data_type = learn_data["type"]
    learn_index_list = list( range( 0, len( learn_data["standardization"] ) ) )
    random.shuffle( learn_index_list )

    for i in learn_index_list:
        if learn_data["year"][i] in escape_year_list:
            continue

        current_standardization = learn_data["standardization"][i]
        current_teacher = learn_data["teacher"][i]
        current_answer = learn_data["answer"][i]
        current_odds = learn_data["odds"][i]
        current_score_list = [ 0 for _ in range( len( current_standardization ) ) ]

        for name in manage_recovery_score.data_name_list:
            data_index = manage_recovery_score.data_name_list.index( name )
            
            for r in range( 0, len( current_standardization ) ):
                if data_type[name] == float:
                    current_score_list[r] += manage_recovery_score.check_score( current_standardization[r][data_index], name )
                elif data_type[name] == int:
                    current_score_list[r] += manage_recovery_score.check_score( current_teacher[r][data_index], name )

        check_data = []

        for i in range( 0, len( current_answer ) ):
            check_data.append( { "rank": current_answer[i], \
                                 "score": current_score_list[i], \
                                 "odds": current_odds[i] } )

        if len( check_data ) < 5:
            continue

        recovery = 0
        check_data.sort( key = lambda x:x["score"], reverse = True )

        for r in range( 0, N ):
            if check_data[r]["rank"] == 1:
                win_count += 1
                recovery = check_data[r]["odds"]
                break

        recovery_data.append( recovery )

    score = 100
    recovery_list = []
    
    for i in range( 0, 100 ):
        cut_count = int( len( recovery_data ) / recovery_len )
        random.shuffle( recovery_data )

        for r in range( 0, recovery_len ):
            s1 = int( r * cut_count )
            s2 = int( s1 + cut_count )
            recovery_list.append(
                sum( recovery_data[s1:s2] ) / ( len( recovery_data[s1:s2] ) * N ) )

        current_recovery = 0
        c = int( recovery_len / 5 )

        for r in range( 0, c ):
            current_recovery += recovery_list[r]

        score = min( score, current_recovery / c )
        recovery_list.clear()

    print( sum( recovery_data ) / ( len( recovery_data ) * N ) )

    return score

def test_simu( simu_data, manage_recovery_score_list: list[ ManageRecoveryScore ], test_years = lib.simu_years ):
    recovery = 0
    win_count = 0
    count = 0
    N = 3
    #print( len( simu_data.keys() ) )
    for race_id in simu_data.keys():
        year = race_id[0:4]

        if not year in test_years:
            continue

        predict_data = {}
        instance_manage_recovery_score = manage_recovery_score_list[0]
        
        for horce_id in simu_data[race_id].keys():
            for name in instance_manage_recovery_score.data_name_list:
                lib.dic_append( predict_data, name, [] )
                data_index = instance_manage_recovery_score.data_name_list.index( name )
                predict_data[name].append( simu_data[race_id][horce_id]["data"][data_index] )

        for name in instance_manage_recovery_score.data_name_list:
            if instance_manage_recovery_score.data_type[name] == float:
                predict_data[name] = lib.standardization( predict_data[name], abort = [ lib.escapeValue ] )

        c = 0
        score_list = []

        for horce_id in simu_data[race_id].keys():
            score = 0

            for manage_recovery_score in manage_recovery_score_list:
                for name in manage_recovery_score.data_name_list:
                    score += manage_recovery_score.check_score( predict_data[name][c], name )

            c += 1
            score_list.append( { "rank": simu_data[race_id][horce_id]["answer"]["rank"],
                                 "odds": simu_data[race_id][horce_id]["answer"]["odds"],
                                 "score": score } )

        if len( score_list ) < 5:
            continue

        score_list.sort( key=lambda x:x["score"], reverse = True )
        count += N

        for i in range( 0, N ):
            if score_list[i]["rank"] == 1:
                win_count += 1
                recovery += score_list[i]["odds"]
                break

    #win_rate = ( win_count / count ) * N
    #print( "count: {}".format( count ) )
    #print( "win_rate: {}".format( win_rate ) )

    return recovery / count
