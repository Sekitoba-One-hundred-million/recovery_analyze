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

def split_data_connect( base, add_data ):
    for k in add_data.keys():
        lib.dic_append( base, k, [] )
        base[k].extend( add_data[k] )

def not_split_data_connect( base, add_data ):
    for name in add_data.keys():
        lib.dic_append( base, name, {} )
        for year in add_data[name].keys():
            lib.dic_append( base[name], year, {} )
            for score in add_data[name][year].keys():
                lib.dic_append( base[name][year], score, { "recovery": 0, "count": 0 } )
                base[name][year][score]["count"] += add_data[name][year][score]["count"]
                base[name][year][score]["recovery"] += add_data[name][year][score]["recovery"]

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
        split_data = {}
        not_split_data = {}

        for i in range( 1, size ):
            file_name = comm.recv( source = i, tag = 2 )
            instance = dm.local_pickle_load( file_name )
            split_data_connect( split_data, instance["split"] )
            not_split_data_connect( not_split_data, instance["not_split"] )

        ds.set_all_data( split_data, not_split_data )
        ds.data_analyze()
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

        instance = { "split": od.ds.split_data, "not_split": od.ds.not_split_data }
        file_name = str( rank ) + "-instance.pickle"
        dir_name = "./storage/"
        dm.local_pickle_save( dir_name + file_name, instance )
        comm.send( dir_name + file_name, dest = 0, tag = 2 )

if __name__ == "__main__":
    main()
