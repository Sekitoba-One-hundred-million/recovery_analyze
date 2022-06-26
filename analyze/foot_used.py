import sekitoba_library as lib
import sekitoba_data_manage as dm
import sekitoba_data_create as dc

from tqdm import tqdm
import matplotlib.pyplot as plt

dm.dl.file_set( "race_data.pickle" )
dm.dl.file_set( "race_info_data.pickle" )
dm.dl.file_set( "race_rank_data.pickle" )
dm.dl.file_set( "horce_data_storage.pickle" )
dm.dl.file_set( "time_index_data.pickle" )

name = "foot_used"

def main():
    result = {}
    race_data = dm.dl.data_get( "race_data.pickle" )
    race_info = dm.dl.data_get( "race_info_data.pickle" )
    race_rank_data = dm.dl.data_get( "race_rank_data.pickle" )
    horce_data = dm.dl.data_get( "horce_data_storage.pickle" )
    foot_used_data = dm.dl.data_get( "foot_used.pickle" )
    time_index_data = dm.dl.data_get( "time_index_data.pickle" )
    
    for k in tqdm( race_data.keys() ):
        race_id = lib.id_get( k )
        year = race_id[0:4]
        race_place_num = race_id[4:6]
        day = race_id[9]
        num = race_id[7]

        key_place = str( race_info[race_id]["place"] )
        key_dist = str( race_info[race_id]["dist"] )
        key_kind = str( race_info[race_id]["kind"] )        
        key_baba = str( race_info[race_id]["baba"] )

        if year in lib.test_years:
            continue

        #芝かダートのみ
        if key_kind == "0" or key_kind == "3":
            continue

        for kk in race_data[k].keys():
            horce_id = kk
            current_data, past_data = lib.race_check( horce_data[horce_id],
                                                     year, day, num, race_place_num )#今回と過去のデータに分ける
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )

            if not cd.race_check():
                continue

            before_cd = pd.before_cd()

            if before_cd == None:
                continue

            try:
                horce_time_index = time_index_data[horce_id]
            except:
                continue

            current_race_rank = race_rank_data[race_id]
            past_cd_list = pd.past_cd_list()
            foot_score = { "1": -100, "2": -100 }
            
            for past_cd in past_cd_list:
                past_race_id = past_cd.race_id()
                
                try:
                    past_race_rank = race_rank_data[past_race_id]
                    foot_used = foot_used_data[past_race_id]
                    time_index = horce_time_index[past_cd.birthday()]
                except:
                    continue

                if past_race_rank < current_race_rank:
                    continue

                key_foot_used = str( foot_used )
                foot_score[key_foot_used] = max( foot_score[key_foot_used], time_index )

            score = -1

            try:
                before_foot_used = foot_used_data[before_cd.race_id()]
            except:
                continue
            
            if not foot_score["1"] == -100 and \
              not foot_score["2"] == -100:
                good_foot_used = 0

                if foot_score["1"] > foot_score["2"]:
                    good_foot_used = 1
                else:
                    good_foot_used = 2

                #slope = lib.stright_slope( cd.place() )
                score = cd.baba_status() * 10 + good_foot_used
                
            key = str( int( score ) )  
            lib.dic_append( result, year, {} )
            lib.dic_append( result[year], key, { "recovery": 0, "count": 0 } )
            
            result[year][key]["count"] += 1

            if cd.rank() == 1:
                result[year][key]["recovery"] += cd.odds()

    for year in result.keys():
        for k in result[year].keys():
            result[year][k]["recovery"] /= result[year][k]["count"]
            result[year][k]["recovery"] = round( result[year][k]["recovery"], 2 )

    score = lib.recovery_score_check( result )
    lib.write_recovery_csv( result, name + ".csv" )
    
if __name__ == "__main__":
    main()
        
