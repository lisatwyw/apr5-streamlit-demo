
import folium, geopy
import streamlit as st
from branca.element import Figure
from pathlib import Path
from streamlit_folium import st_folium, folium_static

def map_loc( address ):
  '''
  Creates a map
  '''

  geolocator = geopy.geocoders.Nominatim(user_agent="3")
  location = geolocator.geocode( address )         
  lx,ly=location.longitude, location.latitude
  #  If you pass coordinates as positional args, please make sure that the order is (latitude, longitude) or (y, x) in Cartesian terms.
  fig = Figure( width=400,height=200)
  a_map = folium.Map(location = [ly,lx], zoom_start = 16)
  
  p  = geopy.point.Point(ly, lx)
  
  gl = geopy.geocoders.Nominatim(user_agent="my_test") # Without the user_agent it raises a ConfigurationError.
  site = gl.reverse(p)
  site_name = site[0]
  folium.Marker( location=[ly, lx], popup='Default popup Marker3',tooltip=site_name).add_to(m)
  fig.add_child(a_map)
  
  return fig, a_map, site_name


st.title( 'My first web app' )

f = 'README.md'
mkd = Path( f ).read_text()
st.markdown( mkd )

st.header( 'My favourite places' )
st.markdown("# Top heading")
st.markdown("## Subheading")


try:
  address = 'Stanley Park, Vancouver'
  fig, a_map, site_name = map_loc(address)
  st_folium( a_map )
except Exception as e:
  print( e ) 
  