import copy
import random
import numpy as np

import SekitobaLibrary as lib

def rate_softmax( data ):
    result = []
    sum_data = 0
    min_value = min( data ) * 0.95

    for i in range( 0, len( data ) ):
        data[i] -= min_value

    sum_data = sum( data )

    for i in range( 0, len( data ) ):
        result.append( data[i] / sum_data )

    return result

def create_normal_dis( loc, scale, check_type, s1, s2 ):
    result = lib.escapeValue
    normal_dis = np.random.normal( 
        loc = loc,
        scale = scale,
        size = 100 )

    for sc in normal_dis:
        sc = check_type( sc )

        if sc <= s1 or s2 <= sc:
            continue

        result = sc
        break
    
    if result == lib.escapeValue:
        print( "loc: {}".format( loc ) )
        print( "scale: {}".format( scale ) )
        print( "s1: {}".format( s1 ) )
        print( "s2: {}".format( s2 ) )
        print( "normal_dis: {}".format( normal_dis ) )
    
    return result

def select_parent( genetic_data ):
    parent_count = 2
    all_rate = 1
    parent_data = []
    
    use_genetic_data: list = copy.deepcopy( genetic_data )

    for i in range( 0, parent_count ):
        select_index = -1
        current_rate = 0
        check_rate = random.random()

        for r in range( 0, len( use_genetic_data ) ):
            current_rate += use_genetic_data[r]["rate"] / all_rate

            if check_rate <= current_rate:
                select_index = r
                break

        parent_data.append( use_genetic_data.pop( select_index ) )
        all_rate -= parent_data[-1]["rate"]        

    return parent_data

def create_next_cut_data( parent_data: list, sort_data: dict ):
    next_cut_index_data = {}

    for parent in parent_data:
        current_cluster: dict = parent["manage_score"].cluster_data
        current_data_tyoe: dict = parent["manage_score"].data_type
        
        for name in current_cluster.keys():
            if current_data_tyoe[name] == int:
                continue

            lib.dic_append( next_cut_index_data, name, [] )
            next_cut_index_data[name].extend( current_cluster[name]["index"] )

    for name in next_cut_index_data.keys():
        cut_count = create_normal_dis( loc = int( len( next_cut_index_data[name] ) / len( parent_data ) ),
                                       scale = 2,
                                       check_type = int,
                                       s1 = 4,
                                       s2 = 26 )

        if cut_count == lib.escapeValue:
            print( "{}: not found cut count",format( name ) )
            exit( 1 )
        
        append = False

        if len( next_cut_index_data[name] ) == cut_count:
            continue
        elif len( next_cut_index_data[name] ) < cut_count:
            append = True

        while 1:
            next_cut_index_data[name].sort()

            if len( next_cut_index_data[name] ) == cut_count:
                break

            s1 = lib.escapeValue
            s2 = lib.escapeValue
            max_dist = lib.escapeValue
            min_dist = 10000000000

            for i in range( 1, len( next_cut_index_data[name] ) ):
                current_dist = abs( next_cut_index_data[name][i] - next_cut_index_data[name][i-1] )

                if current_dist < min_dist and not append:
                    min_dist = current_dist
                    s1 = int( next_cut_index_data[name][i] )
                    s2 = int( next_cut_index_data[name][i-1] )
                elif max_dist < current_dist and append:
                    max_dist = current_dist
                    s1 = int( next_cut_index_data[name][i] )
                    s2 = int( next_cut_index_data[name][i-1] )

            if not append:
                next_cut_index_data[name].remove( s1 )
                next_cut_index_data[name].remove( s2 )

            next_cut_index_data[name].append( int( ( s1 + s2 ) / 2 ) )

    for name in next_cut_index_data.keys():
        next_cut_index_data[name].sort()

        for i in range( 0, len( next_cut_index_data[name] ) ):
            n1 = 0
            n2 = len( sort_data[name] )

            if i > 0:
                n1 = next_cut_index_data[name][i-1]

            if int( i + 1 ) < len( next_cut_index_data[name] ):
                n2 = next_cut_index_data[name][i+1]

            next_cut_data = create_normal_dis( loc = int( next_cut_index_data[name][i] ),
                                               scale = int( len( sort_data[name] ) / 2000 ),
                                               check_type = int,
                                               s1 = n1, s2 = n2 )

            if next_cut_data == lib.escapeValue:
                print( "i: {}".format( i ) )
                print( "n1: {}".format( n1 ) )
                print( "n2: {}".format( n2 ) )
                print( "len: {}".format( len( sort_data[name] ) ) )
                print( "next_cut_index_data: {}".format( next_cut_index_data[name] ) )

            next_cut_index_data[name][i] = next_cut_data

    next_cut_data = {}
    use_cluster: dict = parent["manage_score"].cluster_data

    for name in next_cut_index_data.keys():
        next_cut_data[name] = {}
        next_cut_data[name]["cut"] = []
        next_cut_data[name]["index"] = copy.deepcopy( next_cut_index_data[name] )

        for index in next_cut_index_data[name]:
            next_cut_data[name]["cut"].append( sort_data[name][index] )

        next_cut_data[name]["cut"].sort()
        next_cut_data[name]["index"].sort()

    return next_cut_data

def create_child( parent_data: list, sort_data: dict ):
    next_cluster_data = {}
    next_score_data = {}
    data_type: dict = parent_data[0]["manage_score"].data_type
    name_list = list( data_type.keys() )
    next_cluster_data.update( create_next_cut_data( parent_data, sort_data ) )

    for name in name_list:
        score_len = 0

        if data_type[name] == int:
            next_cluster_data[name] = {}
            next_cluster_data[name]["cut"] = copy.deepcopy( parent_data[0]["manage_score"].cluster_data[name]["cut"] )
            score_len = len( next_cluster_data[name]["cut"] )
        elif data_type[name] == float:
            score_len = int( len( next_cluster_data[name]["cut"] ) + 1 )

        next_cluster_data[name]["score"] = [ 0 ] * score_len
        next_cluster_data[name]["score_rate"] = [ 0 ] * score_len
            
        for parent in parent_data:
            parent_cluster: dict = parent["manage_score"].cluster_data

            for i in range( 0, len( next_cluster_data[name]["score"] ) ):
                if data_type[name] == int:
                    next_cluster_data[name]["score_rate"][i] += 1
                    next_cluster_data[name]["score"][i] += parent_cluster[name]["score"][i]
                elif data_type[name] == float:
                    current_before_index = 0
                    current_index = len( sort_data[name] )

                    if 0 < i:
                        current_before_index = next_cluster_data[name]["index"][i-1]

                    if i < len( next_cluster_data[name]["index"] ):
                        current_index = next_cluster_data[name]["index"][i]
                        
                    for r in range( 0, len( parent_cluster[name]["score"] ) ):
                        parent_before_index = 0
                        parent_index = len( sort_data[name] )

                        if 0 < r:
                            parent_before_index = parent_cluster[name]["index"][r-1]

                        if r < len( parent_cluster[name]["index"] ):
                            parent_index = parent_cluster[name]["index"][r]

                        if parent_index < current_before_index and parent_before_index < current_before_index:
                            continue
                        elif current_index < parent_index and current_index < parent_before_index:
                            break

                        use_index_list = [ current_index, current_before_index, parent_index, parent_before_index ]
                        use_index_list.sort()
                        check_dist = abs( int( use_index_list[1] - use_index_list[2] ) )
                        parent_dist = abs( int( parent_index - parent_before_index ) )
                        check_rate = check_dist / parent_dist
                        next_cluster_data[name]["score"][i] += parent_cluster[name]["score"][r] * check_rate
                        next_cluster_data[name]["score_rate"][i] += check_rate

    for name in name_list:
        for i in range( 0, len( next_cluster_data[name]["score"] ) ):
            if next_cluster_data[name]["score_rate"][i] == 0:
                print( name, i, len( next_cluster_data[name]["score_rate"] ) )
                print( next_cluster_data[name]["index"] )
                print( next_cluster_data[name]["score"] )
                print( next_cluster_data[name]["score_rate"] )
                
            score = next_cluster_data[name]["score"][i] / next_cluster_data[name]["score_rate"][i]
            next_score = lib.escapeValue
            normal_dis = np.random.normal( 
            loc = score,
            scale = 0.1,
            size = 100 )

            for sc in normal_dis:
                if sc <= 0 or 1 <= sc:
                    continue

                next_score = float( sc )
                break

            if next_score == lib.escapeValue:
                print( "not found child score" )
                exit( 1 )

            next_cluster_data[name]["score"][i] = next_score

        next_cluster_data[name].pop( "score_rate" )
            
    return next_cluster_data

def main( manage_score_list, score_list, sort_data ):
    genetic_data = []
    rate_list = rate_softmax( score_list )

    for i in range( 0, len( rate_list ) ):
        genetic_data.append( { "rate": rate_list[i], "manage_score": manage_score_list[i] } )

    genetic_data.sort( key = lambda x:x["rate"], reverse = True )
    children_data = []
    children_data.append( copy.deepcopy( genetic_data[0]["manage_score"].cluster_data ) )

    while 1:
        if len( children_data ) == len( manage_score_list ):
            break

        parent_data = select_parent( genetic_data )
        children_data.append( create_child( parent_data, sort_data ) )

    for i in range( 0, len( manage_score_list ) ):
        if i == 0:
            manage_score_list[i].genelation += 1
        else:
            manage_score_list[i].genelation = 0

        manage_score_list[i].update_cluster( children_data[i] )
