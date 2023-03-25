import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import MarkerCluster
import pandas as pd

st.set_page_config(page_title="Filter")

st.markdown(
    """
    <div style='background-color: #0066cc; padding: 120px'>
        <h2 style='color: white;text-align: center;'>Research past transactions for a smarter home purchase</h2>
        <h3 style='color: #d3d3d3;text-align: center;'>Select • Filter • Visualize </h3>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style='background-color: white; padding: 10px'>
    </div>
    """,
    unsafe_allow_html=True
)



### READ DATA ###
file_location = "updated_2017_to_now.csv"
data = pd.read_csv(file_location, index_col=0)
data = data.dropna(axis=0)
data = data.drop_duplicates().reset_index().drop("index", axis=1)

### SELECTIONS ###
# town
town_filter = list(data["town"].unique())
option_town = st.selectbox("Select a town", options=sorted(town_filter, key=str.lower))
filtered_data = data[data["town"] == option_town]

# flat type
option_flat = st.multiselect("Select desired flat types", ("2 ROOM", "3 ROOM", "4 ROOM", "5 ROOM", "EXECUTIVE", "MULTI-GENERATION"))
filtered_data = filtered_data[filtered_data["flat_type"].isin(option_flat)]

# story range
story_filter = list(data["storey_range"].unique())
option_story = st.multiselect("Select desired story ranges", options=sorted(story_filter, key=str.lower))
filtered_data = filtered_data[filtered_data["storey_range"].isin(option_story)]

# floor area
min_value_area = int(data["floor_area_sqm"].min())
max_value_area = int(data["floor_area_sqm"].max())
select_range_area = st.slider("Select floor area (square meter)", min_value_area, max_value_area, (min_value_area, max_value_area), step = 5)
filtered_data = filtered_data[(filtered_data["floor_area_sqm"] >= select_range_area[0]) & (filtered_data["floor_area_sqm"] <= select_range_area[1])]

# distance to MRT station
min_value_mrt = float(data["Distance_from_MRT"].min())
max_value_mrt = float(data["Distance_from_MRT"].max())
select_range_mrt = st.slider("Select distance to the closest MRT station (km)", min_value_mrt, max_value_mrt, (min_value_mrt, max_value_mrt), step = 0.01)
filtered_data = filtered_data[(filtered_data["Distance_from_MRT"] >= select_range_mrt[0]) & (filtered_data["Distance_from_MRT"] <= select_range_mrt[1])]

# distance to school
min_value_school = float(data["primary_school_distance"].min())
max_value_school = float(data["primary_school_distance"].max())
select_range_school = st.slider("Select distance to the closest primary school range (km)", min_value_school, max_value_school, (min_value_school, max_value_school), step = 0.01)
filtered_data = filtered_data[(filtered_data["primary_school_distance"] >= select_range_school[0]) & (filtered_data["primary_school_distance"] <= select_range_school[1])]

# distance to mall
min_value_mall= float(data["nearest_shopping_mall_distance"].min())
max_value_mall = float(data["nearest_shopping_mall_distance"].max())
select_range_mall = st.slider("Select distance to closest shopping mall (km)", min_value_mall, max_value_mall, (min_value_mall, max_value_mall), step = 0.01)
filtered_data = filtered_data[(filtered_data["nearest_shopping_mall_distance"] >= select_range_mall[0]) & (filtered_data["nearest_shopping_mall_distance"] <= select_range_mall[1])]

# resale price slider
min_value_price = int(data["resale_price"].min())
max_value_price = int(data["resale_price"].max())
select_range_price = st.slider("Select resale price range ($)", min_value_price, max_value_price, (min_value_price, max_value_price), step=10000)
filtered_data = filtered_data[(filtered_data["resale_price"] >= select_range_price[0]) & (filtered_data["resale_price"] <= select_range_price[1])]

### MAP ###
latitude = 1.353047 # fix later
longitude = 103.832023 # fix later
sg_map = folium.Map(location=[latitude, longitude], zoom_start = 11, tiles = "Open Street Map", prefer_canvas=True)
mCluster = MarkerCluster().add_to(sg_map)

for lat, long, address, town, price, month, story, area in zip(filtered_data["Latitude"], filtered_data["Longitude"], filtered_data["address.1"], filtered_data["town"], filtered_data["resale_price"], filtered_data["month"], filtered_data["storey_range"], filtered_data["floor_area_sqm"]):

    html = f"""
        <b>{address}</b>
        <p>{story} storey
            <br>{area} sqm
            <br>${price}
            <br>{month}
        </p>
    """
    popup = folium.Popup(html, max_width=170)
    folium.Marker([lat, long], popup=popup, icon=folium.Icon(icon='home')).add_to(mCluster)

sw = filtered_data[["Latitude", "Longitude"]].min().values.tolist()
ne = filtered_data[["Latitude", "Longitude"]].max().values.tolist()

sg_map.fit_bounds([sw, ne], padding = (300, 300))

st.write(str(len(filtered_data)) + " flats found!")
st_data = st_folium(sg_map, width=1000)
