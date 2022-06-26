import sekitoba_library as lib
import sekitoba_data_manage as dm

dm.dl.file_set( "odds_data.pickle" )
dm.dl.file_set( "rank_score.pickle" )
dm.dl.file_set( "rank_win_rate_data.pickle" )

class Simulation():
    def __init__( self ):
        self.odds_data = dm.dl.data_get( "odds_data.pickle" )
        self.rank_win_rate_data = dm.dl.data_get( "rank_win_rate_data.pickle" )
        self.rank_score = dm.dl.data_get( "rank_score.pickle" )
        self.odds_key = { "one": "単勝", "quinella": "馬連" }
        self.buy_score = { "one": 1407, "quinella": 2610 }
        self.function = {}
        self.function["one"] = self.one
        self.function["quinella"] = self.quinella
        self.money = 1000
        self.first_money = 1000
        self.money_list = []

    def bet_money( self, rate ):
        rate = min( 0.01, rate )
        bet_money = min( self.money / 2, self.first_money )
        bet_money = self.money / 2
        return max( int( bet_money * rate ), 1 )

    def users_score_check( self, users_score, kind ):
        if self.buy_score[kind] <= users_score:
            return True

        return False

    def rank_rate( self, score, rate_kind ):
        rate = -1

        for i in range( 0, len( self.rank_win_rate_data["split"] ) ):
            
            if self.rank_win_rate_data["split"][i] < score:
                rate = self.rank_win_rate_data[rate_kind][i]
                break

        if rate == -1:
            rate = self.rank_win_rate_data[rate_kind][-1]

        return rate

    def score_create( self, learn_data, rate_data ):
        result = {}
        
        for race_id in learn_data.keys():
            result[race_id] = {}
            
            for horce_id in learn_data[race_id].keys():
                instance = {}
                instance["rank"] = learn_data[race_id][horce_id]["rank"]
                instance["score"] = {}
                
                for kind in self.odds_key.keys():
                    instance["score"][kind] = 0
                    
                    for k in learn_data[race_id][horce_id]["score"].keys():
                        instance["score"][kind] += rate_data[kind][k] * learn_data[race_id][horce_id]["score"][k]

                    instance["score"][kind] = int( instance["score"][kind] )
                    
                result[race_id][horce_id] = instance

        return result

    def quinella( self, race_data, odds, race_id ):
        win = 0
        count = 0
        recovery = 0
        kind = "quinella"
        rate_kind = "up_two"
        key_list = list( race_data.keys() )
        move_money = 0

        for i in range( 0, len( key_list ) ):
            horce_id_1 = key_list[i]

            for r in range( i + 1, len( key_list ) ):
                horce_id_2 = key_list[r]
                users_score = race_data[horce_id_1]["score"][kind] + race_data[horce_id_2]["score"][kind]

                if self.users_score_check( users_score, kind ):
                    count += 1
                    rank_score_1 = self.rank_score[race_id][horce_id_1]
                    rank_score_2 = self.rank_score[race_id][horce_id_2]
                    rate = self.rank_rate( rank_score_1["score"], rate_kind ) * self.rank_rate( rank_score_2["score"], rate_kind )
                    move_money -= self.bet_money( rate )
                    
                    if race_data[horce_id_1]["rank"] <= 2 and race_data[horce_id_2]["rank"] <= 2:
                        win += 1
                        recovery += odds / 100
                        move_money += self.bet_money( rate ) * ( odds / 100 )

        self.money += move_money
        return count, win, recovery

    def one( self, race_data, odds, race_id ):
        win = 0
        count = 0
        recovery = 0
        kind = "one"
        rate_kind = "up_two"
        move_money = 0

        for horce_id in race_data.keys():            
            score = race_data[horce_id]["score"][kind]

            if self.buy_score[kind] <= score:
                count += 1
                rate = self.rank_rate( self.rank_score[race_id][horce_id]["score"], rate_kind )
                move_money -= self.bet_money( rate )

                if race_data[horce_id]["rank"] == 1:
                    win += 1
                    recovery += odds / 100
                    move_money += self.bet_money( rate ) * ( odds / 100 )
        
        self.money += move_money
        return count, win, recovery

    def buy( self, race_data, race_id ):
        win = 0
        count = 0
        recovery = 0
        
        try:
            current_odds = self.odds_data[race_id]
        except:
            return count, win, recovery

        for kind in self.buy_score.keys():
            try:
                self.rank_score[race_id]
            except:
                continue

            if self.money < 0:
                break

            c, w, r = self.function[kind]( race_data, current_odds[self.odds_key[kind]], race_id )
            count += c
            win += w
            recovery += r

        self.money_list.append( self.money )
        return count, win, recovery
