import streamlit as st
import geopandas as gpd

# --- Load geodata for Rio de Janeiro municipalities
# Using EarthWorks Stanford GeoJSON data for RJ municipalities
#"https://earthworks.stanford.edu/catalog/stanford-hc979qh6228"
@st.cache_data
def load_polygon():
    try:
        gdf = gpd.read_file('data_manager/stanford-hc979qh6228-geojson.json')
    except Exception as e:
        st.error("Failed to load state data: " + str(e))
        st.stop()
    return gdf

def state_bounds(gdf):
    bounds = gdf.total_bounds

    # Convert to [[southwest_lat, southwest_lon], [northeast_lat, northeast_lon]]
    sw = [bounds[1], bounds[0]]  # (lat, lon)
    ne = [bounds[3], bounds[2]]  # (lat, lon)

    return [sw, ne]

def display_city_info(selected_city, gdf):
    # --- City Information Section
    st.header(f"{selected_city} City Information")

    col1, col2 = st.columns(2)

    # Add more info (example placeholders)
    city_info = {
        "Hazard Risk Index": "9.5",
        "Hazard Frequency": "1/year",
        "Classification": "🔴 high-risk area",
    }

    count=0
    cols=[col1, col2]

    for key, val in city_info.items():
        col = cols[count%2]
        if(count==2):
            st.metric(f"{key}",  f"{val}")
        else:
            col.metric(f"{key}",  f"{val}")
        count+=1

    st.markdown(f"{gdf[gdf["nome"] == selected_city]['latitudese']}")