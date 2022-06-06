from tqdm import tqdm

from simulation import Simulation

import sekitoba_library as lib
import sekitoba_data_manage as dm

dm.dl.file_set( "genetic_test_data.pickle" )
dm.dl.file_set( "users_score_rate.pickle" )

def main():
    count = 0
    recovery = 0
    win = 0
    test_data = dm.dl.data_get( "genetic_test_data.pickle" )
    users_score_rate = dm.dl.data_get( "users_score_rate.pickle" )
    buy_score = { "one": 1343, "quinella": 2460 }
    si = Simulation()

    for kind in buy_score.keys():
        analyze_data = si.simulation( test_data, users_score_rate[kind], kind )
        
        for data in analyze_data:
            if buy_score[kind] <= data["score"]:
                count += 1
                recovery += data["odds"]

                if not data["odds"] == 0:
                    win += 1

    recovery_rate = ( recovery / count ) * 100
    win_rate = ( win / count ) * 100
    money = int( recovery_rate * count - ( count * 100 ) )
    print( "bet_count:{}".format( count ) )
    print( "recovery_rate:{}%".format( recovery_rate ) )
    print( "win_rate:{}%".format( win_rate ) )
    print( "money:{}".format( money ) )

if __name__ == "__main__":
    main()
