import os
from zipfile import ZIP_LZMA, ZipFile

import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
from scipy.stats import linregress

from constants import (
    COL_NAME_MAP,
    DISTRICT_ONLY_VAR_COLS,
    DISTRICT_VAR_COLS,
    HEATMAP_DEFAULT_COLS_MAPPED,
    TEA_TABLE_COLS,
    TEA_VAR_COLS,
)

st.set_page_config(layout="wide")

DATA_COLS = [COL_NAME_MAP[x] for x in DISTRICT_VAR_COLS]


# Adapted from https://discuss.streamlit.io/t/table-of-contents-widget/3470/8
class Toc:
    def __init__(self):
        self._items = []
        self._placeholder = None

    def title(self, text):
        self._markdown(text, "h1")

    def header(self, text):
        self._markdown(text, "h2", " " * 2)

    def subheader(self, text):
        self._markdown(text, "h3", " " * 4)

    def placeholder(self, sidebar=False):
        # self._placeholder = st.sidebar.empty() if sidebar else st.empty()
        self._placeholder_side = st.sidebar.empty()
        self._placeholder = st.empty()

    def generate(self):
        # if self._placeholder:
        #     self._placeholder.markdown("\n".join(self._items), unsafe_allow_html=True)
        self._placeholder.markdown("\n".join(self._items), unsafe_allow_html=True)
        self._placeholder_side.markdown(
            "# Table of Contents\n" + "\n".join(self._items), unsafe_allow_html=True
        )

    def _markdown(self, text, level, space=""):
        # key = "".join(filter(str.isalnum, text)).lower()
        key = text.replace(" ", "-").lower()

        st.markdown(f"<{level} id='{key}'>{text}</{level}>", unsafe_allow_html=True)
        self._items.append(f"{space}* <a href='#{key}'>{text}</a>")


def read_zip_file(file_base: str) -> str:
    with ZipFile(
        os.path.join("outputs", file_base + ".lzma"), "r", compression=ZIP_LZMA
    ) as myzip:
        return myzip.read(file_base + ".html").decode()


@st.cache_data
def get_map_html(var_name: str, admin_level: str) -> str:
    file_base = ""
    if admin_level == "District":
        file_base = var_name.replace("+", "_").replace(" ", "_")
    elif admin_level == "Upazila":
        file_base = var_name.replace("+", "_").replace(" ", "_") + "_thana"
    elif admin_level == "Tea":
        file_base = var_name.replace("+", "_").replace(" ", "_") + "_tea"
    html_file = read_zip_file(file_base)
    return html_file


@st.cache_data
def read_data_csv() -> pd.DataFrame:
    df = pd.read_csv("data/final/district_data.csv")
    df["Tea_State_Presence"] = df["Tea_State_Count"].apply(
        lambda x: "Tea State Present" if x > 0 else "Tea State Absent"
    )
    df = df.rename(columns=COL_NAME_MAP)
    return df


@st.cache_data
def load_tea_data() -> pd.DataFrame:
    return pd.read_csv("data/final/tea_data.csv")


def set_admin(var: str) -> None:
    if var in DISTRICT_ONLY_VAR_COLS and "admin" in st.session_state:
        print("set")
        st.session_state.admin = "District"


def hightlight_row(row: pd.Series) -> list[str]:
    styles = []
    all_tea_cols = TEA_VAR_COLS
    for col in row.index:
        if col not in all_tea_cols:
            styles.append("")
            continue
        quality_col = f"{col}_quality"
        if row[quality_col] == "bad":
            styles.append("color: red")
        else:
            styles.append("")
    return styles


st.title("Seeping Lights ITU Data Hackathon")

toc = Toc()

st.subheader("Table of Contents")
toc.placeholder()

toc.header("Sylhet Tea Gardens Deep Dive")

toc.subheader("Sylhet Choropleth Map with Tea Estate Markers")

selected_tea_var = st.selectbox(
    label="**Please select Variable to Visualize in Map**",
    options=TEA_VAR_COLS,
    format_func=lambda x: COL_NAME_MAP[x],
)

tea_map_html = get_map_html(selected_tea_var, "Tea")

components.html(tea_map_html, height=700)

st.space()
toc.subheader("Sylhet Tea Estate Data Table")
tea_table = load_tea_data()


st.dataframe(
    tea_table.style.apply(hightlight_row, axis=1),
    width="content",
    hide_index=True,
    column_order=TEA_TABLE_COLS,
    column_config={i: COL_NAME_MAP[i] for i in TEA_TABLE_COLS}
    | {
        "nearest_distance": st.column_config.NumberColumn(
            COL_NAME_MAP["nearest_distance"], format="%d"
        ),
        "perc_unreg_workers": st.column_config.NumberColumn(
            COL_NAME_MAP["perc_unreg_workers"], format="percent"
        ),
    },
)

st.divider()

toc.header("Choropleth Map of UMC Metrics Bangladesh")

col1, col2 = st.columns([0.6, 0.4])

with col1:
    selected_var = st.selectbox(
        label="**Please select Variable to Visualize in Map**",
        options=DISTRICT_VAR_COLS,
        format_func=lambda x: COL_NAME_MAP[x],
    )

set_admin(selected_var)

with col2:
    admin_level = st.selectbox(
        label="**Select Admin Level for visualization**",
        options=["District", "Upazila"],
        disabled=selected_var in DISTRICT_ONLY_VAR_COLS,
        key="admin",
    )

map_html = get_map_html(selected_var, admin_level)

components.html(map_html, height=800)

st.divider()

toc.header("Correlation Among Variables")

toc.subheader("Scatter Plot")

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
        index=len(DISTRICT_ONLY_VAR_COLS),
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

toc.subheader("Correlation Heatmap")

selected_cols = st.multiselect(
    label="**Select Variables for Correlation Heatmap**",
    options=DATA_COLS,
    default=HEATMAP_DEFAULT_COLS_MAPPED,
)


cor_fig = px.imshow(
    district_df.loc[:, selected_cols].corr(),
    text_auto=".3g",
    height=1000,
    width=1000,
    zmax=1,
    zmin=-1,
    color_continuous_scale="viridis",
    labels={"x": "var 1", "y": "var 2", "color": "correlation"},
)

cor_fig.update_layout(
    hoverlabel=dict(font=dict(size=14)),
    legend=dict(font=dict(size=14)),
    legend_title=dict(font=dict(size=14)),
)

st.plotly_chart(cor_fig, width="stretch", height="stretch")

toc.generate()
