import streamlit as st
import pandas as pd
from PIL import Image
from setting import API_KEY

# Tools
import folium
from geopandas import GeoDataFrame, points_from_xy

from utils import get_coords, distance_estac, marker_rest
from streamlit_folium import folium_static


image = Image.open('img/gasolina-vende.jpg')

st.sidebar.image(image, caption='Gasolineras Cercanas App ⛽', width=300)
app_mode = st.sidebar.selectbox(
    "Escoge el modo de la aplicacion", ["Run App", "About Me"])

if app_mode == "Run App":
    st.title('Gasolineras Cercanas App ⛽')
    st.markdown(
        'Aplicacion para saber la informacion de las gasolineras en un radio de 1, 2 o 3 kilometros de un punto.\n' +
        'Solo ingresa en ubicacion central la direccion del punto de referencia que desees.')

    df_map = pd.read_csv('DATASET_LIMPIO.csv')
    cities = list(df_map['Municipio'].unique())

    c1, c2 = st.columns((9, 1))
    choose_city = c1.selectbox("Escoge la ciudad", cities)
    central_location = c1.text_input(
        'Ubicacion central', 'Centro Comercial Las Palmas, Transversal 9, Privilegios, Santa Marta, Magdalena, Colombia')

    API_KEY = API_KEY

    rad = c1.slider('Radio', 1, 3, 1)

    oil = list(df_map['Producto'].unique())

    choose_products = c1.selectbox("Escoge el tipo de combustible", oil)

    if len(central_location) != 0 and c1.button('MOSTRAR MAPA'):

        geo_source = get_coords(address=central_location, API_KEY=API_KEY)
        unit = 'km'

        print(f"1 -> {geo_source}")

        results = distance_estac(geo_source, df_map, rad, unit)
        results.reset_index(inplace=True)
        results.drop(columns='index', inplace=True)

        gdf_results = GeoDataFrame(
            results, geometry=points_from_xy(results.LNG, results.LAT))

        gdf_results_2 = gdf_results[gdf_results['Producto'] == choose_products]
        gdf_results_2.reset_index(inplace=True)
        gdf_results_2.drop(columns='index', inplace=True)
        icono = 'usd'

        m = folium.Map([geo_source[0], geo_source[1]], zoom_start=15)

        folium.Circle(
            radius=int(rad)*1000,
            location=[geo_source[0], geo_source[1]],
            color='green',
            fill='green'
        ).add_to(m)

        folium.Marker(
            location=[geo_source[0], geo_source[1]],
            icon=folium.Icon(color='black', icon_color='white',
                             icon="home", prefix='glyphicon'),
            popup="<b>Centroid</b>"
        ).add_to(m)

        marker_rest(gdf_results_2, m, unit, choose_products, icono)
        folium_static(m)
elif app_mode == "About Me":

    st.title("Gasolineras Cercanas App ⛽")
    st.success("Puedes contactarme sin problemas 👇")
    c1, c3 = st.columns((3, 3))
    c1.markdown('* [**Github**](https://github.com/Tavo17s) 🚀')
    c1.markdown(
        '* [**Linkedin**](https://www.linkedin.com/in/gustavo-solano-navarro-653907239/) 🚀')
    img2 = Image.open('img/sadaharu.png')
    c3.image(img2, width=230)
