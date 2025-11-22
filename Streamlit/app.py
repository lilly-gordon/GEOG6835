import streamlit as st
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
import folium
from matplotlib import colors

st.title("CRC NAIP 2011 NDVI Viewer")

# ---------------------------------------------------
# 1️⃣ Load NDVI TIFF
# ---------------------------------------------------
tif_path = r"C:\Users\lilli\OneDrive - USU\Desktop\GEO6835\GEOG6835\Week10\Streamlit\data\CRC_NAIP_2011_NDVI.tif"

with rasterio.open(tif_path) as src:
    ndvi = src.read(1)
    bounds = src.bounds

# ---------------------------------------------------
# 2️⃣ Create NDVI colormap (must come BEFORE ImageOverlay)
# ---------------------------------------------------
ndvi_colors = [
    '#FFFFFF',  # 0.0 - no veg
    '#CE7E45',  # 0.1
    '#FCD163',  # 0.2
    '#99B718',  # 0.3
    '#66A000',  # 0.4
    '#207401',  # 0.5
    '#056201',  # 0.6
    '#004C00',  # 0.7
    '#023B01',  # 0.8
    '#012E01',  # 0.9+
]

cmap = colors.LinearSegmentedColormap.from_list("ndvi", ndvi_colors)

def ndvi_colormap(val):
    rgba = cmap(val)
    return (rgba[0], rgba[1], rgba[2], rgba[3])

# ---------------------------------------------------
# 3️⃣ Create Folium map
# ---------------------------------------------------
center_lat = (bounds.top + bounds.bottom) / 2
center_lon = (bounds.left + bounds.right) / 2

m = folium.Map(location=[center_lat, center_lon], zoom_start=14)

folium.raster_layers.ImageOverlay(
    image=ndvi,
    bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
    colormap=ndvi_colormap,
    opacity=0.8
).add_to(m)

# ---------------------------------------------------
# 4️⃣ Add Legend HTML
# ---------------------------------------------------
legend_html = """
 <div style="
 position: fixed; 
 bottom: 50px; left: 50px; width: 180px; height: 280px; 
 background-color: white; 
 border:2px solid grey; z-index:9999; 
 font-size:14px; padding: 10px;">
 <b>NDVI Legend</b><br>
 <i style="background:#FFFFFF;width:18px;height:18px;float:left;margin-right:8px;"></i>No vegetation (0.0)<br>
 <i style="background:#CE7E45;width:18px;height:18px;float:left;margin-right:8px;"></i>Sparse/Bare (0.1)<br>
 <i style="background:#FCD163;width:18px;height:18px;float:left;margin-right:8px;"></i>Low vegetation (0.2)<br>
 <i style="background:#99B718;width:18px;height:18px;float:left;margin-right:8px;"></i>Moderate (0.3)<br>
 <i style="background:#66A000;width:18px;height:18px;float:left;margin-right:8px;"></i>Healthy (0.4)<br>
 <i style="background:#207401;width:18px;height:18px;float:left;margin-right:8px;"></i>Very Healthy (0.5)<br>
 <i style="background:#056201;width:18px;height:18px;float:left;margin-right:8px;"></i>Dense Veg (0.6)<br>
 <i style="background:#004C00;width:18px;height:18px;float:left;margin-right:8px;"></i>Very Dense (0.7)<br>
 <i style="background:#023B01;width:18px;height:18px;float:left;margin-right:8px;"></i>Ultra Dense (0.8+)<br>
 </div>
"""

m.get_root().html.add_child(folium.Element(legend_html))

folium.LayerControl().add_to(m)

# ---------------------------------------------------
# 5️⃣ Display Map in Streamlit
# ---------------------------------------------------
st.subheader("NDVI Map")
st_folium(m, width=700, height=500)

# ---------------------------------------------------
# 6️⃣ NDVI Histogram
# ---------------------------------------------------
st.subheader("NDVI Histogram")
fig, ax = plt.subplots()
ax.hist(ndvi[np.isfinite(ndvi)], bins=50, color="green")
ax.set_xlabel("NDVI")
ax.set_ylabel("Pixel Count")
st.pyplot(fig)
