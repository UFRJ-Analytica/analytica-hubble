import streamlit as st
import geopandas as gpd

# --- Load geodata for Rio de Janeiro municipalities
# Using EarthWorks Stanford GeoJSON data for RJ municipalities
#"https://earthworks.stanford.edu/catalog/stanford-hc979qh6228"
data_path='flui_app/data_manager/geojson/'

@st.cache_data
def load_brazil_polygon():   
    try:
        gdf_brazil = gpd.read_file(data_path+'geojson_brazil_admin_states.json')
        #gdf = gpd.read_file(data_path+'stanford-hc979qh6228-geojson.json')
    except Exception as e:
        st.error("Failed to load state data: " + str(e))
        st.stop()
    return gdf_brazil

def load_polygon_state(state_code):
    try:
        gdf_state = gpd.read_file(f"{data_path}geojs-{state_code}-mun.json")
    except Exception as e:
        st.error("Failed to load state data: " + str(e))
        st.stop()
    return gdf_state

def state_bounds(gdf):
    bounds = gdf.total_bounds

    # Convert to [[southwest_lat, southwest_lon], [northeast_lat, northeast_lon]]
    sw = [bounds[1], bounds[0]]  # (lat, lon)
    ne = [bounds[3], bounds[2]]  # (lat, lon)

    return [sw, ne]

def display_city_info(selected_city, gdf):
    # --- City Information Section
    st.subheader(f"{selected_city} City Information")
    
    """

    
    """
    # Add more info (example placeholders)
    city_info = {
        "Flood Risk Index": "9.5",
        "Flood Frequency": "1/year",
        "Classification": "🔴 high-risk area",
    }

    count=0
    cols_size=3
    col1, col2, col3 = st.columns([1,1,2])
    cols=[col1, col2, col3]

    for key, val in city_info.items():
        col = cols[count%cols_size]
        if(count==cols_size):
            st.metric(f"{key}",  f"{val}", width="content")
        else:
            col.metric(f"{key}",  f"{val}", width="content")
        count+=1