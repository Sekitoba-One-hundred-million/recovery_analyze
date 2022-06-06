import sekitoba_library as lib
import sekitoba_data_manage as dm

dm.dl.file_set( "odds_data.pickle" )

class Simulation():
    def __init__( self ):
        self.odds_data = dm.dl.data_get( "odds_data.pickle" )
        self.function = {}
        self.function["one"] = self.one
        self.function["quinella"] = self.quinella
        self.function["trio"] = self.trio
        self.function["wide"] = self.wide

        self.odds_key = { "one": "単勝", "quinella": "馬連", "trio": "三連複", "wide": "ワイド" }

    def simulation( self, learn_data, rate_data, kind, test = False ):
        result = []
        
        for race_id in learn_data.keys():
            instance_list = []
            try:
                current_odds = self.odds_data[race_id]
            except:
                continue
            
            for i in range( 0, len( learn_data[race_id] ) ):
                instance = { "odds": 0, "score": 0 }

                for k in learn_data[race_id][i]["score"].keys():
                    if test:
                        instance["score"] += learn_data[race_id][i]["score"][k]
                    else:
                        instance["score"] += rate_data[k] * learn_data[race_id][i]["score"][k]
                        
                    instance["rank"] = learn_data[race_id][i]["rank"]
                    instance["score"] = int( instance["score"] )
                
                instance_list.append( instance )

            if not len( instance_list ) == 0:
                result.extend( self.function[kind]( instance_list, current_odds[self.odds_key[kind]] ) )
            
        result = sorted( result, key=lambda x:x["score"], reverse = True )
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

    def trio( self, data, odds ):
        result = []

        for i in range( 0, len( data ) ):
            for r in range( i + 1, len( data ) ):
                for t in range( r + 1, len( data ) ):
                    score = int( data[i]["score"] + data[r]["score"] + data[t]["score"] )
                    od = odds if data[i]["score"] < 4 and data[r]["score"] < 4 and data[t]["score"] < 4 else 0

                    result.append( { "score": score, "odds": od / 100 } )

        return result
