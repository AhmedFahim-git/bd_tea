# Seeping Lights ITU data hackathon project 2026

In this project we analyze the current state of Universal and Meaningful Connectivity (UMC) in Bangladesh with a special focus on Tea Estates workers and population. The final deliverable of the analysis is a dashboard that helps visualize the key variables related to achieving UMC in Bangladesh.

## Datasets Used

Both public and private (proprietary) datasets were used in the analysis. The following table gives overview of the datasets used:


| Dataset name | Source (organization/provider) | Link (URL) | Coverage (geographic detail and time) | Key variables (max. 5) | Format (CSV, JSON, XLS, SQL, etc.) | Access method (download, API call, scraping, etc.) |
|---|---|---|---|---|---|---|
| Bangladesh: Population and Housing Census Dataset | Bangladesh Bureau of Statistics (BBS) | https://data.humdata.org/dataset/population-and-housing-census-dataset | Bangladesh, up to District (Admin 02) level, 2022 | %_Mobile Phone_Total_15 year+, %_Internet_Total_15 year+ | XLSX | Download |
| Bangladesh - Subnational Administrative Boundaries | Office for the Coordination of Humanitarian Affairs (OCHA) | https://ckan.rimes.int/dataset/bangladesh-subnational-boundaries | Bangladesh, up to Admin level 04, 2024 | Geometry, AREA_SQKM | GDB, XLSX | Download |
| Bangladesh - Population Density | WorldPop | https://data.humdata.org/dataset/worldpop-population-density-for-bangladesh | Bangladesh, resolution of 30 arc-seconds, 2020 | lat, lon, population_density | CSV | Download |
| Operator X Cell tower location | Operator X Employee | Proprietary | Bangladesh | lat, lon | XLSX | Download |
| Bangladesh - Subnational Population Statistics | UNFPA | https://data.humdata.org/dataset/cod-ps-bgd | Bangladesh upto administrative level 0-3, 2022 | T_TL | XLSX | Download |
| Registered 170 Tea State List | Bangladesh Tea Board | https://teaboard.gov.bd/pages/notices/6922ed22dbfab28ce0c016c | Bangladesh, 2025 | District, Thana | PDF | Download |
| Bangladesh Poverty Map | World Bank Group | https://www.worldbank.org/en/data/interactive/2016/11/10/bangladesh-poverty-maps | Bangladesh, upto administrative level 2-3, 2010 | Poverty headcount ratio (%) 4G | XLSX, GDB | Download |
| 4G District-wise download speed | BTRC | Proprietary | Bangladesh, up to District (Admin 02) level, 2026 | 4G Avg. UE throughput DL (MB) | XLSX | Download |
| Tea Estate Location | Bangladesh Tea Board | Proprietary | Sylhet, 2026 | lat, lon | PDF | Download |
| Tea Estate worker and population statistics | Tea Board Sylhet | Proprietary | Sylhet, 2026 | unreg_workes, tea_estate_pop | PDF | Download |



## Methodology:

The goal of the analysis is a dashboard that visualizes the following:

1. Spatial distribution of key demographic variables and network connectivity metrics.
2. Correlation among demographic variables and connectivity metrics.
3. Deeper look into current connectivity of tea estates.

For visualization of spatial information we used administrative boundaries obtained from [Bangladesh - Subnational Administrative Boundaries](https://ckan.rimes.int/dataset/bangladesh-subnational-boundaries) which provided boundaries upto Admin 04 (Union) level. The population for each administrative region was obtained from [Bangladesh - Subnational Population Statistics](https://data.humdata.org/dataset/cod-ps-bgd) dataset. Demographic information are obtained from [Bangladesh Population & Housing Census 2022](https://data.humdata.org/dataset/populationa-and-housing-census-dataset). The report only contained data upto Admin 02 (District) level and we used the variables: % of population using internet, % population having mobile phone, literacy rate (7+), employment rate, % population having financial account, % population having mobile bank account. For all these variables we have overall numbers and broken down by gender. We also obtained the % of population with electricity from this dataset. This was joined by [2010 Poverty Map](https://www.worldbank.org/en/data/interactive/2016/11/10/bangladesh-poverty-maps) as proxy for income distribution at District and Upazila level.

For network connectivity metrics we used  proprietary cell tower locations of an anonymous mobile operator. We used this to calculate the number of towers and cell tower density in each administrative region. We combined the cell tower location data with [gridded population density](https://data.humdata.org/dataset/worldpop-population-density-for-bangladesh) data to find the distance to nearest tower from each grid point and calculated summary statistics of this distance within each administrative region weighted by the population density. The datasets were converted to projected coordinate system EPSG:3106 (Gulshan 303 / TM 90 NE) for distance calculation and then converted back to geographic coordinate system EPSG:4326 (WGS84, World Geodetic System 1984) for visualization. We also obtained another proprietary district-level dataset on average 4G Download Speed (Mbps) from BTRC.

We obtained the Admin 02 (district) and Admin 03 (thana/upazila) of each [tea estate in Bangladesh](https://teaboard.gov.bd/pages/notices/6922ed22dbfbab28ce0c016c) and extracted the data in csv format using ChatGPT. The data was cleaned to make the district and upazila names to match with the official datasets. This data was then used to find number of Tea Estates in each Admin 02 (district) and Admin 03 (upazila). For deeper look into tea estates we obtained cooridinates of tea estates in Sylhet as well as the number of workers and population at each location from proprietary sources.

We used choropleth maps for visualizing the spatial distribution of variables. The demographic information obtained from census data was shown at only Admin 02 (District) level. The network connectivity metrics were visualized at Admin 02 (District) and Admin 03 (Upazila) level.

We also used choropleth maps in the deep dive into Sylhet tea estates, along with colored markers locating each tea estate. A table is also included listing each tea estate in Sylhet, highlighting the connectivity metrics that are lower than required.

We performed statistical test to check the slope coefficient among the variables in linear regression. We also displayed a scatter plot with a regression line to visualize the relation. The statistical test and visualization was done at Admin 02 (District) level data only, using both demographic variables and connectivity metrics. We also included a correlation heatmap to quickly identify important factors affecting connectivity.

## Project Structure

The structure of the project is given below:

```
.
├── data
│   ├── final
│   │   ├── district_data.csv
│   │   └── tea_data.csv
│   ├── intermediate
│   │   ├── final_thana_viz.gpkg
│   │   ├── final_viz.gpkg
│   │   └── ...
│   └── raw
│       ├── BGD_AdminBoundaries_candidate.gdb
│       ├── bgd_admpop_2022.xlsx
│       └── ...
├── outputs
│   ├── 4G_Avg._UE_throughput_DL_(MB).lzma
│   ├── Cell_tower_density.lzma
│   └── ...
├── pyproject.toml
├── constants.py
├── make_map_files.py
├── make_viz_file.py
├── dashboard.py
├── tea_lat_lon.py
├── requirements.txt
└── README.md
```

The datasets downloaded are placed in `data/raw/`. Python scripts are used to transform the raw data into intermediate datasets that are used in later stages, and final datasets that are used in the final streamlit dashboard. The intermediate datasets are stored in `/data/intermediate/`, and the final datasets are stored in `data/final/`. The intermediate datasets are used to generate html maps that are zipped and stored in `outputs/` directory.

The `pyproject.toml` file contains the dev depencies, while the `requirements.txt` file has requirements for streamlit deployment.

## Usage

1. Preprocess tea estate datasets

The python script `tea_lat_lon.py` is used to read `data/raw/tea.pdf`, which has coordinates of tea estates in Sylhet, and the `data/raw/tea_workers.csv`, which has the population and number of workers in the Sylhet tea estates. The processed dataset is stored in `data/intermediate/tea_lat_lon.csv`.

```
python tea_lat_lon.py
```

2. Make intermediate and final datasets for visualization

The python script `make_viz_file.py` is used to read in the raw datasets and `data/intermediate/tea_lat_lon.csv` to make other intermediate datasets and some final datasets for visualization.

Intermediate datasets are:
- `data/intermediate/final_viz.gpkg`
- `data/intermediate/final_thana_viz.gpkg`
- `data/intermediate/tea_data.gpkg`

Final datasets are:
- `data/final/district_data.csv`
- `data/final/tea_data.csv`

```
python make_viz_file.py
```

3. Make map files

The choropleth maps are data intensive and take some time to generate, so they are not suitable to generate directly in the dashboard. Hence it is better to generate the choropleth maps and store them. This makes the process of displaying maps in dashboard significantly faster. The script `make_map_files.py` reads the intermediate datasets generated by `make_viz_file.py` and generates map files for each relevant variable. The maps are zipped and stored in `outputs/`.

```
python make_map_files.py
```

4. Display dashboard

The dashboard reads in maps from `outputs/` directory and datasets from `data/final/` and visualizes them to user.

```
streamlit run dashboard.py --server.port=8501 --server.address=0.0.0.0
```

This has been deployed to Streamlit Cloud and the dashboard can be found on [https://egmoeukl2amlsmpk6ydyqj.streamlit.app/](https://egmoeukl2amlsmpk6ydyqj.streamlit.app/)
