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
    test_data = dm.dl.data_get( "users_score_simu_data.pickle" )
    users_score_rate = dm.dl.data_get( "users_score_rate.pickle" )
    si = Simulation()
    analyze_data = si.score_create( test_data, users_score_rate )
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
