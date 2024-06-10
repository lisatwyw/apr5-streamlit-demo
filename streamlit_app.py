#    Copyright 2024 lisatwyw Lisa Y.W. Tang
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


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
  folium.Marker( location=[ly, lx], popup=site_name,tooltip=site_name).add_to(a_map)
  fig.add_child(a_map)
  
  return fig, a_map, site_name


st.set_page_config(layout="wide")
st.title( 'My first web app' )

f = 'README.md'; mkd = Path( f ).read_text(); st.markdown( mkd )

st.title( 'My favourite places' )
default_addr = 'Banana Leaf, Commercial Drive, Vancouver'
# default_addr = 'Kamei Broadway, Vancouver'
# default_addr = 'Iron Dog Books, Vancouver'

try:
  address = st.text_area( 'Try entering name of your favourite place:', value=default_addr )
  mkdwn='''
  ### Have you tried below?
  - [x] BCCDC
  - [ ] Salmon N' Bannock, Vancouver
  - [x] Simon Fraser University, Vancouver
  - [ ] Stanley Park, Vancouver
  - [x] University of British Columbia, Vancouver
  - [x] Vancouver General Hospital 
    
  '''
  st.markdown( mkdwn )
  fig, a_map, site_name = map_loc(address)
  st_folium( a_map )
except:    
  try:
    fig, a_map, site_name = map_loc(default_addr)
    st_folium( a_map, width = 600, height=1200, returned_objects=[] )
  except Exception as e:
    print( e ) 
  

st.header( 'Show me data' )
st.text( 'Below widget will try to generate graphs of an input CSV' )
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


html = '<br>' *1000
st.components.v1.html(html, height=1000 )
st.header( 'Drum roll please...' )

audio_file = open('data/drum-roll-sound-effect.mp3', 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes, format='audio/ogg')
license='License: Attribution 4.0 International (CC BY 4.0). You are allowed to use sound effects free of charge and royalty free in your multimedia projects for commercial or non-commercial purposes.'
st.write( license )




