import os
from concurrent.futures import ProcessPoolExecutor
from zipfile import ZIP_LZMA, ZipFile

import folium
import geopandas as gpd
import pandas as pd

from constants import (
    COL_NAME_MAP,
    COLOR_MAP,
    DISTRICT_VAR_COLS,
    TEA_VAR_COLS,
    THANA_VAR_COLS,
)

MAP_DISTRICT_DF = gpd.read_file("data/intermediate/final_viz.gpkg")
MAP_THANA_DF = gpd.read_file("data/intermediate/final_thana_viz.gpkg")
TEA_DF = gpd.read_file("data/intermediate/tea_data.gpkg")


FOLIUM_COLOR_MAP = {
    "good": "green",
    "ok": "beige",
    "pretty_bad": "orange",
    "bad": "red",
}


def write_zip_file(file_base: str, text: str) -> None:
    with ZipFile(
        os.path.join("outputs", file_base + ".lzma"), "w", compression=ZIP_LZMA
    ) as myzip:
        myzip.writestr(file_base + ".html", text)


def make_map(
    in_map: folium.Map,
    input_df: pd.DataFrame,
    id_col: str,
    name_col: str,
    var_name: str,
    level: str,
) -> None:
    columns = [
        "geometry",
        id_col,
        name_col,
        var_name,
        "Tea_State_Count",
        "T_TL",
        "AREA_SQKM",
    ]
    bins = pd.qcut(input_df[var_name], q=6, retbins=True)[1]
    folium.Choropleth(
        geo_data=input_df,
        data=input_df,
        columns=[id_col, var_name],
        key_on="feature.properties." + id_col,
        line_weight=0,
        legend_name=COL_NAME_MAP[var_name],
        fill_color=COLOR_MAP[var_name],
        bins=bins,
    ).add_to(in_map)

    tooltip = folium.GeoJsonTooltip(
        fields=[
            name_col,
            var_name,
            "Tea_State_Count",
            "T_TL",
            "AREA_SQKM",
        ],
        aliases=[
            f"{level}:",
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
    ).add_to(in_map)


def get_map_html(var_name: str, input_df: gpd.GeoDataFrame, level: str) -> str:
    m = folium.Map(location=[23.763889, 90.388889], zoom_start=7, font_size="1.2rem")
    id_col = "admin2Pcode" if level == "District" else "admin3Pcode"
    name_col = "District" if level == "District" else "admin3Name_en"
    make_map(
        m,
        input_df,
        id_col,
        name_col,
        var_name,
        "District" if level == "District" else "Upazila",
    )
    fig = folium.Figure(height="800px").add_child(m)
    return fig._repr_html_()


def get_tea_map_html(
    var_name: str, input_df: gpd.GeoDataFrame, tea_df: gpd.GeoDataFrame
):
    m = folium.Map(location=[24.5, 91.666667], zoom_start=9, font_size="1.2rem")
    id_col = "admin3Pcode"
    name_col = "admin3Name_en"
    tea_var_name = var_name
    if var_name == "nearest_distance":
        var_name = "distance"
    var_name = "mean_" + var_name
    make_map(m, input_df, id_col, name_col, var_name, "Upazila")
    for _, row in tea_df.iterrows():
        folium.Marker(
            location=(row["lat"], row["lon"]),
            icon=folium.Icon(
                color=FOLIUM_COLOR_MAP[row[tea_var_name + "_quality"]], icon="leaf"
            ),
            tooltip=f"""<b>Garden Name:</b> {row["tea_garden_bn"]} ({row["tea_garden_en"]})<br>
            <b>{COL_NAME_MAP[tea_var_name]}:</b> {row[tea_var_name]:.0f}{" m" if tea_var_name == "nearest_distance" else ""}<br>
            <b>{COL_NAME_MAP["tot_workers"]}:</b> {row["tot_workers"]}<br>
            <b>{COL_NAME_MAP["perc_unreg_workers"]}:</b> {row["perc_unreg_workers"]:.3g} %<br>
            <b>{COL_NAME_MAP["tea_estate_pop"]}:</b> {row["tea_estate_pop"]}""",
        ).add_to(m)
    fig = folium.Figure(height="700px").add_child(m)
    return fig._repr_html_()


def make_save_map(
    in_tuple: tuple[str, gpd.GeoDataFrame, str, gpd.GeoDataFrame | None],
) -> str:
    var, input_df, level, extra_df = in_tuple
    map_html = ""
    file_base = ""
    print("Started", level, var)
    if level == "District":
        map_html = get_map_html(var, input_df, level)
        file_base = var.replace("+", "_").replace(" ", "_")
    elif level == "Upazila":
        map_html = get_map_html(var, input_df, level)
        file_base = var.replace("+", "_").replace(" ", "_") + "_thana"
    else:
        map_html = get_tea_map_html(var, input_df, extra_df)
        file_base = var.replace("+", "_").replace(" ", "_") + "_tea"
    write_zip_file(file_base, map_html)
    return f"Completed {level} {var}"


if __name__ == "__main__":
    dist_list = []
    for var in DISTRICT_VAR_COLS:
        dist_list.append((var, MAP_DISTRICT_DF, "District", None))

    thana_list = []
    for var in THANA_VAR_COLS:
        thana_list.append((var, MAP_THANA_DF, "Upazila", None))

    sylhet_thana_df = MAP_THANA_DF[MAP_THANA_DF["admin1Name_en"] == "Sylhet"]
    tea_list = []
    for var in TEA_VAR_COLS:
        tea_list.append((var, sylhet_thana_df, "Tea", TEA_DF))

    # in_list = dist_list + thana_list + tea_list
    in_list = tea_list
    with ProcessPoolExecutor(max_workers=8) as executor:
        for my_tuple, res in zip(in_list, executor.map(make_save_map, in_list)):
            try:
                assert res
                print(res)
            except:
                print(f"Failed {my_tuple[2]}, {my_tuple[0]}")
