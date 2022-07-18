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
    genetic_score_ensemble_count = 20
    genetic_score_ensemble_rate = 0.2
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
            users_score_data[key_score] = { "recovery": score_recovery, "score": count }
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
                    minus_score += users_score_data[score_key]["score"]

        check_clear_count = len( check_data )

        if check_clear_count == 0:
            continue

        minus_score /= check_clear_count
        current_best_key = score_key
            
        if check_clear_count == 1:
            current_best_score = check_data[0]["score"]
        else:
            check_data = sorted( check_data, key=lambda x:x["score"] )

            if check_clear_count % 2 == 1:
                median_index = int( check_clear_count / 2 )
                current_best_score = check_data[median_index]["score"]
            else:
                median_index_1 = int( check_clear_count / 2 )
                median_index_2 = int( check_clear_count / 2 - 1 )
                current_best_score = int( ( check_data[median_index_1]["score"] + check_data[median_index_2]["score"] ) / 2 )

        #current_best_score = current_best_score * ( check_clear_count / genetic_score_ensemble_count )
        current_best_score -= minus_score
        
        if best_score < current_best_score:
            best_score = current_best_score
            best_key = current_best_key
            best_one = check_clear_count
        
    #print( best_data )
    return best_score, best_key, best_one
    
def main():
    comm = MPI.COMM_WORLD   #COMM_WORLDは全体
    size = comm.Get_size()  #サイズ（指定されたプロセス（全体）数）
    rank = comm.Get_rank()  #ランク（何番目のプロセスか。プロセスID）
    name = MPI.Get_processor_name() #プロセスが動いているノードのホスト名

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
        N = 100
        population = 10
        first_key = list( learn_data.keys() )[0]
        next_key = list( learn_data[first_key].keys() )[0]
        elements_key_list = list( learn_data[first_key][next_key].keys() )
        score_result = {}
        best_population = {}

        for k in use_buy_key:
            ga = GA( population, elements_key_list )
    
            for i in range( 0, N ):
                score_list = []
                one_list = []

                if rank == 0:
                    print( "kind:{} num:{}".format( k, i ) )
                    s = int( population / ( size - 1 ) )
                    for r in range( 1, size ):
                        s1 = s * ( r - 1 )
                        s2 = s1 + s
                        comm.send( ga.parent[s1:s2], dest = r, tag = 0 )

                    for r in range( 1, size ):
                        instance_score = comm.recv( source = r, tag = 1 )
                        instance_one = comm.recv( source = r, tag = 2 )
                        score_list.extend( instance_score )
                        one_list.extend( instance_one )                    
                else:
                    parents = comm.recv( source = 0, tag = 0 )
                    instance_score_list = []
                    instance_one_list = []
                    
                    for parent in parents:
                        score, best_key, one = score_create( learn_data, parent, k )
                        instance_score_list.append( score )
                        instance_one_list.append( one )
                        print( "score:{} best_key_score:{}, one:{}".format( score, best_key, one ) )

                    comm.send( instance_score_list, dest = 0, tag = 1 )
                    comm.send( instance_one_list, dest = 0, tag = 2 )

                if rank == 0:
                    ga.scores_set( score_list, one_list )
                    ga.next_genetic()
                    print( "best_score:{} best_one:{}\n".format( ga.best_score, ga.best_one ) )

            if rank == 0:
                final_test_score, _, _ = score_create( test_data, ga.best_population, k )
                _ , best_key, _ = score_create( learn_data, ga.best_population, k )
                print( "best_score:{} best_data{}".format( ga.best_score, ga.best_population ) )
                print( "final_test_score:{}".format( final_test_score ) )
                print( "check_key: {}".format( best_key ) )
                best_population[k] = ga.best_population
                best_key_data[k] = best_key
                score_result[k] = { "best_score": ga.best_score, "final_test_score": final_test_score }

        if rank == 0:
            dm.pickle_upload( "users_score_rate.pickle", best_population )
            dm.pickle_upload( "users_best_key.pickle", best_key_data )
            
            for k in score_result.keys():
                print( "kind:{} best_score:{} final_test_score:{} best_key:{} \n".format( k, score_result[k]["best_score"], score_result[k]["final_test_score"], best_key_data[k] ) )

    if not rank == 0:
        sys.exit()
    
    print( "test start" )
    test.main( test_data, use_buy_key, "test" )
    test.main( learn_data, use_buy_key, "learn" )

if __name__ == "__main__":
    main()
