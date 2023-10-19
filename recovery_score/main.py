from tqdm import tqdm
from mpi4py import MPI

import sekitoba_library as lib
import sekitoba_data_manage as dm

from score_create import ScoreCreate
from once_data import OnceData
from data_set import DataSet

import recovery_check

def key_list_search( rank, size, key_list ):
    n = int( len( key_list ) / ( size - 1 ) )
    s1 = int( ( rank - 1 ) * n )

    if not rank + 1 == size:
        s2 = s1 + n
    else:
        s2 = len( key_list ) + 1

    return key_list[s1:s2]

def main():
    comm = MPI.COMM_WORLD   #COMM_WORLDは全体
    size = comm.Get_size()  #サイズ（指定されたプロセス（全体）数）
    rank = comm.Get_rank()  #ランク（何番目のプロセスか。プロセスID）
    name = MPI.Get_processor_name() #プロセスが動いているノードのホスト名

    if rank == 0:
        dm.dl.local_keep()
        
        for i in range( 1, size ):
            comm.send( True, dest = i, tag = 1 )

        ds = DataSet()
        rank_data = {}
        users_data = {}
        odds_data = {}

        for i in range( 1, size ):
            file_name = comm.recv( source = i, tag = 2 )
            print( "finish rank {}".format( i ) )
            instance = dm.local_pickle_load( file_name )
            users_data.update( instance["users"] )
            rank_data.update( instance["rank"] )
            odds_data.update( instance["odds"] )

        ds.set_all_data( users_data, rank_data, odds_data )
        recovery_check.main( ds )
        
        race_id = list( ds.users_data.keys() )[0]
        horce_id = list( ds.users_data[race_id].keys() )[0]
        score_key_list = list( ds.users_data[race_id][horce_id].keys() )
        l = len( score_key_list )
        score_create = ScoreCreate( ds )

        for i, score_key in enumerate( score_key_list ):
            print( l - i, score_key )
            score_create.create( score_key )

        score_create.json_create()
        ds.data_upload()
    else:
        ok = comm.recv( source = 0, tag = 1 )        
        od = OnceData()
        print( "start rank:{}".format( rank ) )
        key_list = key_list_search( rank, size, list( od.race_data.keys() ) )

        if rank == 1:
            for k in tqdm( key_list ):
                od.create( k )
        else:
            for k in key_list:
                od.create( k )

        instance = { "rank": od.ds.rank_data, "odds": od.ds.odds_data, "users": od.ds.users_data }
        file_name = str( rank ) + "-instance.pickle"
        dir_name = "./storage/"
        dm.local_pickle_save( dir_name, file_name, instance )
        comm.send( dir_name + file_name, dest = 0, tag = 2 )
        return

def test():
    comm = MPI.COMM_WORLD   #COMM_WORLDは全体
    size = comm.Get_size()  #サイズ（指定されたプロセス（全体）数）
    rank = comm.Get_rank()  #ランク（何番目のプロセスか。プロセスID）
    name = MPI.Get_processor_name() #プロセスが動いているノードのホスト名

    if rank == 0:
        plus_score_data = {}
        minus_score_data = {}

        for i in range( 1, size ):
            plus_instance = comm.recv( source = i, tag = 0 )
            minus_instance = comm.recv( source = i, tag = 1 )
            plus_score_data.update( plus_instance )
            minus_score_data.update( minus_instance )
            print( i )

        score_create = ScoreCreate( None )
        score_create.plus_score = plus_score_data
        score_create.minus_score = minus_score_data
        score_create.json_create()
    else:
        ds = DataSet()
        ds.odds_data = dm.pickle_load( "users_odds_data.pickle" )
        ds.rank_data = dm.pickle_load( "users_rank_data.pickle" )
        ds.users_data = dm.pickle_load( "users_data.pickle" )

        race_id = list( ds.users_data.keys() )[0]
        horce_id = list( ds.users_data[race_id].keys() )[0]
        score_key_list = list( ds.users_data[race_id][horce_id].keys() )
        score_create = ScoreCreate( ds )
        #print( score_key_list[-1] )
        #score_create.create( score_key_list[-1] )
    
        for i, score_key in enumerate( score_key_list ):
            if i % int( size - 1 ) == int( rank - 1 ):
                print( rank, len( score_key_list ) - i, score_key )
                score_create.create( score_key )

        comm.send( score_create.plus_score, dest = 0, tag = 0 )
        comm.send( score_create.minus_score, dest = 0, tag = 1 )
    
if __name__ == "__main__":
    #main()
    test()
