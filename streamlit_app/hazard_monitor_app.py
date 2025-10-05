import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from shapely.geometry import Point
import map_manager.map as map
import data_manager.data_loader as dl

st.set_page_config(layout="wide")
# --- Title and description
st.markdown("<h1 style='color: #66d575;'>Rio de Janeiro City Hazard Monitoring</h1>", unsafe_allow_html=True)

"" 
""

# --- Load data
gdf = dl.load_polygon()
municipalities = gdf['nome'].sort_values().unique().tolist()
selected_city = None


colMap, _, colDesc = st.columns([7, 0.2, 4]) 
with colMap:
    # --- Map
    st.markdown("#### Select a city in the map or from the sidebar to visualize its information")
    #st.markdown(gdf.keys())
    # limits map to the state bounds
    m = map.styledMap()
    m.fit_bounds(dl.state_bounds(gdf))

    # Add the mask polygon to Folium (dark overlay outside state)
    folium.GeoJson(
        map.masks(gdf),
        style_function=lambda x: {"fillColor": "black", "color": "black", "fillOpacity": 0.7}
    ).add_to(m)

    # --- Add polygons for all municipalities
    popup = folium.GeoJsonPopup(fields=["nome"], aliases=["City:"])
    folium.GeoJson(
        gdf,
        name="Municipalities",
        style_function=lambda x: {"fillColor": "#E0E0E0", "color": "gray", "weight": 1, "fillOpacity": 0.4},
        highlight_function=lambda x: {"fillColor": "#1976D2", "color": "#1976D2", "fillOpacity": 0.6},
        tooltip=folium.GeoJsonTooltip(fields=["nome"], aliases=["City:"]),
        zoom_on_click=True,
        popup=popup,
        popup_keep_highlighted=True,
    ).add_to(m)

    # --- Filter the GeoDataFrame for the selected city
    if selected_city:
        city_gdf = gdf[gdf["nome"] == selected_city]
        # --- Highlight selected city
        folium.GeoJson(
            city_gdf,
            name="Selected City",
            style_function=lambda x: {"fillColor": "#1976D2", "weight": 2, "fillOpacity": 0.6},
            highlight_function=lambda x: {"fillColor": "#1976D2", "color": "#1976D2", "fillOpacity": 0.6},
            tooltip=folium.GeoJsonTooltip(fields=["nome"], aliases=["City:"]),
            zoom_on_click=True,
            popup=popup,
            popup_keep_highlighted=True,
        ).add_to(m)

    # --- Show map
    st_data = st_folium(m, width='100%')


with colDesc:
    # --- City selector
    st.markdown("#### Select the City you want to observe")
    selected_city = st.selectbox("Municipality", (municipalities), key='selected_city_session', index=None)
    

    if selected_city:
        dl.display_city_info(selected_city=selected_city, gdf=gdf)

    # --- Optional: detect click on map
    if st_data and st_data.get("last_active_drawing"):
        st.markdown("🖱️ **Clicked location on map:**")
        coords = st_data["last_clicked"]
        properties = st_data['last_active_drawing']['properties']

        if properties:
            selected_city = properties['nome']
            st.markdown(f"### 🏙️ Selected City: {selected_city}")
        
        if coords:
            st.markdown(f"Lat: {coords['lat']:.4f}, Lon: {coords['lng']:.4f}")


    
