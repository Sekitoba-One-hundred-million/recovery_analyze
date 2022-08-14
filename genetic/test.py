from tqdm import tqdm

import sekitoba_library as lib
import sekitoba_data_manage as dm
from simulation import Simulation

def data_create( learn_data, rate_data, buy_key ):
    result = {}
    score_key = {}
    si = Simulation()
    
    for ticket_kind in buy_key:
        print( ticket_kind )
        result[ticket_kind] = {}
        result[ticket_kind]["all"] = {}
        score_key[ticket_kind] = {}
        analyze_data = si.simulation( learn_data, rate_data[ticket_kind], ticket_kind )

        for year in analyze_data.keys():
            lib.dic_append( result[ticket_kind], year, {} )
            
            for data in analyze_data[year]:
                key_score = str( data["score"] )
                score_key[ticket_kind][key_score] = data["score"]
                lib.dic_append( result[ticket_kind][year], key_score, { "recovery": 0, "count": 0 } )
                lib.dic_append( result[ticket_kind]["all"], key_score, { "recovery": 0, "count": 0 } )
                result[ticket_kind][year][key_score]["recovery"] += data["odds"]
                result[ticket_kind][year][key_score]["count"] += 1
                result[ticket_kind]["all"][key_score]["recovery"] += data["odds"]
                result[ticket_kind]["all"][key_score]["count"] += 1
                
        for year in analyze_data.keys():
            for key_score in score_key[ticket_kind].keys():
                try:
                    result[ticket_kind][year][key_score]["recovery"] /=  result[ticket_kind][year][key_score]["count"]
                    result[ticket_kind][year][key_score]["recovery"] = round( result[ticket_kind][year][key_score]["recovery"], 2 )
                except:
                    result[ticket_kind][year][key_score] = { "recovery": 0, "count": 0 }

        for key_score in result[ticket_kind]["all"].keys():
            result[ticket_kind]["all"][key_score]["recovery"] /= result[ticket_kind]["all"][key_score]["count"]
            result[ticket_kind]["all"][key_score]["recovery"] = round( result[ticket_kind]["all"][key_score]["recovery"], 2 )

    return result, score_key

def csv_write( file_name, data, score_key_dict ):
    f = open( file_name, "w" )
    score_key_list = []
    first = True
    write_score = "year/score\t"

    for k in score_key_dict.keys():
        score_key_list.append( int( k ) )

    score_key_list = sorted( score_key_list )

    for year in data.keys():
        write_recovery = year + "\t"
        write_count = year + "\t"

        for score_key in score_key_list:
            score_key = str( score_key )

            if first:
                write_score += score_key + "\t"

            try:
                write_recovery += str( data[year][score_key]["recovery"] ) + "\t"
                write_count += str( data[year][score_key]["count"] ) + "\t"
            except:
                write_recovery += "0\t"
                write_count += "0\t"

        if first:
            write_score += "\n"
            f.write( write_score )

        write_recovery += "\n"
        write_count += "\n\n"
        f.write( write_recovery )
        f.write( write_count )            
        first = False
            
    f.close()

def key_check( test_data, users_score_rate, kind_key_list, users_best_key ):
    si = Simulation()
    
    for ticket_kind in users_best_key.keys():
        recovery = 0
        count = 0
        check_score = int( users_best_key[ticket_kind] )
        analyze_data = si.simulation( test_data, users_score_rate[ticket_kind], ticket_kind )

        for year in analyze_data.keys():
            for data in analyze_data[year]:
                if check_score <= data["score"]:
                    recovery += data["odds"]
                    count += 1

        recovery /= count
        print( "{} check_score: {}".format( ticket_kind, check_score ) )
        print( "recovery: {} count: {}\n".format( recovery, count ) )

def pram_write( users_rate_data, ticket_kind ):
    f = open( ticket_kind + "_score_rate.txt", "w" )
    
    for k in users_rate_data[ticket_kind].keys():
        f.write( k + ": " + str( users_rate_data[ticket_kind][k] ) + "\n" )

    f.close()

def main( test_data, users_score_rate, users_best_key, kind_key_list, name ):
    test_result, score_key = data_create( test_data, users_score_rate, kind_key_list )
    dir_name = "/Users/kansei/Desktop/recovery_data/"

    for k in kind_key_list:
        pram_write( users_score_rate, k )
        csv_write( dir_name + "genetic_" + name + "_" + k + "_users_score.csv", test_result[k], score_key[k] )

    key_check( test_data, users_score_rate, kind_key_list, users_best_key )
