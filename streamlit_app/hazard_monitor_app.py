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

# --- Load data
gdf = dl.load_polygon()
municipalities = gdf['nome'].sort_values().unique().tolist()

# --- Initialize session state
if "selected_city_session" not in st.session_state:
    st.session_state["selected_city_session"] = None

colMap, _, colDesc = st.columns([7, 0.2, 4])

# =====================================================
# LEFT COLUMN - MAP
# =====================================================
with colMap:
    st.markdown("#### Select a city in the map or from the sidebar to visualize its information")

    # --- Create and style base map
    m = map.styledMap()
    m.fit_bounds(dl.state_bounds(gdf))

    # --- Add dark mask outside state
    folium.GeoJson(
        map.masks(gdf),
        style_function=lambda x: {"fillColor": "black", "color": "black", "fillOpacity": 0.7}
    ).add_to(m)

    # --- Add all municipalities polygons
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

    # --- Highlight currently selected city
    if st.session_state["selected_city_session"]:
        city_gdf = gdf[gdf["nome"] == st.session_state["selected_city_session"]]
        folium.GeoJson(
            city_gdf,
            name="Selected City",
            style_function=lambda x: {"fillColor": "#1976D2", "weight": 2, "fillOpacity": 0.6},
            highlight_function=lambda x: {"fillColor": "#1976D2", "color": "#1976D2", "fillOpacity": 0.6},
            tooltip=folium.GeoJsonTooltip(fields=["nome"], aliases=["City:"]),
        ).add_to(m)

    # --- Display map and capture interactions
    st_data = st_folium(m, width='100%')

# =====================================================
# RIGHT COLUMN - CITY INFORMATION
# =====================================================
with colDesc:
    st.markdown("#### Select the City you want to observe")

    # --- City selector synced with session state
    selected_city = st.selectbox(
        "Municipality",
        municipalities,
        key="city_selector",
        index=(municipalities.index(st.session_state["selected_city_session"])
               if st.session_state["selected_city_session"] in municipalities else 0)
    )

    # --- If selectbox changes, update session state
    if selected_city != st.session_state["selected_city_session"]:
        st.session_state["selected_city_session"] = selected_city
        st.rerun()

    # --- Handle map click
    if st_data and st_data.get("last_active_drawing"):
        properties = st_data["last_active_drawing"].get("properties", {})

        if properties and "nome" in properties:
            clicked_city = properties["nome"]

            # Sync map click → selectbox
            if clicked_city != st.session_state["selected_city_session"]:
                st.session_state["selected_city_session"] = clicked_city
                st.rerun()

    # --- Display city info if selected
    if st.session_state["selected_city_session"]:
        dl.display_city_info(
            selected_city=st.session_state["selected_city_session"],
            gdf=gdf
        )
