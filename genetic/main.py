import sys
import copy
import random
from mpi4py import MPI
from tqdm import tqdm

import sekitoba_library as lib
import sekitoba_data_manage as dm

import test
from simulation import Simulation
from genetic_algorithm import GA

comm = MPI.COMM_WORLD   #COMM_WORLDは全体
size = comm.Get_size()  #サイズ（指定されたプロセス（全体）数）
rank = comm.Get_rank()  #ランク（何番目のプロセスか。プロセスID）
name = MPI.Get_processor_name() #プロセスが動いているノードのホスト名

def key_list_get():
    key_list = []
    test_key_list = []
    race_data = dm.dl.data_get( "race_data.pickle" )

    for k in race_data.keys():
        race_id = lib.id_get( k )
        year = race_id[0:4]

        if year in lib.test_years:
            test_key_list.append( k )
        else:
            key_list.append( k )

    return key_list, test_key_list

def score_create( learn_data, rate_data, kind, test = False ):
    si = Simulation()
    analyze_data = si.simulation( learn_data, rate_data, kind, test = test )
    check_recovery = 1.05
    genetic_score_ensemble_count = 200
    genetic_score_ensemble_rate = 0

    if kind == "one":
        genetic_score_ensemble_rate = 0.05
    elif kind == "quinella":
        genetic_score_ensemble_rate = 0.05
        
    best_data = []
    users_score_data_list = []
    users_score_key = {}
    
    for sec in range( genetic_score_ensemble_count ):
        recovery_data = {}
        
        for year in analyze_data.keys():
            for data in analyze_data[year]:
                if random.random() < genetic_score_ensemble_rate:
                    key_score = str( int( data["score"] ) )
                    lib.dic_append( recovery_data, key_score, { "money": 0, "count": 0 } )
                    recovery_data[key_score]["money"] += data["odds"]
                    recovery_data[key_score]["count"] += 1

        recovery_key_list = list( recovery_data.keys() )
        
        for i in range( 0, len( recovery_key_list ) ):
            recovery_key_list[i] = int( recovery_key_list[i] )
        
        get_money = 0
        count = 0
        users_score_data = {}
        recovery_key_list.sort( reverse = True )

        for users_score in recovery_key_list:
            key_score = str( users_score )
            get_money += recovery_data[key_score]["money"]
            count += recovery_data[key_score]["count"]
            score_recovery = get_money / count
            score = get_money - count
            users_score_data[key_score] = { "recovery": score_recovery, "score": score }
            users_score_key[key_score] = True

        users_score_data_list.append( users_score_data )

    best_score = 0
    best_key = ""
    best_one = 0

    for score_key in users_score_key.keys():
        check_data = []
        current_best_score = 0
        current_best_key = ""
        minus_score = 0
        minus_count = 0
        
        for users_score_data in users_score_data_list:
            if score_key in users_score_data.keys():
                if check_recovery < users_score_data[score_key]["recovery"]:
                    check_data.append( users_score_data[score_key] )
                else:
                    minus_score += min( 0, users_score_data[score_key]["score"] )

        check_clear_count = len( check_data )

        if check_clear_count == 0:
            continue

        #minus_score /= check_clear_count
        current_best_key = score_key
            
        if check_clear_count == 1:
            current_best_score = check_data[0]["score"]
        else:
            check_data = sorted( check_data, key=lambda x:x["score"] )
            ave_score = 0
            median_score = 0

            if check_clear_count % 2 == 1:
                median_index = int( check_clear_count / 2 )
                median_score = check_data[median_index]["score"]
            else:
                median_index_1 = int( check_clear_count / 2 )
                median_index_2 = int( check_clear_count / 2 - 1 )
                median_score = int( ( check_data[median_index_1]["score"] + check_data[median_index_2]["score"] ) / 2 )

            for i in range( 0, check_clear_count ):
                ave_score += check_data[i]["score"]

            ave_score /= check_clear_count
            #current_best_score = ( ave_score + median_score ) / 2
            current_best_score = median_score
            current_best_score -= abs( median_score - ave_score )

        if not  check_clear_count == genetic_score_ensemble_count:
           minus_score /= ( genetic_score_ensemble_count - check_clear_count ) 
            
        minus_score *= ( genetic_score_ensemble_count - check_clear_count ) / genetic_score_ensemble_count
        minus_rate = pow( check_clear_count / genetic_score_ensemble_count, 2 )
        #current_best_score *= check_clear_count
        #print( current_best_score, minus_score )
        current_best_score += minus_score
        #current_best_score /= genetic_score_ensemble_count
        current_best_score = current_best_score * minus_rate
        
        if best_score < current_best_score:
            best_score = current_best_score
            best_key = current_best_key
            best_one = check_clear_count
        
    #print( best_data )
    return best_score, best_key, best_one

def best_rate_data_create( rate_data_list ):
    result = {}

    for rate_data in rate_data_list:
        for k in rate_data.keys():
            lib.dic_append( result, k, 0 )
            result[k] += rate_data[k]

    for k in result.keys():
        result[k] /= len( rate_data_list )

    return result

def operater_ga_analyze( ga: GA ):
    score_list = []
    one_list = []
    s = int( ga.population / ( size - 1 ) )
    
    for r in range( 1, size ):
        s1 = s * ( r - 1 )
        s2 = s1 + s
        comm.send( ga.parent[s1:s2], dest = r, tag = 0 )

    for r in range( 1, size ):
        instance_score = comm.recv( source = r, tag = 1 )
        instance_one = comm.recv( source = r, tag = 2 )
        score_list.extend( instance_score )
        one_list.extend( instance_one )

    return score_list, one_list

def sub_process_ga_analyze( ticket_kind, learn_data ):
    parents = comm.recv( source = 0, tag = 0 )
    instance_score_list = []
    instance_one_list = []
                    
    for parent in parents:
        score, best_key, one = score_create( learn_data, parent, ticket_kind )
        instance_score_list.append( score )
        instance_one_list.append( one )
        print( "score:{} best_key_score:{}, one:{}".format( score, best_key, one ) )

    comm.send( instance_score_list, dest = 0, tag = 1 )
    comm.send( instance_one_list, dest = 0, tag = 2 )

def users_score_test( test_data, learn_data, best_users_score_rate, best_key_data, use_buy_key ):
    if not rank == 0:
        return
        
    print( "test start" )
    test.main( test_data, best_users_score_rate, best_key_data, use_buy_key, "test" )
    test.main( learn_data, best_users_score_rate, best_key_data, use_buy_key, "learn" )

    users_score_rate_upload = "y"#input( "users_score_rate upload(y/n): " )

    if users_score_rate_upload == "y":
        users_score_rate_data = dm.pickle_load( "users_score_rate.pickle" )
        users_best_key = dm.pickle_load( "users_best_key.pickle" )

        if users_score_rate_data == None:
            users_score_rate_data = {}
            
        if users_best_key == None:
            users_best_key = {}

        for k in best_users_score_rate.keys():
            users_score_rate_data[k] = best_users_score_rate[k]
            users_best_key[k] = best_key_data[k]
            
        dm.pickle_upload( "users_score_rate.pickle", users_score_rate_data )
        dm.pickle_upload( "users_best_key.pickle", users_best_key )

def main():
    N = 250
    population = 20
    ensemble_count = 1

    use_buy_key = []
    use_buy_key.append( "one" )
    #use_buy_key.append( "quinella" )
    #use_buy_key.append( "wide" )
    #use_buy_key.append( "triple" )

    users_score_data = dm.pickle_load( "users_score_data.pickle" )
    best_key_data = {}
    learn_data = {}
    test_data = {}
    
    for race_id in users_score_data.keys():
        year = race_id[0:4]

        if year in lib.test_years:
            test_data[race_id] = copy.deepcopy( users_score_data[race_id] )
        else:
            learn_data[race_id] = copy.deepcopy( users_score_data[race_id] )

    ga_update = ""

    if rank == 0:
        ga_update = "y"#input( "ga update(y/n): " )
        
        for r in range( 1, size ):
            comm.send( ga_update, dest = r, tag = 0 )
    else:
        ga_update = comm.recv( source = 0, tag = 0 )

    if ga_update == "y":
        first_key = list( learn_data.keys() )[0]
        next_key = list( learn_data[first_key].keys() )[0]
        elements_key_list = list( learn_data[first_key][next_key].keys() )
        best_users_rate_data = {}
        
        for k in use_buy_key:
            users_score_rate_list = []
            
            for t in range( ensemble_count ):
                ga = GA( population, elements_key_list )
                ga.set_ticket_kind( k )
    
                for n in range( 0, N ):
                    score_list = []
                    one_list = []

                    if rank == 0:
                        print( "kind:{} num:{}".format( k, n ) )
                        score_list, one_list = operater_ga_analyze( ga )
                    else:
                        sub_process_ga_analyze( k, learn_data )
                        
                    if rank == 0:
                        ga.scores_set( score_list, one_list )
                        ga.next_genetic()
                        print( "best_score:{} best_one:{}\n".format( ga.best_score, ga.best_one ) )

                if rank == 0:
                    users_score_rate_list.append( copy.deepcopy( ga.best_population ) )

            if rank == 0:    
                best_users_rate_data[k] = best_rate_data_create( users_score_rate_list )
                _ , best_key, _ = score_create( learn_data, best_users_rate_data[k], k )
                best_key_data[k] = best_key

        users_score_test( test_data, learn_data, best_users_rate_data, best_key_data, use_buy_key )
            
    if not rank == 0:
        sys.exit()    

if __name__ == "__main__":
    main()
