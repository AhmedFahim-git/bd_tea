import os

import folium
import geopandas as gpd

MAP_DF = gpd.read_file("data/final_viz.gpkg")

VAR_COLS = [
    "Inernet_Total_15 year+",
    "Inernet_Male_15 year+",
    "Inernet_Female_15 year+",
    "Mobile Phone_Total_15 year+",
    "Mobile Phone_Male_15 year+",
    "Mobile Phone_Female_15 year+",
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
    "AREA_SQKM": "Area (in sqkm)",
    "Inernet_Total_15 year+": "% of Total 15+ population using Internet",
    "Inernet_Male_15 year+": "% of Male 15+ population using Internet",
    "Inernet_Female_15 year+": "% of Female 15+ population using Internet",
    "Mobile Phone_Total_15 year+": "% of Total 15+ population having Mobile Phone",
    "Mobile Phone_Male_15 year+": "% of Male 15+ population having Mobile Phone",
    "Mobile Phone_Female_15 year+": "% of Female 15+ population having Mobile Phone",
    "Num_op_x_towers": "Number of Operator X Towers in District",
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


def get_map_html(var_name: str):
    m = folium.Map(location=[23.763889, 90.388889], zoom_start=7, font_size="1.2rem")
    folium.Choropleth(
        geo_data=MAP_DF,
        data=MAP_DF,
        columns=["District", var_name],
        key_on="feature.properties.District",
        line_weight=0,
        legend_name=COL_NAME_MAP[var_name],
    ).add_to(m)

    tooltip = folium.GeoJsonTooltip(
        fields=["District", var_name, "Tea_State_Count", "T_TL", "AREA_SQKM"],
        aliases=[
            "District:",
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
        MAP_DF.to_geo_dict(),
        style_function=lambda feature: {
            "color": "green"
            if feature["properties"]["Tea_State_Count"] > 0
            else "black",
            "fillOpacity": 0,
            "weight": 1 if feature["properties"]["Tea_State_Count"] > 0 else 0.5,
        },
        highlight_function=lambda feature: {
            "opacity": 1,
            "weight": 2 if feature["properties"]["Tea_State_Count"] > 0 else 1,
            "color": "green"
            if feature["properties"]["Tea_State_Count"] > 0
            else "black",
        },
        tooltip=tooltip,
    ).add_to(m)
    fig = folium.Figure(height="800px").add_child(m)
    return fig._repr_html_()


if __name__ == "__main__":
    for var in VAR_COLS:
        print(var)
        map_html = get_map_html(var)
        with open(
            os.path.join("outputs", var.replace("+", "_").replace(" ", "_") + ".html"),
            "w",
        ) as f:
            f.write(map_html)
