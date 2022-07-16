import copy
import random
from tqdm import tqdm
import matplotlib.pyplot as plt

from simulation import Simulation

import sekitoba_library as lib
import sekitoba_data_manage as dm

dm.dl.file_set( "genetic_test_data.pickle" )
dm.dl.file_set( "users_score_rate.pickle" )
dm.dl.file_set( "odds_data.pickle" )

def main():
    count = 0
    recovery = 0
    win = 0
    odds_data = dm.dl.data_get( "odds_data.pickle" )
    users_score_data = dm.dl.data_get( "users_score_data.pickle" )
    users_score_rate = dm.dl.data_get( "users_score_rate.pickle" )
    users_score_test_data = {}

    for race_id in users_score_data.keys():
        year = race_id[0:4]

        if year in lib.test_years:
            users_score_test_data[race_id] = copy.deepcopy( users_score_data[race_id] )

    users_score_data.clear()
    si = Simulation()
    analyze_data = si.score_create( users_score_test_data, users_score_rate )
    key_list = list( analyze_data.keys() )
    random.shuffle( key_list )
    
    for race_id in key_list:
        current_odds = odds_data[race_id]
        c, w, r = si.buy( analyze_data[race_id], race_id )
        count += c
        win += w
        recovery += r
        
    recovery_rate = ( recovery / count ) * 100
    win_rate = ( win / count ) * 100
    print( "bet_count:{}".format( count ) )
    print( "recovery_rate:{}%".format( recovery_rate ) )
    print( "win_rate:{}%".format( win_rate ) )
    print( "money:{}".format( int( si.money ) ) )

    x = range( len( si.money_list ) )
    plt.plot( x, si.money_list )
    plt.savefig( "/Users/kansei/Desktop/recovery_data/test.png" )

if __name__ == "__main__":
    main()
