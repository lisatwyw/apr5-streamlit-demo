
import folium, geopy
import streamlit as st
from branca.element import Figure
from pathlib import Path
from streamlit_folium import st_folium, folium_static
import plotly.express as px
import polars as pol
import pandas as pd



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
  folium.Marker( location=[ly, lx], popup='Default popup Marker3',tooltip=site_name).add_to(a_map)
  fig.add_child(a_map)
  
  return fig, a_map, site_name


st.title( 'My first web app' )

f = 'README.md'
mkd = Path( f ).read_text()
st.markdown( mkd )

st.header( 'My favourite places' )
st.markdown("# Top heading")
st.markdown("## Subheading")

default_addr = 'Iron Dog Books, Vancouver'
try:
  address = st.text_area( 'Try entering name of your favourite place:', value=default_addr )
  mkdwn='''
  ### Have you tried below?
  - [ ] Simon Fraser University, Vancouver
  - [x] Stanley Park, Vancouver
  - [x] University of British Columbia, Vancouver
  
  '''
  st.markdown( mkdwn )
  fig, a_map, site_name = map_loc(address)
  st_folium( a_map )
except:    
  try:
    fig, a_map, site_name = map_loc(default_addr)
    st_folium( a_map )
  except Exception as e:
    print( e ) 
  


import pandas as pd
file = st.file_uploader( 'Upload', type=['csv'] )
try:      
  df=pd.read_csv( file )
  st.dataframe( df )

  for c in df.columns:
    try:
      st.header( c )    
      fig = px.histogram(df[c])    
      st.plotly_chart( fig )
    except Exception as e:
      st.write( e )
except Exception as e:
  print(e)
  df = None


