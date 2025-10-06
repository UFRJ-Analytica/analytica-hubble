import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from PIL import Image
import altair as alt
import flui_app.map_manager.map as map
import flui_app.data_manager.data_loader as dl
import pandas as pd

st.set_page_config(layout="wide")
 # --- Title and description
rightIcon, leftIcon = st.columns([1,4], vertical_alignment="bottom")
rightIcon.image(Image.open("resources/img/flui-br.png"), width=250)
"""

"""

STOCKS = [
    "NDWI",
    "Tmean",
    "precipitation",
]

DEFAULT_STOCKS = ["NDWI", "Tmean","precipitation"]

def stocks_to_str(stocks):
    return ",".join(stocks)

if "tickers_input" not in st.session_state:
    st.session_state.tickers_input = st.query_params.get(
        "stocks", stocks_to_str(DEFAULT_STOCKS)
    ).split(",")

def update_query_param():
    if st.session_state.tickers_input:
        st.query_params["stocks"] = stocks_to_str(st.session_state.tickers_input)
    else:
        st.query_params.pop("stocks", None)


# --- Columns
colDesc, colMap = st.columns([5, 5])

cardMap= colMap.container(
    border=True, height="content", vertical_alignment="center"
)

card1= colDesc.container(
    border=True, height="content", vertical_alignment="center"
)
card2 = colDesc.container(
    border=True, height="stretch", vertical_alignment="top"
)

chart_cell = colDesc.container(
    border=True, height="stretch", vertical_alignment="top"
)

with colDesc:
    # --- Load Brazil polygons
    gdf_brazil = dl.load_brazil_polygon()

    with card1:
        rightInput, leftInput = st.columns([1,4])
        # --- State selection
        states = gdf_brazil['name'].sort_values().unique().tolist()
        if "selected_state" not in st.session_state:
            st.session_state["selected_state"] = states[0]

        selected_state = rightInput.selectbox(
            "Select the state",
            states,
            index=states.index(st.session_state["selected_state"]),
            key="state_selector",
            width=400
        )

        tickers = leftInput.multiselect(
            "Weather variables",
            options=sorted(set(STOCKS) | set(st.session_state.tickers_input)),
            default=st.session_state.tickers_input,
            placeholder="Choose stocks to compare. Example: NVDA",
            accept_new_options=True,
        )

        tickers = [t.upper() for t in tickers]


    # --- Load GDF for selected state
    state_code = gdf_brazil[gdf_brazil['name'] == selected_state].iloc[0]['id']
    gdf = dl.load_polygon_state(state_code)
    city_name_key = 'name'
    municipalities = gdf[city_name_key].sort_values().unique().tolist()

    # --- Reset city selection if state changes
    if selected_state != st.session_state["selected_state"]:
        st.session_state["selected_state"] = selected_state
        st.session_state["selected_city_session"] = municipalities[0]

    if "selected_city_session" not in st.session_state:
        st.session_state["selected_city_session"] = municipalities[0]
    

# =====================================================
# RIGHT COLUMN - MAP
# =====================================================
with colMap:
    with cardMap:
        st.markdown("#### Select a city in the map or from the sidebar to visualize its information")

        # --- Create and style base map
        m = map.styledMap()
        m.fit_bounds(dl.state_bounds(gdf))

        # --- Add dark mask outside state
        folium.GeoJson(
            map.masks(gdf_brazil),
            style_function=lambda x: {"fillColor": "black", "color": "black", "fillOpacity": 0.7}
        ).add_to(m)

        # --- Add all municipalities polygons
        popup = folium.GeoJsonPopup(fields=[city_name_key], aliases=["City:"])
        folium.GeoJson(
            gdf,
            name="Municipalities",
            style_function=lambda x: {"fillColor": "#E0E0E0", "color": "gray", "weight": 1, "fillOpacity": 0.4},
            highlight_function=lambda x: {"fillColor": "#1976D2", "color": "#1976D2", "fillOpacity": 0.6},
            tooltip=folium.GeoJsonTooltip(fields=[city_name_key], aliases=["City:"]),
            zoom_on_click=True,
            popup=popup,
            popup_keep_highlighted=True,
        ).add_to(m)

        # --- Highlight currently selected city
        city_gdf = gdf[gdf[city_name_key] == st.session_state["selected_city_session"]]
        folium.GeoJson(
            city_gdf,
            name="Selected City",
            style_function=lambda x: {"fillColor": "#1976D2", "weight": 2, "fillOpacity": 0.6},
            highlight_function=lambda x: {"fillColor": "#1976D2", "color": "#1976D2", "fillOpacity": 0.6},
            tooltip=folium.GeoJsonTooltip(fields=[city_name_key], aliases=["City:"]),
        ).add_to(m)

        # --- Display map and capture interactions
        st_data = st_folium(m, width='100%')

# =====================================================
# LEFT COLUMN - CITY INFORMATION
# =====================================================
with colDesc:
    with card2:
        # --- Handle map click
        if st_data and st_data.get("last_active_drawing"):
            properties = st_data["last_active_drawing"].get("properties", {})
            if properties and city_name_key in properties:
                clicked_city = properties[city_name_key]
                if clicked_city != st.session_state["selected_city_session"]:
                    st.session_state["selected_city_session"] = clicked_city
                    st.rerun()

        # --- Display city info
        if st.session_state["selected_city_session"]:
            dl.display_city_info(
                selected_city=st.session_state["selected_city_session"],
                gdf=gdf
            )

    # Load the data
    horizon_map = {
        "1 Months": "1mo",
        "3 Months": "3mo",
        "6 Months": "6mo",
        "1 Year": "1y",
        "5 Years": "5y",
        "10 Years": "10y",
        "20 Years": "20y",
    }

    data = pd.read_csv('flui_app/data_manager/output.csv', sep=',')

    @st.cache_resource(show_spinner=False)
    def load_data(tickers, period):
        #tickers_obj = yf.Tickers(tickers)
        data = pd.read_csv('flui_app/data_manager/output.csv', sep=',')
        #data = tickers.history(period=period)
        if data is None:
            raise RuntimeError("Returned no data.")
        return data
    
    horizon = st.pills(
        "Time horizon",
        options=list(horizon_map.keys()),
        default="6 Months",
    )


    data = load_data(tickers, horizon_map[horizon])
    df_sorted = data.sort_values('date', ascending=True)
    
    #normalized = data.div(data.iloc[0])

    with chart_cell:
        chart = (
            alt.Chart(df_sorted)
            .mark_line(color="#1b9e77")  # You can change color if desired
            .encode(
                x=alt.X("date:T", title="Date"),
                y=alt.Y("precipitation:Q", title="Precipitation (mm)"),
                tooltip=["date:T", "precipitation:Q"]
            )
            .properties(
                width=700,
                height=350,
                title="Precipitation Over Time"
            )
            .interactive()  # allows zooming and panning
        )

        st.altair_chart(chart, use_container_width=True)
