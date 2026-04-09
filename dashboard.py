import os

import streamlit as st
import streamlit.components.v1 as components

#     return gpd.read_file("data/final_viz.gpkg")
#
#
# MAP_DF = load_data()

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


@st.cache_data
def get_map_html(var_name: str):
    with open(
        os.path.join("outputs", var_name.replace("+", "_").replace(" ", "_") + ".html"),
        "r",
    ) as f:
        html_file = f.read()
    return html_file
    # m = folium.Map(location=[23.763889, 90.388889], zoom_start=7, font_size="1.2rem")
    # folium.Choropleth(
    #     geo_data=MAP_DF,
    #     data=MAP_DF,
    #     columns=["District", var_name],
    #     key_on="feature.properties.District",
    #     line_weight=0,
    #     legend_name=COL_NAME_MAP[var_name],
    # ).add_to(m)
    #
    # tooltip = folium.GeoJsonTooltip(
    #     fields=["District", var_name, "Tea_State_Count", "T_TL", "AREA_SQKM"],
    #     aliases=[
    #         "District:",
    #         f"{COL_NAME_MAP[var_name]}:",
    #         f"{COL_NAME_MAP['Tea_State_Count']}",
    #         f"{COL_NAME_MAP['T_TL']}",
    #         f"{COL_NAME_MAP['AREA_SQKM']}",
    #     ],
    #     localize=True,
    #     sticky=False,
    #     labels=True,
    #     # style="font-size: 14px;",
    #     # style="""
    #     #     background-color: #F0EFEF;
    #     #     border: 2px solid black;
    #     #     border-radius: 3px;
    #     #     box-shadow: 3px;
    #     # """,
    #     max_width=800,
    # )
    #
    # folium.GeoJson(
    #     MAP_DF.to_geo_dict(),
    #     style_function=lambda feature: {
    #         "color": "green"
    #         if feature["properties"]["Tea_State_Count"] > 0
    #         else "black",
    #         # 'stroke':False,
    #         # 'fill': False,
    #         "fillOpacity": 0,
    #         # "opacity": 0,
    #         "weight": 1 if feature["properties"]["Tea_State_Count"] > 0 else 0.5,
    #     },
    #     highlight_function=lambda feature: {
    #         "opacity": 1,
    #         "weight": 2 if feature["properties"]["Tea_State_Count"] > 0 else 1,
    #         "color": "green"
    #         if feature["properties"]["Tea_State_Count"] > 0
    #         else "black",
    #     },
    #     # style_function=lambda x: {
    #     #     "fillColor": colormap(x["properties"]["change"])
    #     #     if x["properties"]["change"] is not None
    #     #     else "transparent",
    #     #     "color": "black",
    #     #     "fillOpacity": 0.4,
    #     # },
    #     tooltip=tooltip,
    #     # popup=popup,
    # ).add_to(m)
    # fig = folium.Figure(height="800px").add_child(m)
    # return fig._repr_html_()
    # return m.get_root()._repr_html_()


selected_var = st.selectbox(
    label="**Please select Variable to Visualize**",
    options=VAR_COLS,
    format_func=lambda x: COL_NAME_MAP.get(x, x),
)
print("hello world")

# placeholder = st.empty()

# placeholder.empty()
# map = get_map(selected_var)
map_html = get_map_html(selected_var)
# st_folium(
#     map,
#     # zoom=7,
#     # center=[23.763889, 90.388889],
#     # width=900,
#     # height=600,
#     use_container_width=True,
#     returned_objects=[],
# )

# fig = folium.Figure().add_child(map)
# comp = st.components.v2.component(name="sup", html=map.get_root()._repr_html_())
# st.html(map_html, unsafe_allow_javascript=True)
# print(map_html[:500])
# fig = folium.Figure(height="800px").add_child(map_html)


# with open("some_file.txt", "w") as f:
#     f.write(map_html)
# print(map_html[190:201])
# print(map_html[190:250])
# map_html = map_html[:5] + ' height="1400" ' + map_html[5:]
# map_html_sss = map_html.get_root()._repr_html_()
# map_html_sss = map_html_sss[:201] + ' width="900" height="900" ' + map_html_sss[201:]
# map_html_sss = map_html_sss[:5] + ' height="1400" ' + map_html_sss[5:]
components.html(map_html, height=800)
# components.iframe(map_html, height=800)
# comp = st.components.v2.component(name="sup", html=map_html_sss, isolate_styles=True)
#
# comp(height=900)
# st.html(fig.render(), unsafe_allow_javascript=True)


# map.render()
# st.html(map.get_root()._repr_html_(), unsafe_allow_javascript=True)
# st.markdown(map.get_root()._repr_html_(), unsafe_allow_html=True)
# with placeholder.container():
# st_folium(
#     map_html,
#     returned_objects=[],
#     use_container_width=True,
# )
# folium_static(map_html)
# with st.empty():
#     map = get_map(selected_var)
#     st_folium(map)
