import copy
import random
import numpy as np

import SekitobaLibrary as lib

TEACHER = "teacher"
YEAR = "year"

class ManageScore:
    def __init__( self, learn_data, cd = {} ):
        self.data_name_list = []
        self.cluster_data = copy.deepcopy( cd )
        self.data_type = copy.deepcopy( learn_data["type"] )
        self.sort_data = {}
        self.genelation = 0
        self.read_score_name()

        if not len( self.cluster_data ) == 0:
            return

        self.create_init_cluster( learn_data )

        for name in self.data_name_list:
            self.create_init_score( name )

    def update_cluster( self, cluster_data ):
        self.cluster_data = copy.deepcopy( cluster_data )

    def check_float_score( self, value, name ):
        score = lib.escapeValue
        
        for i in range( 0, len( self.cluster_data[name]["cut"] ) ):
            if value <= self.cluster_data[name]["cut"][i]:
                score = self.cluster_data[name]["score"][i]
                break

        if score == lib.escapeValue:
            score = self.cluster_data[name]["score"][-1]

        return score

    def check_int_score( self, value, name ):
        value = int( value )
        score = lib.escapeValue

        for i in range( 0, len( self.cluster_data[name]["cut"] ) ):
            if value == self.cluster_data[name]["cut"][i]:
                score = self.cluster_data[name]["score"][i]
                break

        return score

    def check_score( self, value, name ):
        if value == lib.escapeValue:
            return 0

        score = lib.escapeValue
        
        if self.data_type[name] == float:
            score = self.check_float_score( value, name )
        elif self.data_type[name] == int:
            score = self.check_int_score( value, name )

        return score
            
    def read_score_name( self ):
        f = open( "common/rank_score_data.txt", "r" )
        all_data = f.readlines()

        for data in all_data:
            data = data.replace( "\n", "" )

            if len( data ) == 0:
                continue
            
            self.data_name_list.append( data )

    def create_init_score( self, data_name ):
        self.cluster_data[data_name]["score"] = []

        for i in range( 0, len( self.cluster_data[data_name]["cut"] ) ):
            self.cluster_data[data_name]["score"].append( random.random() )

        if self.data_type[data_name] == float:
            self.cluster_data[data_name]["score"].append( random.random() )

    def create_int_cut_data( self, learn_data, data_name ):
        score_index = self.data_name_list.index( data_name )
        data_list = []

        for i in range( 0, len( learn_data["teacher"] ) ):
            for r in range( 0, len( learn_data["teacher"][i] ) ):
                value = int( learn_data["teacher"][i][r][score_index] )
                
                if value == lib.escapeValue or value in data_list:
                    continue

                data_list.append( value )

        data_list.sort()
        self.cluster_data[data_name] = { "cut": data_list }
        
    def create_float_cut_data( self, learn_data, data_name ):
        cluster = random.randint( 5, 25 )
        score_index = self.data_name_list.index( data_name )
        data_list = []
        
        for i in range( 0, len( learn_data["teacher"] ) ):
            year = learn_data["year"][i]

            if year in lib.simu_years:
                continue

            instance_data = []
            
            for r in range( 0, len( learn_data["teacher"][i] ) ):
                value = learn_data["standardization"][i][r][score_index]
                
                if value == lib.escapeValue:
                    continue
                    
                data_list.append( value )

        data_list.sort()
        cut_line_data = []
        cut_index_data = []
            
        for i in range( 1, cluster ):
            cut_index = int( i * ( len( data_list ) / cluster ) )
            cut_index_data.append( cut_index )

        n1 = 0
        n2 = cut_index_data[1]
            
        for i in range( 0, len( cut_index_data ) ):
            normal_dis = np.random.normal( 
                loc = cut_index_data[i],
                scale = 50,
                size = 100 )

            for sc in normal_dis:
                if sc < n1 and n2 < sc:
                    continue

                cut_index_data[i] = int( sc )
                break

            n1 = cut_index_data[i]
            cut_line_data.append( data_list[n1] )

            if i + 1 == len( cut_index_data ):
                n2 = len( cut_index_data )
            else:
                n2 = cut_index_data[i+1]            

        cut_line_data.sort()
        cut_index_data.sort()
        self.cluster_data[data_name] = { "cut": cut_line_data,
                                         "index": cut_index_data }
        self.sort_data[data_name] = data_list
            
    def create_init_cluster( self, learn_data ):
        for data_name in self.data_name_list:
            if self.data_type[data_name] == float:
                self.create_float_cut_data( learn_data, data_name )
            elif self.data_type[data_name] == int:
                self.create_int_cut_data( learn_data, data_name )
