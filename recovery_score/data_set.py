import sekitoba_library as lib
import sekitoba_data_manage as dm

class DataSet:
    def __init__( self ):
        self.split_data = {}
        self.not_split_data = {}
        self.split_list_data = {}
        self.analyze_score_data = {}
        self.year = ""
        self.odds = 0
        self.set_name()

    def set_name( self ):
        f = open( "common/list.txt", "r" )
        name_data = f.readlines()

        for name in name_data:
            name = name.replace( "\n", "" )
            self.split_data[name] = []
            self.not_split_data[name] = {}

    def set_yo( self, year, odds ):
        self.year = year
        self.odds = odds

    def set_not_split_data( self, name, score ):
        key_score = str( int( score ) )
        key_year = str( int( self.year ) )
        lib.dic_append( self.not_split_data[name], key_year, {} )
        lib.dic_append( self.not_split_data[name][key_year], key_score, { "recovery": 0, "count": 0 } )
        self.not_split_data[name][key_year][key_score]["count"] += 1
        self.not_split_data[name][key_year][key_score]["recovery"] += self.odds

    def set_split_data( self, name, score ):
        key_year = str( int( self.year ) )
        instance = {}
        instance["key"] = score
        instance["odds"] = self.odds
        instance["year"] = key_year
        self.split_data[name].append( instance )

    def recovery_check( self, data ):
        for year in data.keys():
            for k in data[year].keys():
                data[year][k]["recovery"] /= data[year][k]["count"]
                data[year][k]["recovery"] = round( data[year][k]["recovery"], 2 )

        return data

    def data_analyze( self ):
        for name in self.split_data.keys():
            if len( self.split_data[name] ) == 0:
                continue
            
            recovery_data, split_list = lib.recovery_data_split( self.split_data[name] )
            recovery_data = self.recovery_check( recovery_data )
            analyze_score = lib.recovery_score_check( recovery_data )
            print( name, analyze_score )
            self.analyze_score_data[name] = analyze_score
            self.split_list_data[name] = split_list

        for name in self.not_split_data.keys():
            if len( self.not_split_data[name] ) == 0:
                continue

            recovery_data = self.recovery_check( self.not_split_data[name] )
            analyze_score = lib.recovery_score_check( recovery_data )
            print( name, analyze_score )
            self.analyze_score_data[name] = analyze_score

    def data_upload( self ):
        dm.pickle_upload( "split_data.pickle", self.split_list_data )
        dm.pickle_upload( "recovery_score_data.pickle", self.analyze_score_data )
