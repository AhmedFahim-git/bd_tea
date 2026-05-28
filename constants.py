### CONSTANTS for make_viz_file.py

ALL_DISTRICT_COLUMNS = [
    "geometry",
    "admin2Pcode",
    "District",
    "admin1Name_en",
    "AREA_SQKM",
    "T_TL",
    "M_TL",
    "F_TL",
    "Inernet_Total_15 year+",
    "Inernet_Male_15 year+",
    "Inernet_Female_15 year+",
    "Mobile Phone_Total_15 year+",
    "Mobile Phone_Male_15 year+",
    "Mobile Phone_Female_15 year+",
    "4G Avg. UE throughput DL (MB)",
    "Literacy Rate_7year+_Overall",
    "Literacy Rate_7year+_Male",
    "Literacy Rate_7year+_Female",
    "Employment_Rate",
    "Employment_Rate_Male",
    "Employment_Rate_Female",
    "Have financial account_Overall",
    "Have financial account_Male",
    "Have financial account_Female",
    "Mobile Bank Account_Overall",
    "Mobile Bank Account_Male",
    "Mobile Bank Account_Female",
    "National Grid_%",
    # "Solar Power_%",
    "No Electricity Connection_%",
    "Poverty headcount ratio (%)",
    "Extreme poverty headcount ratio (%)",
    "Percentage of population in bottom 40% (%)",
    "Num_op_x_towers",
    "Cell_tower_density",
    "Tea_State_Count",
    "mean_distance",
    "min_distance",
    "max_distance",
    "median_distance",
    "25_perc_distance",
    "75_perc_distance",
    "std_dev_distance",
    "mean_num_tower_500m",
    "mean_num_tower_1000m",
    "mean_num_tower_2000m",
    "mean_num_tower_5000m",
    "mean_num_tower_10000m",
]

ALL_THANA_COLUMNS = [
    "geometry",
    "admin1Name_en",
    "admin2Name_en",
    "admin3Name_en",
    "admin3Pcode",
    "AREA_SQKM",
    "T_TL",
    "M_TL",
    "F_TL",
    "Num_op_x_towers",
    "Cell_tower_density",
    "Tea_State_Count",
    "Poverty headcount ratio (%)",
    "Extreme poverty headcount ratio (%)",
    "Percentage of population in bottom 40% (%)",
    "mean_distance",
    "min_distance",
    "max_distance",
    "median_distance",
    "25_perc_distance",
    "75_perc_distance",
    "std_dev_distance",
    "mean_num_tower_500m",
    "mean_num_tower_1000m",
    "mean_num_tower_2000m",
    "mean_num_tower_5000m",
    "mean_num_tower_10000m",
]


INTERNET_BBS_COLS = [
    "District",
    "Inernet_Total_15 year+",
    "Inernet_Male_15 year+",
    "Inernet_Female_15 year+",
]

MOBILE_BBS_COLS = [
    "District",
    "Mobile Phone_Total_15 year+",
    "Mobile Phone_Male_15 year+",
    "Mobile Phone_Female_15 year+",
]

LITERACY_BBS_COLS = [
    "District",
    "Literacy Rate_7year+_Overall",
    "Literacy Rate_7year+_Male",
    "Literacy Rate_7year+_Female",
]

EMPLOY_BBS_COLS = [
    "District",
    "Overall_Working_Status_5 Year+",
    "Overall_Working_Status_5 Year+_Male",
    "Overall_Working_Status_5 Year+_Female",
    "Overall_Employed_Working_Status_5 Year+",
    "Overall_Employed_Working_Status_5 Year+_Male",
    "Overall_Employed_Working_Status_5 Year+_Female",
]

FINANCIAL_BBS_COLS = [
    "District",
    "Have financial account_Overall",
    "Have financial account_Male",
    "Have financial account_Female",
]

MOBILE_BANK_BBS_COLS = [
    "District",
    "Mobile Bank Account_Overall",
    "Mobile Bank Account_Male",
    "Mobile Bank Account_Female",
]

ELECTRICITY_BBS_COLS = [
    "District",
    "National Grid_%",
    # "Solar Power_%",
    "No Electricity Connection_%",
]

POVERTY_COLS = [
    "admin2Pcode",
    "Poverty headcount ratio (%)",
    "Extreme poverty headcount ratio (%)",
    "Percentage of population in bottom 40% (%)",
]

POVERTY_THANA_COLS = [
    "admin3Pcode",
    "Poverty headcount ratio (%)",
    "Extreme poverty headcount ratio (%)",
    "Percentage of population in bottom 40% (%)",
]

BBS_DISTRICT_MAP = {
    "Barishal": "Barisal",
    "Bogura": "Bogra",
    "Brahmanbaria": "Brahamanbaria",
    "Chattogram": "Chittagong",
    "Cumilla": "Comilla",
    "Jashore": "Jessore",
    "Moulvibazar": "Maulvibazar",
    "Chapainababganj": "Nawabganj",
}

TEA_THANA_MAP = {
    "Moulvibazar": "Maulvi Bazar Sadar",
    "Tetulia": "Tentulia",
    "Baghaichhari": "Baghai Chhari",
    "Habiganj": "Habiganj Sadar",
    "Sylhet": "Sylhet Sadar",
    "Jaintapur": "Jaintiapur",
    "Panchagarh": "Panchagarh Sadar",
    "Bhujpur": "Fatikchhari",
}

TEA_DISTRICT_MAP = {"Moulvibazar": "Maulvibazar", "Chattogram": "Chittagong"}

XYZ_JOIN_COLS = [
    "geometry",
    "pop_den",
    "nearest_distance",
    "num_tower_500m",
    "num_tower_1000m",
    "num_tower_2000m",
    "num_tower_5000m",
    "num_tower_10000m",
]

DISTANCE_RAD_METRIC_INIT_COLS = [
    "pop_den",
    "nearest_distance",
    "num_tower_500m",
    "num_tower_1000m",
    "num_tower_2000m",
    "num_tower_5000m",
    "num_tower_10000m",
]


### CONSTANTS for make_map_files.py

COLOR_MAP = {
    "Inernet_Total_15 year+": "RdYlGn",
    "Inernet_Male_15 year+": "RdYlGn",
    "Inernet_Female_15 year+": "RdYlGn",
    "Mobile Phone_Total_15 year+": "RdYlGn",
    "Mobile Phone_Male_15 year+": "RdYlGn",
    "Mobile Phone_Female_15 year+": "RdYlGn",
    "4G Avg. UE throughput DL (MB)": "RdYlGn",
    "Literacy Rate_7year+_Overall": "RdYlGn",
    "Literacy Rate_7year+_Male": "RdYlGn",
    "Literacy Rate_7year+_Female": "RdYlGn",
    "Employment_Rate": "RdYlGn",
    "Employment_Rate_Male": "RdYlGn",
    "Employment_Rate_Female": "RdYlGn",
    "Have financial account_Overall": "RdYlGn",
    "Have financial account_Male": "RdYlGn",
    "Have financial account_Female": "RdYlGn",
    "Mobile Bank Account_Overall": "RdYlGn",
    "Mobile Bank Account_Male": "RdYlGn",
    "Mobile Bank Account_Female": "RdYlGn",
    "National Grid_%": "RdYlGn",
    "Solar Power_%": "RdYlGn",
    "No Electricity Connection_%": "RdYlGn_r",
    "Poverty headcount ratio (%)": "RdYlGn_r",
    "Extreme poverty headcount ratio (%)": "RdYlGn_r",
    "Percentage of population in bottom 40% (%)": "RdYlGn_r",
    "Num_op_x_towers": "RdYlGn",
    "Cell_tower_density": "RdYlGn",
    "mean_num_tower_500m": "RdYlGn",
    "mean_num_tower_1000m": "RdYlGn",
    "mean_num_tower_2000m": "RdYlGn",
    "mean_num_tower_5000m": "RdYlGn",
    "mean_num_tower_10000m": "RdYlGn",
    "mean_distance": "RdYlGn_r",
    "min_distance": "RdYlGn_r",
    "max_distance": "RdYlGn_r",
    "median_distance": "RdYlGn_r",
    "25_perc_distance": "RdYlGn_r",
    "75_perc_distance": "RdYlGn_r",
    "std_dev_distance": "RdYlGn_r",
}


### CONSTANTS for make_map_files.py and dashboard.py

COL_NAME_MAP = {
    "T_TL": "Total Population",
    "M_TL": "Male Population",
    "F_TL": "Female Population",
    "AREA_SQKM": "Area (in sqkm)",
    "admin3Name_en": "Upazila",
    "tea_garden_bn": "Tea Garden Name (BN)",
    "tea_garden_en": "Tea Garden Name (EN)",
    "reg_workers": "Registered Workers",
    "unreg_workers": "Unregistered Workers",
    "tot_workers": "Total Tea Estate Workers",
    "tea_estate_pop": "Tea Estate Population",
    "perc_unreg_workers": "Percentage Unregistered Workers",
    "Inernet_Total_15 year+": "% of Total 15+ population using Internet",
    "Inernet_Male_15 year+": "% of Male 15+ population using Internet",
    "Inernet_Female_15 year+": "% of Female 15+ population using Internet",
    "Mobile Phone_Total_15 year+": "% of Total 15+ population having Mobile Phone",
    "Mobile Phone_Male_15 year+": "% of Male 15+ population having Mobile Phone",
    "Mobile Phone_Female_15 year+": "% of Female 15+ population having Mobile Phone",
    "4G Avg. UE throughput DL (MB)": "4G Download Speed (Mbps)",
    "Literacy Rate_7year+_Overall": "Literacy Rate Overall of Age 7+ (%)",
    "Literacy Rate_7year+_Male": "Literacy Rate Male of Age 7+ (%)",
    "Literacy Rate_7year+_Female": "Literacy Rate Female of Age 7+ (%)",
    "Employment_Rate": "Employment Rate Overall (%)",
    "Employment_Rate_Male": "Employment Rate of Male (%)",
    "Employment_Rate_Female": "Employment Rate of Female (%)",
    "Have financial account_Overall": "% of Total population having Financial Account",
    "Have financial account_Male": "% of Male population having Financial Account",
    "Have financial account_Female": "% of Female population having Financial Account",
    "Mobile Bank Account_Overall": "% of Total population having Moble Bank Account",
    "Mobile Bank Account_Male": "% of Male population having Moble Bank Account",
    "Mobile Bank Account_Female": "% of Female population having Moble Bank Account",
    "National Grid_%": "% of population with National Grid as main electricity source",
    "Solar Power_%": "% of population with Solar Power as main electricity source",
    "No Electricity Connection_%": "% of population without electricity connection",
    "Poverty headcount ratio (%)": "% of population below official upper national poverty line",
    "Extreme poverty headcount ratio (%)": "% of population below official lower national poverty line",
    "Percentage of population in bottom 40% (%)": "% of population in bottom 40% of consumption distribution",
    "Num_op_x_towers": "Number of Operator X Towers in region",
    "Cell_tower_density": "Density of Operator X Towers(# per sqkm)",
    "Tea_State_Count": "Number of Tea States",
    "mean_distance": "Mean Distance to Nearest Tower (in m)",
    "min_distance": "Min Distance to Nearest Tower (in m)",
    "max_distance": "Max Distance to Nearest Tower (in m)",
    "median_distance": "Median Distance to Nearest Tower (in m)",
    "25_perc_distance": "First Quartile Distance to Nearest Tower (in m)",
    "75_perc_distance": "3rd Quartile Distance to Nearest Tower (in m)",
    "std_dev_distance": "Std Dev of Distance to Nearest Tower (in m)",
    "mean_num_tower_500m": "Mean Number of Towers in 0.5 km",
    "mean_num_tower_1000m": "Mean Number of Towers in 1 km",
    "mean_num_tower_2000m": "Mean Number of Towers in 2 km",
    "mean_num_tower_5000m": "Mean Number of Towers in 5 km",
    "mean_num_tower_10000m": "Mean Number of Towers in 10 km",
    "nearest_distance": "Distance to nearest Tower (in m)",
    "num_tower_500m": "Number of Towers in 0.5 km",
    "num_tower_1000m": "Number of Towers in 1 km",
    "num_tower_2000m": "Number of Towers in 2 km",
    "num_tower_5000m": "Number of Towers in 5 km",
    "num_tower_10000m": "Number of Towers in 10 km",
}


DISTRICT_ONLY_VAR_COLS = [
    "Inernet_Total_15 year+",
    "Inernet_Male_15 year+",
    "Inernet_Female_15 year+",
    "Mobile Phone_Total_15 year+",
    "Mobile Phone_Male_15 year+",
    "Mobile Phone_Female_15 year+",
    "4G Avg. UE throughput DL (MB)",
    "Literacy Rate_7year+_Overall",
    "Literacy Rate_7year+_Male",
    "Literacy Rate_7year+_Female",
    "Employment_Rate",
    "Employment_Rate_Male",
    "Employment_Rate_Female",
    "Have financial account_Overall",
    "Have financial account_Male",
    "Have financial account_Female",
    "Mobile Bank Account_Overall",
    "Mobile Bank Account_Male",
    "Mobile Bank Account_Female",
    "National Grid_%",
    # "Solar Power_%",
    "No Electricity Connection_%",
]

THANA_VAR_COLS = [
    "Poverty headcount ratio (%)",
    "Extreme poverty headcount ratio (%)",
    "Percentage of population in bottom 40% (%)",
    "Num_op_x_towers",
    "Cell_tower_density",
    "mean_distance",
    # "min_distance",
    # "max_distance",
    # "median_distance",
    # "25_perc_distance",
    # "75_perc_distance",
    # "std_dev_distance",
    # "mean_num_tower_500m",
    # "mean_num_tower_1000m",
    # "mean_num_tower_2000m",
    # "mean_num_tower_5000m",
    # "mean_num_tower_10000m",
]

DISTRICT_VAR_COLS = DISTRICT_ONLY_VAR_COLS + THANA_VAR_COLS

TEA_VAR_COLS = [
    "nearest_distance",
    # "num_tower_500m",
    # "num_tower_1000m",
    # "num_tower_2000m",
    # "num_tower_5000m",
    # "num_tower_10000m",
]


### CONSTANTS for dashboard.py

TEA_TABLE_COLS = [
    "tea_garden_bn",
    "tea_garden_en",
    "tot_workers",
    "perc_unreg_workers",
    "tea_estate_pop",
] + TEA_VAR_COLS

HEATMAP_DEFAULT_COLS = [
    "Inernet_Total_15 year+",
    "Mobile Phone_Total_15 year+",
    "4G Avg. UE throughput DL (MB)",
    "Cell_tower_density",
    "mean_distance",
    "Literacy Rate_7year+_Overall",
    "Mobile Bank Account_Overall",
    "National Grid_%",
    "Poverty headcount ratio (%)",
]

HEATMAP_DEFAULT_COLS_MAPPED = [COL_NAME_MAP[i] for i in HEATMAP_DEFAULT_COLS]
