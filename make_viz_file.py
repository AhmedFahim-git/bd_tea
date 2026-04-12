import geopandas as gpd
import numpy as np
import pandas as pd


def agg_func(in_df):
    avg = np.average(in_df["nearest_distance"], weights=in_df["pop_den"])
    std_dev = np.sqrt(
        np.average(np.square(in_df["nearest_distance"] - avg), weights=in_df["pop_den"])
    )
    return pd.Series(
        {
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
    ).astype(int)


REQD_DISTRICT_COLUMNS = [
    "geometry",
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
    "Literacy Rate_7year+_Overall",
    "Literacy Rate_7year+_Male",
    "Literacy Rate_7year+_Female",
    "Employment_Rate",
    "Employment_Rate_Male",
    "Employment_Rate_Female",
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
]
REQD_THANA_COLUMNS = [
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
    "mean_distance",
    "min_distance",
    "max_distance",
    "median_distance",
    "25_perc_distance",
    "75_perc_distance",
    "std_dev_distance",
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

tea_state_divisions = ["Chittagong", "Sylhet", "Rangpur"]
if __name__ == "__main__":
    adm_data_2 = gpd.read_file(
        "data/BGD_AdminBoundaries_candidate.gdb", layer="bgd_admbnda_adm2_bbs_20201113"
    )
    adm_data_table_2 = pd.read_excel(
        "data/bgd_adminboundaries_tabulardata.xlsx", sheet_name="ADM2"
    )
    adm_pop_2 = pd.read_excel(
        "data/bgd_admpop_2022.xlsx", sheet_name="bgd_admpop_adm2_2022"
    )
    adm_data_3 = gpd.read_file(
        "data/BGD_AdminBoundaries_candidate.gdb", layer="bgd_admbnda_adm3_bbs_20201113"
    )
    adm_data_table_3 = pd.read_excel(
        "data/bgd_adminboundaries_tabulardata.xlsx", sheet_name="ADM3"
    )
    adm_pop_3 = pd.read_excel(
        "data/bgd_admpop_2022.xlsx", sheet_name="bgd_admpop_adm3_2022"
    )

    internet_bbs = pd.read_excel(
        "data/bangladesh_bbs_population-and-housing-census-dataset_2022_admin-02.xlsx",
        sheet_name="Internet User",
    )
    mobile_bbs = pd.read_excel(
        "data/bangladesh_bbs_population-and-housing-census-dataset_2022_admin-02.xlsx",
        sheet_name=" Population having Mobile Phone",
    )
    literacy_bbs = pd.read_excel(
        "data/bangladesh_bbs_population-and-housing-census-dataset_2022_admin-02.xlsx",
        sheet_name="Literacy Rate_Aged 7 Yrs & Abov",
    )
    employ_bbs = pd.read_excel(
        "data/bangladesh_bbs_population-and-housing-census-dataset_2022_admin-02.xlsx",
        sheet_name=" Aged 5 Yrs & Above_Working Sta",
    )
    bbs_data = (
        internet_bbs[
            [
                "District",
                "Inernet_Total_15 year+",
                "Inernet_Male_15 year+",
                "Inernet_Female_15 year+",
            ]
        ]
        .merge(
            mobile_bbs[
                [
                    "District",
                    "Mobile Phone_Total_15 year+",
                    "Mobile Phone_Male_15 year+",
                    "Mobile Phone_Female_15 year+",
                ]
            ],
            on="District",
            validate="one_to_one",
        )
        .merge(
            literacy_bbs[
                [
                    "District",
                    "Literacy Rate_7year+_Overall",
                    "Literacy Rate_7year+_Male",
                    "Literacy Rate_7year+_Female",
                ]
            ],
            on="District",
            validate="one_to_one",
        )
        .merge(
            employ_bbs[
                [
                    "District",
                    "Overall_Working_Status_5 Year+",
                    "Overall_Working_Status_5 Year+_Male",
                    "Overall_Working_Status_5 Year+_Female",
                    "Overall_Employed_Working_Status_5 Year+",
                    "Overall_Employed_Working_Status_5 Year+_Male",
                    "Overall_Employed_Working_Status_5 Year+_Female",
                ]
            ],
            on="District",
            validate="one_to_one",
        )
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
    df = pd.read_csv("data/tea_estates_extracted.csv").rename(
        columns={"Dakghor": "Post_Office", "Jela": "District"}
    )
    df["Thana"] = df["Thana"].replace(
        {
            "Moulvibazar": "Maulvi Bazar Sadar",
            "Tetulia": "Tentulia",
            "Baghaichhari": "Baghai Chhari",
            "Habiganj": "Habiganj Sadar",
            "Sylhet": "Sylhet Sadar",
            "Jaintapur": "Jaintiapur",
            "Panchagarh": "Panchagarh Sadar",
            "Bhujpur": "Fatikchhari",
        }
    )
    df["District"] = df["District"].replace(
        {"Moulvibazar": "Maulvibazar", "Chattogram": "Chittagong"}
    )

    tea_district_dict: dict[str, int] = df.groupby("District").size().to_dict()
    tea_thana_dict: dict[str, int] = df.groupby("Thana").size().to_dict()

    xyz = pd.read_csv("data/bgd_pd_2020_1km_UNadj_ASCII_XYZ.csv").rename(
        columns={"X": "lon", "Y": "lat", "Z": "pop_den"}
    )
    xyz = gpd.GeoDataFrame(
        xyz, geometry=gpd.points_from_xy(x=xyz.lon, y=xyz.lat, crs="EPSG:4326")
    )

    op_x_tower_loc = pd.read_excel(
        "data/test.xlsx", usecols=[2, 3], skiprows=3
    ).drop_duplicates(ignore_index=True)
    op_x_tower_loc = gpd.GeoDataFrame(
        op_x_tower_loc,
        geometry=gpd.points_from_xy(
            x=op_x_tower_loc.Lon, y=op_x_tower_loc.Lat, crs="EPSG:4326"
        ),
    )
    xyz_nearest_tower = (
        xyz.to_crs(epsg=3106)
        .sjoin_nearest(
            op_x_tower_loc.to_crs(epsg=3106), distance_col="nearest_distance"
        )
        .to_crs(epsg=4326)
    )

    cell_tower_district_dict = (
        adm_data_2.sjoin(op_x_tower_loc).groupby("admin2Name_en").size().to_dict()
    )

    adm_data_2["Num_op_x_towers"] = adm_data_2["admin2Name_en"].map(
        cell_tower_district_dict
    )
    adm_data_2["Cell_tower_density"] = (
        adm_data_2["Num_op_x_towers"] / adm_data_2["AREA_SQKM"]
    )

    cell_tower_thana_dict = (
        adm_data_3.sjoin(op_x_tower_loc).groupby("admin3Name_en").size().to_dict()
    )

    adm_data_3["Num_op_x_towers"] = adm_data_3["admin3Name_en"].map(
        cell_tower_thana_dict
    )
    adm_data_3["Cell_tower_density"] = (
        adm_data_3["Num_op_x_towers"] / adm_data_3["AREA_SQKM"]
    )

    adm_data_2["Tea_State_Count"] = adm_data_2["admin2Name_en"].map(tea_district_dict)
    adm_data_2["Tea_State_Count"] = adm_data_2["Tea_State_Count"].fillna(0)

    adm_data_3["Tea_State_Count"] = adm_data_3["admin3Name_en"].map(tea_thana_dict)
    adm_data_3["Tea_State_Count"] = adm_data_3["Tea_State_Count"].fillna(0)

    distance_district_metrics = (
        adm_data_2[["geometry", "admin2Name_en"]]
        .sjoin(xyz_nearest_tower[["geometry", "pop_den", "nearest_distance"]])[
            ["admin2Name_en", "pop_den", "nearest_distance"]
        ]
        .groupby("admin2Name_en", as_index=False)
        .apply(agg_func)
    )

    distance_thana_metrics = (
        adm_data_3[["geometry", "admin3Pcode"]]
        .sjoin(xyz_nearest_tower[["geometry", "pop_den", "nearest_distance"]])[
            ["admin3Pcode", "pop_den", "nearest_distance"]
        ]
        .groupby("admin3Pcode", as_index=False)
        .apply(agg_func)
    )

    final_df = adm_data_2.merge(
        distance_district_metrics, on="admin2Name_en", validate="one_to_one"
    )[REQD_DISTRICT_COLUMNS]
    final_df.to_file("data/final_viz.gpkg")

    adm_data_3.merge(distance_thana_metrics, on="admin3Pcode", validate="one_to_one")[
        REQD_THANA_COLUMNS
    ].to_file("data/final_thana_viz.gpkg")
    pd.DataFrame(final_df.drop(columns=["geometry"])).to_csv(
        "data/district_data.csv", index=False
    )
