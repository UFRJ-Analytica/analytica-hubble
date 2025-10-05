import streamlit as st
import geopandas as gpd
from shapely.geometry import box
import folium


def masks(gdf):
    world = gpd.GeoDataFrame(geometry=[box(-180, -90, 180, 90)], crs="EPSG:4326")
    state_geom = gpd.GeoDataFrame(geometry=[gdf.unary_union], crs="EPSG:4326")
    
    mask = gpd.overlay(world, state_geom, how="difference")
    return mask

def styledMap():
    # --- Map centered in the state
    m = folium.Map(location=[-22.9, -43.2], 
            zoom_start=8, 
            min_zoom=8, 
            max_bounds=True, 
            tiles="cartodb positron")
    
    # --- Remove black box when selecting
    css_to_inject = """
    <style>
        .leaflet-interactive:focus {
            outline: none;
        }
    </style>
    """
    m.get_root().html.add_child(folium.Element(css_to_inject))

    return m