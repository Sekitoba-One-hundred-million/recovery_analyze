import sekitoba_library as lib
import sekitoba_data_manage as dm
from sekitoba_data_create.race_type import RaceType
from tqdm import tqdm
import matplotlib.pyplot as plt

dm.dl.file_set( "race_data.pickle" )
dm.dl.file_set( "wrap_data.pickle" )
dm.dl.file_set( "race_info_data.pickle" )
dm.dl.file_set( "horce_data_storage.pickle" )

name = "my_deployment_count"

def main():
    result = {}
    race_data = dm.dl.data_get( "race_data.pickle" )
    wrap_data = dm.dl.data_get( "wrap_data.pickle" )
    race_info = dm.dl.data_get( "race_info_data.pickle" )
    horce_data = dm.dl.data_get( "horce_data_storage.pickle" )
    race_type = RaceType()
    
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

        #芝かダートのみ
        if key_kind == "0" or key_kind == "3":
            continue

        race_deployment = {}
        check_deployment = {}
        
        for kk in race_data[k].keys():
            horce_id = kk
            current_data, past_data = lib.race_check( horce_data[horce_id],
                                                     year, day, num, race_place_num )#今回と過去のデータに分ける
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )

            if not cd.race_check():
                continue

            past_cd_list = pd.past_cd_list()
            search_deployment = { "1": 100, "2": 100, "3": 100, "4": 100, "5": 100, "6": 100 }
            
            for past_cd in past_cd_list:
                past_race_id = past_cd.race_id()
                
                try:
                    past_wrap_data = wrap_data[past_race_id]
                except:
                    continue

                past_deployment = lib.pace_create( past_wrap_data )
                
                if past_deployment == -1:
                    continue

                key_past_deployment = str( int( past_deployment ) )
                search_deployment[key_past_deployment] = min( past_cd.rank(), search_deployment[key_past_deployment] )

                best_dep_score = 100
            best_dep = ""

            for dk in search_deployment.keys():
                if search_deployment[dk] < best_dep_score:
                    best_dep_score = search_deployment[dk]
                    best_dep = dk

            if len( best_dep ) == 0:
                continue

            race_deployment[kk] = best_dep
            lib.dic_append( check_deployment, best_dep, 0 )
            check_deployment[best_dep] += 1

        for kk in race_data[k].keys():
            horce_id = kk
            current_data, past_data = lib.race_check( horce_data[horce_id],
                                                     year, day, num, race_place_num )#今回と過去のデータに分ける
            cd = lib.current_data( current_data )
            pd = lib.past_data( past_data, current_data )

            if not cd.race_check():
                continue

            if not kk in race_deployment.keys():
                continue
            
            score = check_deployment[race_deployment[kk]]
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
    #lib.recovery_data_upload( name, score, [] )
    
if __name__ == "__main__":
    main()
        
