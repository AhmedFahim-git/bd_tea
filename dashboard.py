import os
from zipfile import ZIP_LZMA, ZipFile

import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
from scipy.stats import linregress

DISTRICT_ONLY_VARS = [
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
]
DISTRICT_THANA_VARS = [
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
VAR_COLS = DISTRICT_ONLY_VARS + DISTRICT_THANA_VARS
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
DATA_COLS = [COL_NAME_MAP[x] for x in VAR_COLS]


def read_zip_file(file_base: str) -> str:
    with ZipFile(
        os.path.join("outputs", file_base + ".lzma"), "r", compression=ZIP_LZMA
    ) as myzip:
        return myzip.read(file_base + ".html").decode()


@st.cache_data
def get_map_html(var_name: str, admin_level: str) -> str:
    if admin_level == "District":
        file_base = var_name.replace("+", "_").replace(" ", "_")
    else:
        file_base = var_name.replace("+", "_").replace(" ", "_") + "_thana"
    html_file = read_zip_file(file_base)
    return html_file


@st.cache_data
def read_data_csv():
    df = pd.read_csv("data/district_data.csv")
    df["Tea_State_Presence"] = df["Tea_State_Count"].apply(
        lambda x: "Tea State Present" if x > 0 else "Tea State Absent"
    )
    df = df.rename(columns=COL_NAME_MAP)
    return df


def set_admin(var):
    if var in DISTRICT_ONLY_VARS and "admin" in st.session_state:
        print("set")
        st.session_state.admin = "District"


st.header("Choropleth map showing spatial distribution")

col1, col2 = st.columns([0.6, 0.4])

with col1:
    selected_var = st.selectbox(
        label="**Please select Variable to Visualize in Map**",
        options=VAR_COLS,
        format_func=lambda x: COL_NAME_MAP[x],
    )

set_admin(selected_var)

with col2:
    admin_level = st.selectbox(
        label="**Select Admin Level for visualization**",
        options=["District", "Upazila"],
        disabled=selected_var in DISTRICT_ONLY_VARS,
        key="admin",
    )

map_html = get_map_html(selected_var, admin_level)

components.html(map_html, height=800)

st.divider()

st.header("Correlation among variables")

col1, col2 = st.columns(2)

with col1:
    ind_var = st.selectbox(
        label="**Independent Variable**",
        options=DATA_COLS,
    )

if "dep_var" in st.session_state and ind_var == st.session_state.dep_var:
    st.session_state.dep_var = DATA_COLS[
        (DATA_COLS.index(ind_var) + 1) % len(DATA_COLS)
    ]
with col2:
    dep_var = st.selectbox(
        label="**Dependent Variable**",
        options=DATA_COLS,
        index=len(DISTRICT_ONLY_VARS),
        key="dep_var",
    )

district_df = read_data_csv()

reg = linregress(x=district_df[ind_var], y=district_df[dep_var])

st.html(
    f"<h3 style='margin-bottom: 0;'>Pearson correlation coeffecient: {reg.rvalue:.3g}  P-value: {reg.pvalue:.3g}</h3>"
)

st.html(
    f"<h3 style='margin-bottom: 0; margin-top: 0;'>Statistical Significance: {'Significant' if reg.pvalue <= 0.05 else 'Not Significant'}</h3>"
)

fig = px.scatter(
    district_df,
    x=ind_var,
    y=dep_var,
    color="Tea_State_Presence",
    trendline="ols",
    trendline_scope="overall",
    hover_data=["District", "Number of Tea States", "Total Population"],
)
fig.update_layout(
    hoverlabel=dict(font=dict(size=14)),
    legend=dict(font=dict(size=14)),
    legend_title=dict(font=dict(size=14)),
)
st.plotly_chart(fig)
