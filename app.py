import streamlit as st
import leafmap.foliumap as leafmap
import os

st.set_page_config(layout="wide")
st.title("Urban Sprawl Impacts on Soil Resources - Tours Metropolitan Area")

st.sidebar.title("Layer Controls")

# Initialize the map
m = leafmap.Map(center=[47.39, 0.688], zoom=11, esri=True)



# Define raster layers (projected to EPSG:4326)
raster_layers = {
    "Urban cover 2015 (Blue)": ("https://huggingface.co/datasets/lamia9598/app/resolve/main/urban_cover_2015_cog.tif", "Blues"),
    "Urban cover 2040 BAU (Red)": ("https://huggingface.co/datasets/lamia9598/app/resolve/main/urban_cover_2040_bau_cog.tif", "Reds"),
    "Urban cover 2040 Compact (Green)": ("https://huggingface.co/datasets/lamia9598/app/resolve/main/urban_cover_2040_compact_cog.tif", "Greens"),
    "Soil Vulnerability (Magma)": ("https://huggingface.co/datasets/lamia9598/app/resolve/main/soil_vulnerability_cog.tif", "magma")
}


# Display layers with high-quality settings
for label, (file_path, cmap) in raster_layers.items():
    if st.sidebar.checkbox(f"Show {label}", value=("2015" in label or "BAU" in label)):
        m.add_raster(
            file_path,
            layer_name=label,
            colormap=cmap,
            rescale=True,
            vmin=1,
            vmax=255,
            nodata=0
        )

# Add vector overlay (boundary shapefile)
vector_file = "scotclipped1_4326.geojson"

if os.path.exists(vector_file):
    m.add_vector(vector_file, layer_name="Study Area", shown=True)
else:
    st.warning(f"Boundary file not found: {vector_file}")

# Enable layer control and display map
m.add_layer_control()
m.to_streamlit(width=1200, height=700)
