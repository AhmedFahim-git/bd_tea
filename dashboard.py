import os

import streamlit as st
import streamlit.components.v1 as components

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


selected_var = st.selectbox(
    label="**Please select Variable to Visualize**",
    options=VAR_COLS,
    format_func=lambda x: COL_NAME_MAP.get(x, x),
)

map_html = get_map_html(selected_var)

components.html(map_html, height=800)
