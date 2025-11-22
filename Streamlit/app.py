import streamlit as st
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
import folium

st.title("CRC NAIP 2011 NDVI Viewer (True NDVI Scale)")

# ---------------------------------------------------
# Load NDVI TIFF from PIL so its cloud compatable
# ---------------------------------------------------
tif_path = "data/CRC_NAIP_2011_NDVI.tif"

# Extract band + bounds
img = Image.open(tif_path)
ndvi = np.array(img).astype(float)


left, bottom, right, top = (-109.870, 38.123, -109.855, 38.140)  

# ---------------------------------------------------
# NDVI colormap with true NDVI scale (-1 to 1)
# ---------------------------------------------------

# NDVI threshold breaks (bins)
ndvi_breaks = [-1.0, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0]

# Colors corresponding to those bins — official GEE NDVI palette
ndvi_colors = [
    '#FFFFFF',  # <=0.0 (no veg)
    '#CE7E45',  # 0.0–0.1
    '#FCD163',  # 0.1–0.2
    '#99B718',  # 0.2–0.3
    '#66A000',  # 0.3–0.4
    '#207401',  # 0.4–0.5
    '#056201',  # 0.5–0.6
    '#004C00',  # 0.6–0.7
    '#023B01',  # 0.7–0.8
    '#012E01',  # >0.8 dense
]

# Map NDVI values to the correct color bin
def ndvi_colormap(val):
    """Map NDVI value (-1 to 1) to correct GEE-style color."""
    if np.isnan(val):
        return (0, 0, 0, 0)  # transparent for NaN
    
    for i in range(len(ndvi_breaks) - 1):
        if ndvi_breaks[i] <= val < ndvi_breaks[i + 1]:
            hex_color = ndvi_colors[i]
            rgb = tuple(int(hex_color[j:j+2], 16) / 255 for j in (1, 3, 5))
            return (rgb[0], rgb[1], rgb[2], 1.0)
    
    # fallback (should not happen)
    return (0, 0, 0, 1)

# ---------------------------------------------------
# Create Folium map centered on raster
# ---------------------------------------------------
center_lat = (top + bottom) / 2
center_lon = (left + right) / 2

m = folium.Map(location=[center_lat, center_lon], zoom_start=14)

# Add the raster with TRUE NDVI values and our custom colormap
folium.raster_layers.ImageOverlay(
    image=ndvi,                       # REAL NDVI (-1 → 1)
    bounds=[[bottom, left], [top, right]],
    colormap=ndvi_colormap,           # exact GEE palette
    opacity=0.8
).add_to(m)

# ---------------------------------------------------
# 4️⃣ Add Legend (GEE Style)
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
# 5️⃣ Show map in Streamlit
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
