from tqdm import tqdm
from mpi4py import MPI

import sekitoba_library as lib
import sekitoba_data_manage as dm

from common.name import Name
from once_data import OnceData

data_name = Name()

dm.dl.file_set( "race_data.pickle" )
dm.dl.file_set( "race_info_data.pickle" )
dm.dl.file_set( "horce_data_storage.pickle" )
dm.dl.file_set( "baba_index_data.pickle" )
dm.dl.file_set( "parent_id_data.pickle" )

def use_key_list( key_list ):
    result = []
    
    for k in key_list:
        race_id = lib.id_get( k )
        year = race_id[0:4]

        if year in lib.test_years:
            result.append( k )

    return result

def key_list_search( rank, size, key_list ):
    n = int( len( key_list ) / ( size - 1 ) )
    s1 = int( ( rank - 1 ) * n )

    if not rank + 1 == size:
        s2 = s1 + n
    else:
        s2 = len( key_list ) + 1

    return key_list[s1:s2]

def data_connect( base, add_data ):
    for year in add_data.keys():
        lib.dic_append( base, year, {} )
        for score in add_data[year].keys():
            lib.dic_append( base[year], score, { "recovery": 0, "count": 0 } )
            base[year][score]["count"] += add_data[year][score]["count"]
            base[year][score]["recovery"] += add_data[year][score]["recovery"]

def recovery_check( data ):
    check = {}
    key_list = []

    for year in data.keys():
        for score in data[year].keys():
            if not score in check.keys():
                check[score] = True
                key_list.append( int( score ) )
        
    key_list = sorted( key_list, reverse = True )
    
    for year in data.keys():
        
        for k in key_list:
            k = str( k )
            try:
                data[year][k]["recovery"] = data[year][k]["recovery"] / data[year][k]["count"]
                data[year][k]["recovery"] = round( data[year][k]["recovery"], 2 )
            except:
                data[year][k] = {}
                data[year][k]["recovery"] = 0
                data[year][k]["count"] = 0

def main():
    comm = MPI.COMM_WORLD   #COMM_WORLDは全体
    size = comm.Get_size()  #サイズ（指定されたプロセス（全体）数）
    rank = comm.Get_rank()  #ランク（何番目のプロセスか。プロセスID）
    name = MPI.Get_processor_name() #プロセスが動いているノードのホスト名

    if rank == 0:
        dm.dl.local_keep()
        
        for i in range( 1, size ):
            comm.send( True, dest = i, tag = 1 )

        score_data = {}

        for i in range( 1, size ):
            file_name = comm.recv( source = i, tag = 2 )
            instance = dm.local_pickle_load( file_name )
            data_connect( score_data, instance )

        recovery_check( score_data )
        file_name = "users_score.csv"
        lib.write_recovery_csv( score_data, file_name )
    else:
        ok = comm.recv( source = 0, tag = 1 )
        od = OnceData()
        print( "start rank:{}".format( rank ) )
        key_list = use_key_list( list( od.race_data.keys() ) )
        key_list = key_list_search( rank, size, key_list )

        if rank == 1:
            for k in tqdm( key_list ):
                od.create( k )
        else:
            for k in key_list:
                od.create( k )

        file_name = str( rank ) + "-instance.pickle"
        dir_name = "./storage/"
        dm.local_pickle_save( dir_name + file_name, od.data )
        comm.send( dir_name + file_name, dest = 0, tag = 2 )

    MPI.Finalize()
    
if __name__ == "__main__":
    main()
