import math
import torch
import random
import numpy as np

import sekitoba_library as lib
import sekitoba_data_manage as dm

from nn import MoneyNN

dm.dl.file_set( "odds_data.pickle" )
dm.dl.file_set( "users_rank_data.pickle" )

# 0: not buy
# 1: buy

class Simulation():
    def __init__( self ):
        self.odds_data = dm.dl.data_get( "odds_data.pickle" )
        self.users_rank_data = dm.dl.data_get( "users_rank_data.pickle" )
        self.function = {}
        self.function["one"] = self.one_simulation
        self.odds_key = { "one": "単勝", "quinella": "馬連", "triple": "三連複", "wide": "ワイド" }

    def buy( self, not_buy_rate ):
        if random.random() < not_buy_rate:
            return False

        return True

    def rate_create( self, data ):
        rate_data = []
        sum_data = 0

        for d in data:
            sum_data += math.exp( d )

        for d in data:
            rate_data.append( math.exp( d ) / sum_data )

        return rate_data
          

    def one_simulation( self, model: MoneyNN, learn_data: dict, race_id_list: list ):
        kind = "one"
        money = 0
        bet_count = 0
        select_list = []

        for race_id in race_id_list:
            for horce_id in learn_data[race_id].keys():
                select = model.forward( torch.tensor( np.array( [ learn_data[race_id][horce_id] ], dtype = np.float32 ) ) )[0].detach().numpy()
                select_rate = self.rate_create( select )
                s = 0
                
                if self.buy( select_rate[0] ):
                #if select_rate[0] < select_rate[1]:
                    money -= 1
                    bet_count += 1
                    s = 1

                    if self.users_rank_data[race_id][horce_id] == 1:
                        money += self.odds_data[race_id][self.odds_key[kind]] / 100
                        
                select_list.append( ( select, s ) )
                
        return money, bet_count, select_list
