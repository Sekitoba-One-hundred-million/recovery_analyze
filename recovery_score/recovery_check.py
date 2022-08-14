import sekitoba_library as lib
import sekitoba_data_manage as dm

from data_set import DataSet

RECOVERY = "recovery"
COUNT = "count"

def main( ds: DataSet ):
    recovery_data = {}
    recovery_test_data = {}
    
    for race_id in ds.users_data.keys():
        key_year = race_id[0:4]
        
        for horce_id in ds.users_data[race_id].keys():
            for users_score_kind in ds.users_data[race_id][horce_id].keys():
                key_score = str( int( ds.users_data[race_id][horce_id][users_score_kind] ) )

                if key_year in lib.test_years:
                    lib.dic_append( recovery_test_data, users_score_kind, {} )
                    lib.dic_append( recovery_test_data[users_score_kind], key_year, {} )
                    lib.dic_append( recovery_test_data[users_score_kind][key_year], key_score, { RECOVERY: 0, COUNT: 0 } )
                    recovery_test_data[users_score_kind][key_year][key_score][COUNT] += 1
                
                    if ds.rank_data[race_id][horce_id] == 1:
                        recovery_test_data[users_score_kind][key_year][key_score][RECOVERY] += ds.odds_data[race_id][horce_id]
                else:
                    lib.dic_append( recovery_data, users_score_kind, {} )
                    lib.dic_append( recovery_data[users_score_kind], key_year, {} )
                    lib.dic_append( recovery_data[users_score_kind][key_year], key_score, { RECOVERY: 0, COUNT: 0 } )
                    recovery_data[users_score_kind][key_year][key_score][COUNT] += 1
                    
                    if ds.rank_data[race_id][horce_id] == 1:
                        recovery_data[users_score_kind][key_year][key_score][RECOVERY] += ds.odds_data[race_id][horce_id]

    for name in recovery_data.keys():
        for year in recovery_data[name].keys():
            for key_score in recovery_data[name][year].keys():
                recovery_data[name][year][key_score][RECOVERY] /= recovery_data[name][year][key_score][COUNT]
                recovery_data[name][year][key_score][RECOVERY] = round( recovery_data[name][year][key_score][RECOVERY], 2 )

    for name in recovery_test_data.keys():
        for year in recovery_test_data[name].keys():
            for key_score in recovery_test_data[name][year].keys():
                recovery_test_data[name][year][key_score][RECOVERY] /= recovery_test_data[name][year][key_score][COUNT]
                recovery_test_data[name][year][key_score][RECOVERY] = round( recovery_test_data[name][year][key_score][RECOVERY], 2 )

    for name in recovery_data.keys():
        lib.write_recovery_csv( recovery_data[name], name + ".csv", add_dir = "prod_recovery/" )
        lib.write_recovery_csv( recovery_test_data[name], name + "_test.csv", add_dir = "prod_recovery/" )
