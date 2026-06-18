import geopandas as gpd
import numpy as np
import pandas as pd

from constants import (
    ALL_DISTRICT_COLUMNS,
    ALL_THANA_COLUMNS,
    BBS_DISTRICT_MAP,
    DISTANCE_RAD_METRIC_INIT_COLS,
    ELECTRICITY_BBS_COLS,
    EMPLOY_BBS_COLS,
    FINANCIAL_BBS_COLS,
    GENDER_PARITY_DICT,
    HIES_DISTRICT_MAP,
    INCOME_PRICE_COLS,
    INTERNET_BBS_COLS,
    LITERACY_BBS_COLS,
    MOBILE_BANK_BBS_COLS,
    MOBILE_BBS_COLS,
    POVERTY_COLS,
    POVERTY_THANA_COLS,
    TEA_DISTRICT_MAP,
    TEA_THANA_MAP,
    USD_BDT_EXCHANGE_RATE_2025,
    XYZ_JOIN_COLS,
)

NUM_500_MAP = {(0, 2): "bad", (2, 5): "ok", (5, float("inf")): "good"}
NUM_1000_MAP = {(0, 4): "bad", (4, 11): "ok", (11, float("inf")): "good"}
NUM_2000_MAP = {(0, 9): "bad", (9, 26): "ok", (26, float("inf")): "good"}
NUM_5000_MAP = {(0, 26): "bad", (26, 81): "ok", (81, float("inf")): "good"}
NUM_10000_MAP = {(0, 76): "bad", (76, 251): "ok", (251, float("inf")): "good"}

DIST_MAP = {(0, 500): "good", (500, 1000): "ok", (1000, float("inf")): "bad"}

RADIUS_DISTANCES = [500, 1000, 2000, 5000, 10000]
RADIUS_MAPS = [NUM_500_MAP, NUM_1000_MAP, NUM_2000_MAP, NUM_5000_MAP, NUM_10000_MAP]


def get_bbs_data() -> pd.DataFrame:
    internet_bbs = pd.read_excel(
        "data/raw/bangladesh_bbs_population-and-housing-census-dataset_2022_admin-02.xlsx",
        sheet_name="Internet User",
    )
    mobile_bbs = pd.read_excel(
        "data/raw/bangladesh_bbs_population-and-housing-census-dataset_2022_admin-02.xlsx",
        sheet_name=" Population having Mobile Phone",
    )

    literacy_bbs = pd.read_excel(
        "data/raw/bangladesh_bbs_population-and-housing-census-dataset_2022_admin-02.xlsx",
        sheet_name="Literacy Rate_Aged 7 Yrs & Abov",
    )
    employ_bbs = pd.read_excel(
        "data/raw/bangladesh_bbs_population-and-housing-census-dataset_2022_admin-02.xlsx",
        sheet_name=" Aged 5 Yrs & Above_Working Sta",
    )
    financial_bbs = pd.read_excel(
        "data/raw/bangladesh_bbs_population-and-housing-census-dataset_2022_admin-02.xlsx",
        sheet_name="Having Account in Financial",
    )
    mobile_bank_bbs = pd.read_excel(
        "data/raw/bangladesh_bbs_population-and-housing-census-dataset_2022_admin-02.xlsx",
        sheet_name=" Having Mobile Banking Account",
    )
    electricity_bbs = pd.read_excel(
        "data/raw/bangladesh_bbs_population-and-housing-census-dataset_2022_admin-02.xlsx",
        sheet_name=" Main Source of Electricity ",
    )
    bbs_data = (
        internet_bbs[INTERNET_BBS_COLS]
        .merge(
            mobile_bbs[MOBILE_BBS_COLS],
            on="District",
            validate="one_to_one",
        )
        .merge(
            literacy_bbs[LITERACY_BBS_COLS],
            on="District",
            validate="one_to_one",
        )
        .merge(
            employ_bbs[EMPLOY_BBS_COLS],
            on="District",
            validate="one_to_one",
        )
        .merge(financial_bbs[FINANCIAL_BBS_COLS])
        .merge(mobile_bank_bbs[MOBILE_BANK_BBS_COLS])
        .merge(electricity_bbs[ELECTRICITY_BBS_COLS])
    ).replace({"District": BBS_DISTRICT_MAP})

    bbs_data["Employment_Rate"] = (
        (
            bbs_data["Overall_Employed_Working_Status_5 Year+"]
            / bbs_data["Overall_Working_Status_5 Year+"]
        )
        * 100
    ).round(2)
    bbs_data["Employment_Rate_Male"] = (
        (
            bbs_data["Overall_Employed_Working_Status_5 Year+_Male"]
            / bbs_data["Overall_Working_Status_5 Year+_Male"]
        )
        * 100
    ).round(2)
    bbs_data["Employment_Rate_Female"] = (
        (
            bbs_data["Overall_Employed_Working_Status_5 Year+_Female"]
            / bbs_data["Overall_Working_Status_5 Year+_Female"]
        )
        * 100
    ).round(2)

    for k, v in GENDER_PARITY_DICT.items():
        bbs_data[k] = ((bbs_data[v[0]] / bbs_data[v[1]]) * 100).round(2)

    return bbs_data


def get_hies_income_affordability_data() -> pd.DataFrame:
    hies_survey_filename = "data/raw/HH_SEC_4A.dta"

    df = pd.read_stata(hies_survey_filename, convert_categoricals=False).dropna(
        subset="s4bq16"
    )
    price_data = pd.read_excel(
        "data/raw/ITU_ICTPriceBaskets_2008-2025.xlsx", sheet_name="economies_2008-2025"
    )
    val_labels = dict()
    with pd.io.stata.StataReader(hies_survey_filename) as reader:
        val_labels = reader.value_labels()

    df["s4aq05b"] = df["s4aq05b"].astype(int)
    df["s4aq05b"] = df["s4aq05b"].map(val_labels["S4AQ05B"]).replace(HIES_DISTRICT_MAP)
    df_grouped = (
        df.groupby("s4aq05b", as_index=False)["s4bq16"]
        .agg(["mean", "count"])
        .rename(
            columns={
                "s4aq05b": "District",
                "mean": "Monthly_income",
                "count": "Num_Income_Samples",
            }
        )
    )

    usd_5GB_price = price_data[
        (price_data["Economy"] == "Bangladesh")
        & (price_data["Unit"] == "USD")
        & (price_data[2025].notnull())
        & (price_data["Code"] == "i271mb_5GB$")
    ].iloc[0][2025]

    df_grouped["Data_Cost_perc_income"] = (
        ((usd_5GB_price * USD_BDT_EXCHANGE_RATE_2025) / df_grouped["Monthly_income"])
        * 100
    ).round(2)
    df_grouped["Monthly_income"] = df_grouped["Monthly_income"].round(2)
    return df_grouped[INCOME_PRICE_COLS]


def get_poverty_df(adm_data: pd.DataFrame) -> pd.DataFrame:
    poverty_df = pd.read_excel("data/raw/zila_and_upazila_data/zila_indicators.xlsx")
    poverty_df["admin2Pcode"] = "BD" + poverty_df["DisGeoCode"].astype(str)

    poverty_df["combined"] = poverty_df.apply(
        func=lambda x: (x["Zila Name"].title(),), axis=1
    )
    adm_data["combined"] = adm_data.apply(func=lambda x: (x["admin2Name_en"],), axis=1)
    temp_pcode_dict = (
        adm_data.loc[
            adm_data["admin2Pcode"].isin(
                set(adm_data["admin2Pcode"]) - set(poverty_df["admin2Pcode"])
            )
        ]
        .set_index("combined")["admin2Pcode"]
        .to_dict()
    )
    adm_data = adm_data.drop(columns=["combined"])

    poverty_df.loc[
        poverty_df["admin2Pcode"].isin(
            set(poverty_df["admin2Pcode"]) - set(adm_data["admin2Pcode"])
        ),
        "admin2Pcode",
    ] = poverty_df.loc[
        poverty_df["admin2Pcode"].isin(
            set(poverty_df["admin2Pcode"]) - set(adm_data["admin2Pcode"])
        ),
        "combined",
    ].map(temp_pcode_dict)
    return poverty_df


def get_poverty_df_thana(adm_data: pd.DataFrame) -> pd.DataFrame:
    poverty_df_thana = pd.read_excel(
        "data/raw/zila_and_upazila_data/upazila_indicators.xlsx"
    )
    poverty_gdf_thana = gpd.read_file(
        "data/raw/gis_data/gdb/Bangladesh_Data.gdb", layer="Bangladesh_Upazilas"
    )[["UpazCode", "Division_N", "District_N", "Thana_Name"]].rename(
        columns={
            "Division_N": "Division Name",
            "District_N": "Zila Name",
            "Thana_Name": "Upazila Name",
        }
    )

    poverty_gdf_thana.loc[poverty_gdf_thana["UpazCode"] == 507088, "Upazila Name"] = (
        "SHIBGANJ"
    )

    poverty_df_thana["combined"] = poverty_df_thana.apply(
        func=lambda x: (x["Division Name"], x["Zila Name"], x["Upazila Name"]), axis=1
    )
    poverty_gdf_thana["combined"] = poverty_gdf_thana.apply(
        func=lambda x: (x["Division Name"], x["Zila Name"], x["Upazila Name"]), axis=1
    )
    poverty_gdf_thana.loc[
        poverty_gdf_thana["combined"].isin(
            set(poverty_gdf_thana["combined"]) - set(poverty_df_thana["combined"])
        ),
        "Upazila Name",
    ] = poverty_gdf_thana.apply(
        lambda x: x["Upazila Name"].rstrip("(" + x["Zila Name"] + ")").strip(), axis=1
    ).loc[
        poverty_gdf_thana["combined"].isin(
            set(poverty_gdf_thana["combined"]) - set(poverty_df_thana["combined"])
        )
    ]
    poverty_df_thana = poverty_df_thana.drop(columns="combined")
    poverty_gdf_thana = poverty_gdf_thana.drop(columns="combined")

    poverty_df_thana = poverty_df_thana.merge(
        pd.DataFrame(poverty_gdf_thana),
        on=["Division Name", "Zila Name", "Upazila Name"],
        validate="one_to_one",
    )
    poverty_df_thana["UpazCode"] = poverty_df_thana["UpazCode"].astype(int)

    poverty_df_thana.loc[poverty_df_thana["UpazCode"] == 303985, "UpazCode"] = 453985

    poverty_df_thana["admin3Pcode"] = "BD" + poverty_df_thana["UpazCode"].astype(str)

    poverty_df_thana["combined"] = poverty_df_thana.apply(
        func=lambda x: (x["Zila Name"].title(), x["Upazila Name"].title()), axis=1
    )
    adm_data["combined"] = adm_data.apply(
        func=lambda x: (x["admin2Name_en"], x["admin3Name_en"]), axis=1
    )

    adm_pcode_dict = (
        adm_data.loc[
            adm_data["admin3Pcode"].isin(
                set(adm_data["admin3Pcode"]) - set(poverty_df_thana["admin3Pcode"])
            )
        ]
        .set_index("combined")["admin3Pcode"]
        .to_dict()
    )
    adm_data = adm_data.drop(columns=["combined"])

    poverty_df_thana.loc[
        poverty_df_thana["admin3Pcode"].isin(
            set(poverty_df_thana["admin3Pcode"]) - set(adm_data["admin3Pcode"])
        ),
        "admin3Pcode",
    ] = poverty_df_thana.loc[
        poverty_df_thana["admin3Pcode"].isin(
            set(poverty_df_thana["admin3Pcode"]) - set(adm_data["admin3Pcode"])
        ),
        "combined",
    ].map(adm_pcode_dict)
    return poverty_df_thana


def agg_func(in_df: pd.DataFrame) -> pd.Series:
    avg = np.average(in_df["nearest_distance"], weights=in_df["pop_den"])
    std_dev = np.sqrt(
        np.average(np.square(in_df["nearest_distance"] - avg), weights=in_df["pop_den"])
    )
    distance_metrics = {
        "mean_distance": avg,
        "min_distance": np.min(in_df["nearest_distance"]),
        "max_distance": np.max(in_df["nearest_distance"]),
        "median_distance": np.quantile(
            in_df["nearest_distance"],
            q=0.5,
            method="inverted_cdf",
            weights=in_df["pop_den"],
        ).item(),
        "25_perc_distance": np.quantile(
            in_df["nearest_distance"],
            q=0.25,
            method="inverted_cdf",
            weights=in_df["pop_den"],
        ).item(),
        "75_perc_distance": np.quantile(
            in_df["nearest_distance"],
            q=0.75,
            method="inverted_cdf",
            weights=in_df["pop_den"],
        ).item(),
        "std_dev_distance": std_dev,
    }
    tower_radius_metrics = {
        f"mean_num_tower_{i}m": np.average(
            in_df[f"num_tower_{i}m"], weights=in_df["pop_den"]
        )
        for i in RADIUS_DISTANCES
    }
    return pd.Series(
        {k: round(v) for k, v in distance_metrics.items()} | tower_radius_metrics
    )


def get_quality(metric: int, metric_dict: dict[tuple[float, float], str]) -> str:
    for (lower_bound, upper_bound), v in metric_dict.items():
        if (metric >= lower_bound) and (metric < upper_bound):
            return v
    return "Invalid"


def get_num_tower_radius_map(
    input_df: gpd.GeoDataFrame, tower_df: gpd.GeoDataFrame, radius: int
) -> dict[int, int]:
    return (
        input_df.to_crs(epsg=3106)
        .buffer(radius)
        .reset_index()
        .rename(columns={"index": "ind", 0: "geometry"})
        .set_geometry("geometry")
        .to_crs(epsg=4326)
        .sjoin(tower_df)
        .groupby("ind")
        .size()
        .to_dict()
    )


def get_dist_num_tower_rad_metrics(
    input_df: gpd.GeoDataFrame, tower_df: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    input_df["ind"] = range(len(input_df))
    nearest_map = (
        input_df.to_crs(epsg=3106)
        .sjoin_nearest(tower_df.to_crs(epsg=3106), distance_col="nearest_distance")
        .set_index("ind")["nearest_distance"]
        .to_dict()
    )
    input_df["nearest_distance"] = input_df["ind"].map(nearest_map).fillna(0)

    for i in RADIUS_DISTANCES:
        rad_map = get_num_tower_radius_map(input_df, tower_df, i)
        input_df[f"num_tower_{i}m"] = input_df["ind"].map(rad_map).fillna(0).astype(int)

    return input_df.drop(columns=["ind"])


def get_xyz_data(tower_df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    xyz = pd.read_csv("data/raw/bgd_pd_2020_1km_UNadj_ASCII_XYZ.csv").rename(
        columns={"X": "lon", "Y": "lat", "Z": "pop_den"}
    )
    xyz = gpd.GeoDataFrame(
        xyz, geometry=gpd.points_from_xy(x=xyz.lon, y=xyz.lat, crs="EPSG:4326")
    )
    return get_dist_num_tower_rad_metrics(xyz, tower_df)


def get_adm_dist_metrics(
    in_df: gpd.GeoDataFrame, adm_data: gpd.GeoDataFrame, adm_join_col: str
) -> pd.DataFrame:
    selected_cols = [adm_join_col] + DISTANCE_RAD_METRIC_INIT_COLS
    return pd.DataFrame(
        adm_data[["geometry", adm_join_col]]
        .sjoin(in_df[XYZ_JOIN_COLS])[selected_cols]
        .groupby(adm_join_col, as_index=False)
        .apply(agg_func)
    )


def get_cell_tower_metrics(
    adm_data: gpd.GeoDataFrame, tower_df: gpd.GeoDataFrame, adm_join_col: str
) -> pd.DataFrame:
    cell_tower_dict = adm_data.sjoin(tower_df).groupby(adm_join_col).size().to_dict()

    adm_data["Num_op_x_towers"] = adm_data[adm_join_col].map(cell_tower_dict)
    adm_data["Cell_tower_density"] = adm_data["Num_op_x_towers"] / adm_data["AREA_SQKM"]

    return pd.DataFrame(
        adm_data[[adm_join_col, "Num_op_x_towers", "Cell_tower_density"]]
    )


def get_tea_lat_lon(tower_df: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    t_lat_lon = pd.read_csv("data/intermediate/tea_lat_lon.csv")

    t_lat_lon = gpd.GeoDataFrame(
        data=t_lat_lon,
        geometry=gpd.points_from_xy(x=t_lat_lon.lon, y=t_lat_lon.lat, crs="EPSG:4326"),
    )
    t_lat_lon = get_dist_num_tower_rad_metrics(t_lat_lon, tower_df)
    for i, rad_map in zip(RADIUS_DISTANCES, RADIUS_MAPS):
        t_lat_lon[f"num_tower_{i}m_quality"] = t_lat_lon[f"num_tower_{i}m"].apply(
            get_quality, metric_dict=rad_map
        )

    t_lat_lon["nearest_distance_quality"] = t_lat_lon["nearest_distance"].apply(
        get_quality, metric_dict=DIST_MAP
    )
    t_lat_lon["perc_unreg_workers"] = (
        t_lat_lon["unreg_workers"] / t_lat_lon["tot_workers"]
    ) * 100
    return t_lat_lon


if __name__ == "__main__":
    adm_data_2 = gpd.read_file(
        "data/raw/BGD_AdminBoundaries_candidate.gdb",
        layer="bgd_admbnda_adm2_bbs_20201113",
    )
    adm_data_table_2 = pd.read_excel(
        "data/raw/bgd_adminboundaries_tabulardata.xlsx", sheet_name="ADM2"
    )
    adm_pop_2 = pd.read_excel(
        "data/raw/bgd_admpop_2022.xlsx", sheet_name="bgd_admpop_adm2_2022"
    )
    adm_data_3 = gpd.read_file(
        "data/raw/BGD_AdminBoundaries_candidate.gdb",
        layer="bgd_admbnda_adm3_bbs_20201113",
    )
    adm_data_table_3 = pd.read_excel(
        "data/raw/bgd_adminboundaries_tabulardata.xlsx", sheet_name="ADM3"
    )
    adm_pop_3 = pd.read_excel(
        "data/raw/bgd_admpop_2022.xlsx", sheet_name="bgd_admpop_adm3_2022"
    )

    bbs_data = get_bbs_data()

    net_speed_df = pd.read_excel(
        "data/raw/qos_radio_network_kpi_2026-05-19.xlsx", sheet_name="Sheet1", nrows=64
    ).rename(columns={"Distric": "District"})
    hies_income_affordability_df = get_hies_income_affordability_data()
    bbs_data = bbs_data.merge(net_speed_df, on="District", validate="one_to_one").merge(
        hies_income_affordability_df, on="District", validate="one_to_one"
    )

    assert len(bbs_data) == 64, "There should be 64 Districts"

    adm_data_2 = adm_data_2.merge(
        adm_data_table_2[["ADM2_EN", "AREA_SQKM"]],
        left_on="admin2Name_en",
        right_on="ADM2_EN",
        validate="one_to_one",
    )
    adm_data_2 = adm_data_2.merge(
        adm_pop_2[["ADM2_NAME", "T_TL", "M_TL", "F_TL"]],
        left_on="admin2Name_en",
        right_on="ADM2_NAME",
        validate="one_to_one",
    )
    adm_data_3 = adm_data_3.merge(
        adm_data_table_3[["ADM3_PCODE", "AREA_SQKM"]],
        left_on="admin3Pcode",
        right_on="ADM3_PCODE",
        validate="one_to_one",
    )
    adm_data_3 = adm_data_3.merge(
        adm_pop_3[["ADM3_PCODE", "T_TL", "M_TL", "F_TL"]],
        on="ADM3_PCODE",
        validate="one_to_one",
    )

    adm_data_2 = adm_data_2.merge(
        bbs_data,
        left_on="admin2Name_en",
        right_on="District",
        validate="one_to_one",
    )

    poverty_df = get_poverty_df(adm_data_2[["admin2Name_en", "admin2Pcode"]].copy())
    poverty_df_thana = get_poverty_df_thana(
        adm_data_3[["admin2Name_en", "admin3Name_en", "admin3Pcode"]].copy()
    )

    adm_data_2 = adm_data_2.merge(
        poverty_df[POVERTY_COLS],
        on="admin2Pcode",
        validate="one_to_one",
    )

    adm_data_3 = adm_data_3.merge(
        poverty_df_thana[POVERTY_THANA_COLS],
        on="admin3Pcode",
        validate="one_to_one",
    )

    op_x_tower_loc = pd.read_excel(
        "data/raw/tower.xlsx", usecols=[2, 3], skiprows=3
    ).drop_duplicates(ignore_index=True)
    op_x_tower_loc = gpd.GeoDataFrame(
        op_x_tower_loc,
        geometry=gpd.points_from_xy(
            x=op_x_tower_loc.Lon, y=op_x_tower_loc.Lat, crs="EPSG:4326"
        ),
    )

    district_cell_tower_metrics = get_cell_tower_metrics(
        adm_data_2[["geometry", "admin2Name_en", "AREA_SQKM"]].copy(),
        op_x_tower_loc,
        "admin2Name_en",
    )
    thana_cell_tower_metrics = get_cell_tower_metrics(
        adm_data_3[["geometry", "admin3Pcode", "AREA_SQKM"]].copy(),
        op_x_tower_loc,
        "admin3Pcode",
    )

    adm_data_2 = adm_data_2.merge(
        district_cell_tower_metrics, on="admin2Name_en", validate="one_to_one"
    )
    adm_data_3 = adm_data_3.merge(
        thana_cell_tower_metrics, on="admin3Pcode", validate="one_to_one"
    )

    xyz = get_xyz_data(op_x_tower_loc)

    district_tower_metrics = get_adm_dist_metrics(
        xyz, adm_data_2[["geometry", "admin2Name_en"]].copy(), "admin2Name_en"
    )
    thana_tower_metrics = get_adm_dist_metrics(
        xyz, adm_data_3[["geometry", "admin3Pcode"]].copy(), "admin3Pcode"
    )

    adm_data_2 = adm_data_2.merge(
        district_tower_metrics, on="admin2Name_en", validate="one_to_one"
    )
    adm_data_3 = adm_data_3.merge(
        thana_tower_metrics, on="admin3Pcode", validate="one_to_one"
    )

    df = pd.read_csv("data/raw/tea_estates_extracted.csv").rename(
        columns={"Dakghor": "Post_Office", "Jela": "District"}
    )
    df["Thana"] = df["Thana"].replace(TEA_THANA_MAP)
    df["District"] = df["District"].replace(TEA_DISTRICT_MAP)

    tea_district_dict: dict[str, int] = df.groupby("District").size().to_dict()
    tea_thana_dict: dict[str, int] = df.groupby("Thana").size().to_dict()

    adm_data_2["Tea_State_Count"] = (
        adm_data_2["admin2Name_en"].map(tea_district_dict).fillna(0).astype(int)
    )

    adm_data_3["Tea_State_Count"] = (
        adm_data_3["admin3Name_en"].map(tea_thana_dict).fillna(0).astype(int)
    )

    t_lat_lon = get_tea_lat_lon(op_x_tower_loc)

    final_df = adm_data_2[ALL_DISTRICT_COLUMNS]
    final_df.to_file("data/intermediate/final_viz.gpkg")

    adm_data_3[ALL_THANA_COLUMNS].to_file("data/intermediate/final_thana_viz.gpkg")
    t_lat_lon.to_file("data/intermediate/tea_data.gpkg")
    pd.DataFrame(t_lat_lon.drop(columns=["geometry", "lat", "lon"])).to_csv(
        "data/final/tea_data.csv", index=False
    )
    pd.DataFrame(final_df.drop(columns=["geometry"])).to_csv(
        "data/final/district_data.csv", index=False
    )
