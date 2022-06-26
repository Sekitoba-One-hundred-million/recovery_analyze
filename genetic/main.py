import sys
import copy
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
    recovery_data = {}

    for year in analyze_data.keys():
        recovery_data[year] = {}
        current_score = analyze_data[year][0]["score"]
        score = 0
        count = 0
        recovery = 0
        max_count = 0 
        
        for data in analyze_data[year]:
            count += 1
        
            if data["score"] == current_score:
                recovery += data["odds"]
            else:
                key_score = current_score
                r = recovery / count
                recovery_data[year][key_score] = { "recovery": r, "count": count }
                recovery += data["odds"]
                current_score = data["score"]

    check_recovery = 1.05
    score_data = {}

    for year in recovery_data.keys():
        for key_score in recovery_data[year].keys():
            lib.dic_append( score_data, key_score, { "recovery": 0, "count": 0, "one": 0 } )
            score_data[key_score]["count"] += 1
            
            if check_recovery < recovery_data[year][key_score]["recovery"]:
                money = recovery_data[year][key_score]["recovery"] * recovery_data[year][key_score]["count"]
                score_data[key_score]["recovery"] += money - recovery_data[year][key_score]["count"]
                score_data[key_score]["one"] += 1

    best_score = 0
    best_key_score = "0"
    
    for key_score in score_data.keys():
        rate = score_data[key_score]["one"] / score_data[key_score]["count"]
        score = score_data[key_score]["recovery"] * rate

        if best_score < score:
            best_key_score = key_score
            best_score = score

    return best_score, best_key_score
    
def main():
    comm = MPI.COMM_WORLD   #COMM_WORLDは全体
    size = comm.Get_size()  #サイズ（指定されたプロセス（全体）数）
    rank = comm.Get_rank()  #ランク（何番目のプロセスか。プロセスID）
    name = MPI.Get_processor_name() #プロセスが動いているノードのホスト名

    use_buy_key = []
    use_buy_key.append( "one" )
    use_buy_key.append( "quinella" )

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
        ga_update = input( "ga update(y/n): " )
        
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

                if rank == 0:
                    print( "kind:{} num:{}".format( k, i ) )
                    s = int( population / ( size - 1 ) )
                    for r in range( 1, size ):
                        s1 = s * ( r - 1 )
                        s2 = s1 + s
                        comm.send( ga.parent[s1:s2], dest = r, tag = 0 )

                    for r in range( 1, size ):
                        instance_score = comm.recv( source = r, tag = 1 )
                        score_list.extend( instance_score )
                        
                else:
                    parents = comm.recv( source = 0, tag = 0 )
                    instance_score_list = []
                    
                    for parent in parents:
                        score, best_key = score_create( learn_data, parent, k )
                        instance_score_list.append( score )
                        print( "score:{} best_key_score:{}".format( score, best_key ) )

                    comm.send( instance_score_list, dest = 0, tag = 1 )

                if rank == 0:
                    ga.scores_set( score_list )
                    ga.next_genetic()
                    print( "best_score:{}\n".format( ga.best_score ) )

            if rank == 0:
                final_test_score, _ = score_create( test_data, ga.best_population, k )
                _ , best_key = score_create( learn_data, ga.best_population, k )
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
    test.main( test_data, use_buy_key )

if __name__ == "__main__":
    main()
