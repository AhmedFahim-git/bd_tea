import os
from zipfile import ZIP_LZMA, ZipFile

import folium
import geopandas as gpd

MAP_DISTRICT_DF = gpd.read_file("data/final_viz.gpkg")
MAP_THANA_DF = gpd.read_file("data/final_thana_viz.gpkg")

DISTRICT_VAR_COLS = [
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
    "mean_distance",
    "min_distance",
    "max_distance",
    "median_distance",
    "25_perc_distance",
    "75_perc_distance",
    "std_dev_distance",
]
THANA_VAR_COLS = [
    "Num_op_x_towers",
    "Cell_tower_density",
    "mean_distance",
    "min_distance",
    "max_distance",
    "median_distance",
    "25_perc_distance",
    "75_perc_distance",
    "std_dev_distance",
]
COL_NAME_MAP = {
    "T_TL": "Total Population",
    "M_TL": "Male Population",
    "F_TL": "Female Population",
    "AREA_SQKM": "Area (in sqkm)",
    "admin3Name_en": "Upazila",
    "Inernet_Total_15 year+": "% of Total 15+ population using Internet",
    "Inernet_Male_15 year+": "% of Male 15+ population using Internet",
    "Inernet_Female_15 year+": "% of Female 15+ population using Internet",
    "Mobile Phone_Total_15 year+": "% of Total 15+ population having Mobile Phone",
    "Mobile Phone_Male_15 year+": "% of Male 15+ population having Mobile Phone",
    "Mobile Phone_Female_15 year+": "% of Female 15+ population having Mobile Phone",
    "Literacy Rate_7year+_Overall": "Literacy Rate Overall of Age 7+ (%)",
    "Literacy Rate_7year+_Male": "Literacy Rate Male of Age 7+ (%)",
    "Literacy Rate_7year+_Female": "Literacy Rate Female of Age 7+ (%)",
    "Employment_Rate": "Employment Rate Overall (%)",
    "Employment_Rate_Male": "Employment Rate of Male (%)",
    "Employment_Rate_Female": "Employment Rate of Female (%)",
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
}
COLOR_MAP = {
    "Inernet_Total_15 year+": "RdYlGn",
    "Inernet_Male_15 year+": "RdYlGn",
    "Inernet_Female_15 year+": "RdYlGn",
    "Mobile Phone_Total_15 year+": "RdYlGn",
    "Mobile Phone_Male_15 year+": "RdYlGn",
    "Mobile Phone_Female_15 year+": "RdYlGn",
    "Literacy Rate_7year+_Overall": "RdYlGn",
    "Literacy Rate_7year+_Male": "RdYlGn",
    "Literacy Rate_7year+_Female": "RdYlGn",
    "Employment_Rate": "RdYlGn",
    "Employment_Rate_Male": "RdYlGn",
    "Employment_Rate_Female": "RdYlGn",
    "Num_op_x_towers": "RdYlGn",
    "Cell_tower_density": "RdYlGn",
    "mean_distance": "RdYlGn_r",
    "min_distance": "RdYlGn_r",
    "max_distance": "RdYlGn_r",
    "median_distance": "RdYlGn_r",
    "25_perc_distance": "RdYlGn_r",
    "75_perc_distance": "RdYlGn_r",
    "std_dev_distance": "RdYlGn_r",
}


def write_zip_file(file_base: str, text: str):
    with ZipFile(
        os.path.join("outputs", file_base + ".lzma"), "w", compression=ZIP_LZMA
    ) as myzip:
        myzip.writestr(file_base + ".html", text)


def get_map_html(var_name: str, input_df: gpd.GeoDataFrame, level: str):
    m = folium.Map(location=[23.763889, 90.388889], zoom_start=7, font_size="1.2rem")
    id_col = "District" if level == "District" else "admin3Pcode"
    name_col = "District" if level == "District" else "admin3Name_en"
    if id_col == name_col:
        columns = ["geometry", id_col, var_name, "Tea_State_Count", "T_TL", "AREA_SQKM"]
    else:
        columns = [
            "geometry",
            id_col,
            name_col,
            var_name,
            "Tea_State_Count",
            "T_TL",
            "AREA_SQKM",
        ]
    folium.Choropleth(
        geo_data=input_df,
        data=input_df,
        columns=[id_col, var_name],
        key_on="feature.properties." + id_col,
        line_weight=0,
        legend_name=COL_NAME_MAP[var_name],
        fill_color=COLOR_MAP[var_name],
    ).add_to(m)

    tooltip = folium.GeoJsonTooltip(
        fields=[
            name_col,
            var_name,
            "Tea_State_Count",
            "T_TL",
            "AREA_SQKM",
        ],
        aliases=[
            "District:" if level == "District" else "Upazila:",
            f"{COL_NAME_MAP[var_name]}:",
            f"{COL_NAME_MAP['Tea_State_Count']}",
            f"{COL_NAME_MAP['T_TL']}",
            f"{COL_NAME_MAP['AREA_SQKM']}",
        ],
        localize=True,
        sticky=False,
        labels=True,
        max_width=800,
    )

    folium.GeoJson(
        input_df[columns].to_geo_dict(),
        style_function=lambda feature: {
            "color": "blue"
            if feature["properties"]["Tea_State_Count"] > 0
            else "black",
            "fillOpacity": 0,
            "weight": 1.3 if feature["properties"]["Tea_State_Count"] > 0 else 0.5,
        },
        highlight_function=lambda feature: {
            "opacity": 1,
            "weight": 2.3 if feature["properties"]["Tea_State_Count"] > 0 else 1,
            "color": "blue"
            if feature["properties"]["Tea_State_Count"] > 0
            else "black",
        },
        tooltip=tooltip,
    ).add_to(m)
    fig = folium.Figure(height="800px").add_child(m)
    return fig._repr_html_()


if __name__ == "__main__":
    for var in DISTRICT_VAR_COLS:
        print(var)
        map_html = get_map_html(var, MAP_DISTRICT_DF, "District")
        file_base = var.replace("+", "_").replace(" ", "_")
        write_zip_file(file_base, map_html)
    print("starting upazila")
    for var in THANA_VAR_COLS:
        print(var)
        map_html = get_map_html(var, MAP_THANA_DF, "Upazila")
        file_base = var.replace("+", "_").replace(" ", "_") + "_thana"
        write_zip_file(file_base, map_html)
