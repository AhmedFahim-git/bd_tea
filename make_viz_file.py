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
    )


REQD_COLUMNS = [
    "geometry",
    "District",
    "admin1Name_en",
    "AREA_SQKM",
    "T_TL",
    "Inernet_Total_15 year+",
    "Inernet_Male_15 year+",
    "Inernet_Female_15 year+",
    "Mobile Phone_Total_15 year+",
    "Mobile Phone_Male_15 year+",
    "Mobile Phone_Female_15 year+",
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


tea_state_divisions = ["Chittagong", "Sylhet", "Rangpur"]
if __name__ == "__main__":
    adm_data_2 = gpd.read_file(
        "data/BGD_AdminBoundaries_candidate.gdb", layer="bgd_admbnda_adm2_bbs_20201113"
    )
    adm_data_table = pd.read_excel(
        "data/bgd_adminboundaries_tabulardata.xlsx", sheet_name="ADM2"
    )
    adm_pop = pd.read_excel(
        "data/bgd_admpop_2022.xlsx", sheet_name="bgd_admpop_adm2_2022"
    )

    internet_bbs = pd.read_excel(
        "data/bangladesh_bbs_population-and-housing-census-dataset_2022_admin-02.xlsx",
        sheet_name="Internet User",
    ).replace(
        {
            "District": {
                "Barishal": "Barisal",
                "Bogura": "Bogra",
                "Brahmanbaria": "Brahamanbaria",
                "Chattogram": "Chittagong",
                "Cumilla": "Comilla",
                "Jashore": "Jessore",
                "Moulvibazar": "Maulvibazar",
                "Chapainababganj": "Nawabganj",
            }
        }
    )
    mobile_bbs = pd.read_excel(
        "data/bangladesh_bbs_population-and-housing-census-dataset_2022_admin-02.xlsx",
        sheet_name=" Population having Mobile Phone",
    ).replace(
        {
            "District": {
                "Barishal": "Barisal",
                "Bogura": "Bogra",
                "Brahmanbaria": "Brahamanbaria",
                "Chattogram": "Chittagong",
                "Cumilla": "Comilla",
                "Jashore": "Jessore",
                "Moulvibazar": "Maulvibazar",
                "Chapainababganj": "Nawabganj",
            }
        }
    )

    adm_data_2 = adm_data_2.merge(
        adm_data_table[["ADM2_EN", "AREA_SQKM"]],
        left_on="admin2Name_en",
        right_on="ADM2_EN",
        validate="one_to_one",
    )
    adm_data_2 = adm_data_2.merge(
        adm_pop[["ADM2_NAME", "T_TL"]],
        left_on="admin2Name_en",
        right_on="ADM2_NAME",
        validate="one_to_one",
    )
    adm_data_2 = adm_data_2.merge(
        internet_bbs[
            [
                "District",
                "Inernet_Total_15 year+",
                "Inernet_Male_15 year+",
                "Inernet_Female_15 year+",
            ]
        ],
        left_on="admin2Name_en",
        right_on="District",
        validate="one_to_one",
    )
    adm_data_2 = adm_data_2.merge(
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
    df = pd.read_csv("~/Downloads/tea_estates_extracted.csv").rename(
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
        }
    )
    df["District"] = df["District"].replace(
        {"Moulvibazar": "Maulvibazar", "Chattogram": "Chittagong"}
    )
    df["Post_Office"] = df["Post_Office"].replace(
        {"Barachal": "Baramchal", "Satgaon": "Satgoan"}
    )
    tea_dict: dict[str, int] = df.groupby("District").size().to_dict()

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

    cell_tower_dict = (
        adm_data_2.sjoin(op_x_tower_loc).groupby("admin2Name_en").size().to_dict()
    )

    adm_data_2["Num_op_x_towers"] = adm_data_2["admin2Name_en"].map(cell_tower_dict)
    adm_data_2["Cell_tower_density"] = (
        adm_data_2["Num_op_x_towers"] / adm_data_2["AREA_SQKM"]
    )

    adm_data_2["Tea_State_Count"] = adm_data_2["admin2Name_en"].map(tea_dict)
    adm_data_2["Tea_State_Count"] = adm_data_2["Tea_State_Count"].fillna(0)

    distance_metrics = (
        adm_data_2[["geometry", "admin2Name_en"]]
        .sjoin(
            xyz.to_crs(epsg=3106)
            .sjoin_nearest(
                op_x_tower_loc.to_crs(epsg=3106), distance_col="nearest_distance"
            )
            .to_crs(epsg=4326)[["geometry", "pop_den", "nearest_distance"]]
        )[["admin2Name_en", "pop_den", "nearest_distance"]]
        .groupby("admin2Name_en", as_index=False)
        .apply(agg_func)
    )

    final_df = adm_data_2.merge(
        distance_metrics, on="admin2Name_en", validate="one_to_one"
    )[REQD_COLUMNS]
    final_df.to_file("data/final_viz.gpkg")
