import math
import random
import copy
import numpy as np
from mpi4py import MPI

from learn import ManageScore
from learn import simulation
from learn import genetic

import SekitobaLibrary as lib
import SekitobaDataManage as dm

def create_softmax_data( learn_data ):
    learn_data["softmax"] = [ [] for _ in range( len( learn_data["teacher"] ) ) ]

    for i in range( 0, len( learn_data["teacher"] ) ):
        softmax_init_data = []
        
        for r in range( 0, len( learn_data["teacher"][i] ) ):
            softmax_init_data.append( [ 0 ] * len( learn_data["teacher"][i][r] ) )

        learn_data["softmax"][i] = softmax_init_data

        for t in range( 0, len( learn_data["teacher"][i][0] ) ):
            instance_data = []
            
            for r in range( 0, len( learn_data["teacher"][i] ) ):
                instance_data.append( learn_data["teacher"][i][r][t] )

            softmax_instance_data = lib.softmax( instance_data, escape_list = [ lib.escapeValue ] )

            for r in range( 0, len( softmax_instance_data ) ):
                learn_data["softmax"][i][r][t] = softmax_instance_data[r]

def create_standardization_data( learn_data ):
    learn_data["standardization"] = [ [] for _ in range( len( learn_data["teacher"] ) ) ]

    for i in range( 0, len( learn_data["teacher"] ) ):
        standardization_init_data = []
        
        for r in range( 0, len( learn_data["teacher"][i] ) ):
            standardization_init_data.append( [ 0 ] * len( learn_data["teacher"][i][r] ) )

        learn_data["standardization"][i] = standardization_init_data

        for t in range( 0, len( learn_data["teacher"][i][0] ) ):
            instance_data = []
            
            for r in range( 0, len( learn_data["teacher"][i] ) ):
                instance_data.append( learn_data["teacher"][i][r][t] )

            standardization_instance_data = lib.standardization( instance_data, abort = [ lib.escapeValue ] )

            for r in range( 0, len( standardization_instance_data ) ):
                learn_data["standardization"][i][r][t] = standardization_instance_data[r]
        
def main_core( learn_data, simu_data ):
    comm = MPI.COMM_WORLD   #COMM_WORLDは全体
    size = comm.Get_size()  #サイズ（指定されたプロセス（全体）数）
    rank = comm.Get_rank()  #ランク（何番目のプロセスか。プロセスID）
    name = MPI.Get_processor_name() #プロセスが動いているノードのホスト名

    year_list = []

    for year in learn_data["year"]:
        if not year in year_list:
            year_list.append( year )            

    N = 20
    STEP = 200
    ANSANBLE = 3
    finish = False
    learn_sort_data = {}
    test_remove_year_list = copy.deepcopy( year_list )
    test_remove_year_list.remove( lib.recovery_test_years[0] )
    test_remove_year_list.remove( lib.recovery_test_years[1] )

    print( "main:{}".format( rank ) )
    result_manage_score_list = []    

    for c in range( 0, ANSANBLE ):
        best_score = -1
        manage_score_list = []
        best_manage_score_list = []
        create_standardization_data( learn_data )

        for i in range( 0, N ):
            print( "main:{} create:{}".format( rank, i ) )
            manage_score = ManageScore( learn_data )

            if len( learn_sort_data ) == 0:
                learn_sort_data = copy.deepcopy( manage_score.sort_data )

            manage_score.sort_data.clear()
            manage_score_list.append( manage_score )
        
        for i in range( 0, STEP ):
            check_rank = 0
            instance_manage_score_list = copy.deepcopy( manage_score_list )

            while 1:
                if len( instance_manage_score_list ) == 0:
                    break
                
                check_rank += 1
                send_rank = int( check_rank % size )

                if send_rank == 0:
                    continue

                instance_manage_score = instance_manage_score_list.pop( 0 )
                comm.send( instance_manage_score, dest = send_rank, tag = 1 )

            for r in range( 1, size ):
                comm.send( None, dest = r, tag = 1 )

            manage_score_list.clear()
            recovery_list = []

            for r in range( 1, size ):
                recv_data = comm.recv( source = r, tag = r )
                recovery_list.extend( recv_data["recovery"] )
                manage_score_list.extend( recv_data["manage_score"] )

            best_score = -1
            best_manage_score = None
            score_list = []
        
            for r in range( 0, len( recovery_list ) ):
                score = recovery_list[r]

                if best_score < score:
                    best_score = score
                    best_manage_score = copy.deepcopy( manage_score_list[r] )

            if best_manage_score.genelation == 0:
                #check_score = simulation.main( learn_data,
                #                               best_manage_score,
                #                               recovery_len = 5,
                #                               escape_year_list = test_remove_year_list )
                best_manage_score_list.append( { "score": simulation.test_simu( simu_data, [ best_manage_score ], test_years = lib.recovery_test_years ),
                                                 "manage_score": best_manage_score } )
                #best_manage_score_list.append( { "score": check_score,
                #                                 "manage_score": best_manage_score } )

            print( c, i, len( best_manage_score_list ), min( recovery_list ), best_score,
                   best_manage_score_list[-1]["score"],
                   simulation.test_simu( simu_data, [ best_manage_score ], test_years = lib.simu_years ) )
            genetic.main( manage_score_list, recovery_list, learn_sort_data )

            if i == int( STEP - 1 ) and c == int( ANSANBLE - 1 ):
                finish = True

            for r in range( 1, size ):
                comm.send( finish, dest = r, tag = 1 )

        best_manage_score_list.sort( key = lambda x:x["score"], reverse = True )
        result_manage_score_list.append( copy.deepcopy( best_manage_score_list[0]["manage_score"] ) )
        
    print( "main:{} finish".format( rank ) )
    print( simulation.test_simu( simu_data, result_manage_score_list, test_years = lib.recovery_test_years ),
           simulation.test_simu( simu_data, result_manage_score_list, test_years = lib.simu_years ) )

    result_cluster = {}
    result_cluster["name"] = result_manage_score_list[0].data_name_list
    result_cluster["type"] = result_manage_score_list[0].data_type
    result_cluster["cluster"] = []

    for manage_score in result_manage_score_list:
        result_cluster["cluster"].append( manage_score.cluster_data )

    dm.pickle_upload( "recovery_cluster_data.pickle", result_cluster )

def sub_core():
    comm = MPI.COMM_WORLD   #COMM_WORLDは全体
    size = comm.Get_size()  #サイズ（指定されたプロセス（全体）数）
    rank = comm.Get_rank()  #ランク（何番目のプロセスか。プロセスID）
    name = MPI.Get_processor_name() #プロセスが動いているノードのホスト名
    print( "sub:{}".format( rank ) )
    learn_data = dm.pickle_load( lib.name.data_name() )
    create_standardization_data( learn_data )

    year_list = []

    for year in learn_data["year"]:
        if not year in year_list:
            year_list.append( year )            

    remove_valid_year_list = [ year for year in year_list if not year in lib.recovery_test_years ]

    while 1:
        manage_score_list: list[ ManageScore ] = []

        while 1:
            manage_score = comm.recv( source = 0, tag = 1 )

            if manage_score is None:
                break

            manage_score_list.append( manage_score )

        recovery_list = []

        for i in range( 0, len( manage_score_list ) ):
            recovery = simulation.main( learn_data, manage_score_list[i], \
                                         escape_year_list = lib.test_years )
            recovery_list.append( recovery )
        
        send_data = { "recovery": recovery_list, \
                      "manage_score": manage_score_list }
        comm.send( send_data, dest = 0, tag = rank )
        finish = comm.recv( source = 0, tag = 1 )
        
        if finish:
            print( "sub:{} finish".format( rank ) )
            break
