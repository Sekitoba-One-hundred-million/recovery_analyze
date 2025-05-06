import faulthandler

faulthandler.enable()

def data_score_read():
    result = []
    f = open( "./common/rank_score_data.txt", "r" )
    all_data = f.readlines()

    for i in range( 0, len( all_data ) ):
        split_data = all_data[i].replace( "\n", "" ).split( " " )

        if len( split_data ) == 2:
            result.append( i )
            
    f.close()
    result = sorted( result, reverse = True )
    return result

def data_remove( data: list, delete_data: list ):
    for i in range( 0, len( delete_data ) ):
        data.pop( delete_data[i] )

    return data

def main():
    from argparse import ArgumentParser
    import matplotlib.pyplot as plt
    import numpy as np
    from mpi4py import MPI
    from tqdm import tqdm

    import SekitobaDataManage as dm
    import SekitobaLibrary as lib

    from learn import recovery_main
    from data_analyze import data_create

    lib.name.set_name( "recovery" )

    comm = MPI.COMM_WORLD   #COMM_WORLDは全体
    size = comm.Get_size()  #サイズ（指定されたプロセス（全体）数）
    rank = comm.Get_rank()  #ランク（何番目のプロセスか。プロセスID）
    name = MPI.Get_processor_name() #プロセスが動いているノードのホスト名

    lib.log.set_write( False )
    parser = ArgumentParser()
    parser.add_argument( "-u", type=bool, default = False, help = "optional" )
    parser.add_argument( "-l", type=bool, default = False, help = "optional" )
    parser.add_argument( "-s", type=str, default = 'test', help = "optional" )
    parser.add_argument( "-o", type=bool, default = False, help = "optional" )
    parser.add_argument( "-b", type=bool, default = False, help = "optional" )

    u_check = parser.parse_args().u
    l_check = parser.parse_args().l
    s_check = parser.parse_args().s
    o_check = parser.parse_args().o
    b_check = parser.parse_args().b

    if s_check == 'prod':
        lib.prod_check = True

    data = data_create.main( update = u_check )

    if u_check and rank == 0:
        dm.pickle_upload( lib.name.data_name(), data["data"] )
        dm.pickle_upload( lib.name.simu_name(), data["simu"] )

    if l_check:
        if rank == 0:
            recovery_main.main_core( data["data"], data["simu"] )
        else:
            recovery_main.sub_core()

    MPI.Finalize()        
    
if __name__ == "__main__":
    main()
