import sekitoba_library as lib
import sekitoba_data_manage as dm

from data_set import DataSet

RECOVERY = "recovery"
COUNT = "count"

def main( ds: DataSet ):
    recovery_data = {}
    
    for race_id in ds.users_data.keys():
        key_year = race_id[0:4]
        
        for horce_id in ds.users_data[race_id].keys():
            for users_score_kind in ds.users_data[race_id][horce_id].keys():
                key_score = str( int( ds.users_data[race_id][horce_id][users_score_kind] ) )

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

    write_name = {}

    for name in recovery_data.keys():
        name = name.replace( "_minus", "" )
        write_name[name] = True
    
    for name in write_name.keys():
        lib.write_recovery_csv( recovery_data[name], name + ".csv", add_dir = "prod_recovery/" )
