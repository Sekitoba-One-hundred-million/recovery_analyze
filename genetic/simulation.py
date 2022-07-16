from mpi4py import MPI

import sekitoba_library as lib
import sekitoba_data_manage as dm

dm.dl.file_set( "odds_data.pickle" )
dm.dl.file_set( "users_rank_data.pickle" )

comm = MPI.COMM_WORLD   #COMM_WORLDは全体
size = comm.Get_size()  #サイズ（指定されたプロセス（全体）数）
rank = comm.Get_rank()  #ランク（何番目のプロセスか。プロセスID）
name = MPI.Get_processor_name() #プロセスが動いているノードのホスト名

class Simulation():
    def __init__( self ):
        self.odds_data = dm.dl.data_get( "odds_data.pickle" )
        self.users_rank_data = dm.dl.data_get( "users_rank_data.pickle" )        
        self.function = {}
        self.function["one"] = self.one
        self.function["quinella"] = self.quinella
        self.function["triple"] = self.triple
        self.function["wide"] = self.wide

        self.odds_key = { "one": "単勝", "quinella": "馬連", "triple": "三連複", "wide": "ワイド" }

    def simulation( self, learn_data, rate_data, buy_kind, test = False ):
        result = {}
        
        for race_id in learn_data.keys():
            instance_list = []
            try:
                current_odds = self.odds_data[race_id]
            except:
                continue

            for horce_id in learn_data[race_id].keys():
                instance = { "odds": 0, "score": 0 }
                
                for kind in learn_data[race_id][horce_id].keys():
                    if test:
                        instance["score"] += learn_data[race_id][horce_id][kind]
                    else:
                        instance["score"] += rate_data[kind] * learn_data[race_id][horce_id][kind]
                        
                instance["rank"] = self.users_rank_data[race_id][horce_id]
                instance["score"] = int( int( instance["score"] / 5 ) * 5 )
                instance_list.append( instance )

            if not len( instance_list ) == 0:
                year = race_id[0:4]
                lib.dic_append( result, year, [] )
                result[year].extend( self.function[buy_kind]( instance_list, current_odds[self.odds_key[buy_kind]] ) )

        for year in result.keys():
            result[year] = sorted( result[year], key=lambda x:x["score"], reverse = True )
            
        return result

    def one( self, data, odds ):
        result = []
        
        for i in range( 0, len( data ) ):
            score = data[i]["score"]
            od = odds if data[i]["rank"] == 1 else 0
            result.append( { "score": score, "odds": od / 100 } )

        return result
            
    def quinella( self, data, odds ):
        result = []
        
        for i in range( 0, len( data ) ):
            for r in range( i + 1, len( data ) ):
                score = int( data[i]["score"] + data[r]["score"] )
                od = odds if data[i]["rank"] < 3 and data[r]["rank"] < 3 else 0
                result.append( { "score": score, "odds": od / 100 } )

        return result

    def triple( self, data, odds ):
        result = []
        
        for i in range( 0, len( data ) ):
            for r in range( i + 1, len( data ) ):
                for t in range( r + 1, len( data ) ):
                    score = int( data[i]["score"] + data[r]["score"] + data[t]["score"] )
                    od = odds if data[i]["rank"] < 4 and data[r]["rank"] < 4 and data[t]["rank"] < 4 else 0
                    result.append( { "score": score, "odds": od / 100 } )

        return result

    def wide( self, data, odds ):
        result = []
        for i in range( 0, len( data ) ):
            for r in range( i + 1, len( data ) ):
                score = int( data[i]["score"] + data[r]["score"] )
                od = 0
                
                if data[i]["rank"] < 4 and data[r]["rank"] < 4:
                    ra = int( data[i]["rank"] + data[r]["rank"] - 3 )
                    
                    try:
                        od = odds[ra]
                    except:
                        od = 0

                result.append( { "score": score, "odds": od / 100 } )

        return result
