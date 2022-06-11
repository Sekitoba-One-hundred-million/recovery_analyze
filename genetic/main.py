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
    current_score = analyze_data[0]["score"]
    score = 0
    count = 0
    recovery = 0
    max_count = 0 
    
    for data in analyze_data:
        count += 1
        
        if data["score"] == current_score:
            recovery += data["odds"]
        else:
            r = recovery / count
            profit_money = recovery - count
            score = max( score, profit_money )
            recovery += data["odds"]
            current_score = data["score"]

    return score
    
def main():
    data_update = input( "data update? (y/n): " )

    if data_update == "y":
        learn_data = {}
        test_data = {}
    elif data_update == "n":
        learn_data = dm.pickle_load( "genetic_learn_data.pickle" )
        test_data = dm.pickle_load( "genetic_test_data.pickle" )

    if learn_data == None or len( learn_data ) == 0:
        from once_data import OnceData
        
        od = OnceData()
        test_simu_data = {}
        key_list, test_key_list = key_list_get()
        print( test_key_list[0], key_list[-1] )
        for k in tqdm( key_list ):
            data, _, race_id = od.create( k )

            if not race_id == None:
                learn_data[race_id] = data

        for k in tqdm( test_key_list ):
            data, simu_data, race_id = od.create( k )

            if not race_id == None:
                test_data[race_id] = data
                test_simu_data[race_id] = simu_data

        dm.pickle_upload( "genetic_learn_data.pickle", learn_data )
        dm.pickle_upload( "genetic_test_data.pickle", test_data )
        dm.pickle_upload( "users_score_simu_data.pickle", test_simu_data )

    ga_update = input( "GA update? (y/n): " )

    if ga_update == "y":
        buy_key = [ "one", "quinella", "wide" ]
        use_buy_key = []

        for k in buy_key:
            ny = input( "buy update {} (y/n): ".format( k ) )

            if ny == "y":
                use_buy_key.append( k )
        
        N = 100
        population = 10
        first_key = list( learn_data.keys() )[0]
        elements_key_list = list( learn_data[first_key][0]["score"].keys() )
        score_result = {}
        best_population = dm.pickle_load( "users_score_rate.pickle" )

        if best_population == None:
            best_population = {}

        for k in use_buy_key:
            ga = GA( population, elements_key_list )
    
            for i in range( 0, N ):
                score_list = []        
                print( "kind:{} num:{}".format( k, i ) )
        
                for parent in ga.parent:
                    score = score_create( learn_data, parent, k )
                    score_list.append( score )
                    print( "score:{}".format( score ) )

                ga.scores_set( score_list )
                ga.next_genetic()
                print( "best_score:{}\n".format( ga.best_score ) )

            final_test_score = score_create( test_data, ga.best_population, k )
            print( "best_score:{} best_data{}".format( ga.best_score, ga.best_population ) )
            print( "final_test_score:{}".format( final_test_score ) )
            best_population[k] = ga.best_population
            score_result[k] = { "best_score": ga.best_score, "final_test_score": final_test_score }

        for k in score_result.keys():
            print( "kind:{} best_score:{} final_test_score:{}".format( k, \
                                                                      score_result[k]["best_score"], \
                                                                      score_result[k]["final_test_score"] ) )
        
        dm.pickle_upload( "users_score_rate.pickle", best_population )

    print( "test start" )
    test.main()

if __name__ == "__main__":
    main()
