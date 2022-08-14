import copy
import random
import numpy as np
import torch
from torch.autograd import Variable
import torch.nn.functional as F

import sekitoba_library as lib
import sekitoba_data_manage as dm

from simulation import Simulation
from data import Data
from nn import MoneyNN

LEARNING_RATE = 0.01

dm.dl.file_set( "users_score_data.pickle" )

def data_split( data ):
    learn_data = {}
    test_data = {}
    
    for race_id in data.keys():
        year = race_id[0:4]

        if year in lib.test_years:
            test_data[race_id] = copy.deepcopy( data[race_id] )
        else:
            learn_data[race_id] = copy.deepcopy( data[race_id] )

    return learn_data, test_data

def answer_score_create( model: MoneyNN, simulation: Simulation, learn_data: dict ):
    kind = "one"
    trial_count = 5
    check_rate = 0.05
    penalty_bet_rate = 0.1
    ganma = 0.1

    answer_data = []
    predict_data = []
    average_recovery = 0
    average_bet_count = 0

    for t in range( trial_count ):
        use_data = []
        use_id_list = []

        for race_id in learn_data.keys():
            if random.random() < check_rate:
                use_id_list.append( race_id )
                
                for horce_id in learn_data[race_id].keys():
                    use_data.append( learn_data[race_id][horce_id] )

        all_race_num = len( use_data )
        money, bet_count, select_list = simulation.function[kind]( model, learn_data, use_id_list )
        bet_rate = bet_count / all_race_num
        recovery_rate = 0
        
        if not bet_count == 0:
            recovery_rate = ( bet_count + money ) / bet_count
        
        score = ( recovery_rate - 1 )
        average_recovery += recovery_rate
        average_bet_count += bet_count

        if bet_rate < penalty_bet_rate:
            score -= ( penalty_bet_rate - bet_rate )

        score = min( max( score, -1 ), 1 )
        predict_data.extend( use_data )

        for select in select_list:
            select_score = copy.deepcopy( select[0] )

            if select[1] == 0:
                select_score[0] += ganma * score
                select_score[1] -= ganma * score
            else:
                select_score[0] -= ganma * score
                select_score[1] += ganma * score
                
            select_score[0] = min( max( select_score[0], -1 ), 1 )
            select_score[1] = min( max( select_score[1], -1 ), 1 )
            answer_data.append( copy.deepcopy( select_score ) )

    average_recovery /= trial_count
    average_bet_count /= trial_count
    predict_data = model.forward( torch.tensor( np.array( predict_data, dtype = np.float32 ) ) )
    print( "recovery: {} bet_count: {}".format( average_recovery, average_bet_count ) )
    return predict_data, torch.from_numpy( np.array( answer_data, dtype=np.float32 ) )
    #return predict_data, answer_data

def main():
    N = 100
    users_score_data = dm.dl.data_get( "users_score_data.pickle" )
    data = Data( users_score_data )
    simulation = Simulation()
    model = MoneyNN( data.N )
    optimizer = torch.optim.Adam( model.parameters(), lr = LEARNING_RATE )

    print( "learn start" )
    
    for n in range( 1, N + 1 ):
        model.eval()
        predict_data, answer_data = answer_score_create( model, simulation, data.learn_data )
        model.train()
        loss = F.l1_loss( predict_data, answer_data )
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print( "n:{} loss:{}".format( n, loss ) )

if __name__ == "__main__":
    main()
