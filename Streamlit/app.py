import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
import folium

st.title("CRC NAIP 2011 NDVI Viewer")

# ---------------------------------------------------
# 1) Load NDVI TIFF using PIL (Safe on Streamlit Cloud)
# ---------------------------------------------------
tif_path = "data/CRC_NAIP_2011_NDVI.tif"

img = Image.open(tif_path)
ndvi = np.array(img)  # REAL NDVI values (-1 to 1)

# ---------------------------------------------------
# 2) Geospatial Bounds (manually inserted)
# ---------------------------------------------------
left  = -109.639353
right = -109.628493
bottom = 38.262410
top    = 38.268114

# Map center
center_lat = (top + bottom) / 2
center_lon = (left + right) / 2

# ---------------------------------------------------
# 3) NDVI Breaks + Colors (GEE style)
# ---------------------------------------------------
ndvi_breaks = [-1.0, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0]

ndvi_colors = [
    '#FFFFFF',
    '#CE7E45',
    '#FCD163',
    '#99B718',
    '#66A000',
    '#207401',
    '#056201',
    '#004C00',
    '#023B01',
    '#012E01'
]

def ndvi_colormap(val):
    """Map NDVI value to RGBA tuple."""
    if np.isnan(val):
        return (0, 0, 0, 0)
    for i in range(len(ndvi_breaks) - 1):
        if ndvi_breaks[i] <= val < ndvi_breaks[i + 1]:
            hex_color = ndvi_colors[i]
            r = int(hex_color[1:3], 16) / 255
            g = int(hex_color[3:5], 16) / 255
            b = int(hex_color[5:7], 16) / 255
            return (r, g, b, 1)
    return (0, 0, 0, 1)

# ---------------------------------------------------
# 4) Folium map
# ---------------------------------------------------
m = folium.Map(location=[center_lat, center_lon], zoom_start=15)

folium.raster_layers.ImageOverlay(
    image=ndvi,
    bounds=[[bottom, left], [top, right]],
    colormap=ndvi_colormap,
    opacity=0.8
).add_to(m)

# ---------------------------------------------------
# 5) Legend
# ---------------------------------------------------
legend_html = """
 <div style="
 position: fixed; 
 bottom: 50px; left: 50px; width: 180px; height: 280px; 
 background-color: white; 
 border:2px solid grey; z-index:9999; 
 font-size:14px; padding: 10px;">
 <b>NDVI Legend</b><br>
 <i style="background:#FFFFFF;width:18px;height:18px;float:left;margin-right:8px;"></i>No vegetation (≤ 0.0)<br>
 <i style="background:#CE7E45;width:18px;height:18px;float:left;margin-right:8px;"></i>0.0 – 0.1<br>
 <i style="background:#FCD163;width:18px;height:18px;float:left;margin-right:8px;"></i>0.1 – 0.2<br>
 <i style="background:#99B718;width:18px;height:18px;float:left;margin-right:8px;"></i>0.2 – 0.3<br>
 <i style="background:#66A000;width:18px;height:18px;float:left;margin-right:8px;"></i>0.3 – 0.4<br>
 <i style="background:#207401;width:18px;height:18px;float:left;margin-right:8px;"></i>0.4 – 0.5<br>
 <i style="background:#056201;width:18px;height:18px;float:left;margin-right:8px;"></i>0.5 – 0.6<br>
 <i style="background:#004C00;width:18px;height:18px;float:left;margin-right:8px;"></i>0.6 – 0.7<br>
 <i style="background:#023B01;width:18px;height:18px;float:left;margin-right:8px;"></i>0.7 – 0.8<br>
 <i style="background:#012E01;width:18px;height:18px;float:left;margin-right:8px;"></i>0.8 – 1.0<br>
 </div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# ---------------------------------------------------
# 6) Display Map
# ---------------------------------------------------
st.subheader("NDVI Map")
st_folium(m, width=700, height=500)

# ---------------------------------------------------
# 7) NDVI Histogram
# ---------------------------------------------------
st.subheader("NDVI Histogram")
fig, ax = plt.subplots()
ax.hist(ndvi[np.isfinite(ndvi)], bins=50, color="green")
ax.set_xlabel("NDVI")
ax.set_ylabel("Pixel Count")
st.pyplot(fig)


