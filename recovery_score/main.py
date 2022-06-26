from tqdm import tqdm
from mpi4py import MPI

import sekitoba_library as lib
import sekitoba_data_manage as dm

from once_data import OnceData
from data_set import DataSet

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

        for i in range( 1, size ):
            file_name = comm.recv( source = i, tag = 2 )
            instance = dm.local_pickle_load( file_name )
            users_data.update( instance["users"] )
            rank_data.update( instance["rank"] )

        ds.set_all_data( users_data, rank_data )
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

        instance = { "rank": od.rank_data, "users": od.ds.users_data }
        file_name = str( rank ) + "-instance.pickle"
        dir_name = "./storage/"
        dm.local_pickle_save( dir_name + file_name, instance )
        comm.send( dir_name + file_name, dest = 0, tag = 2 )

if __name__ == "__main__":
    main()
