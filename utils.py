import folium
import pandas as pd
from haversine import haversine, Unit
from geopandas import GeoDataFrame, points_from_xy
import googlemaps

radio = 2
unit = 'km'

geo_source = 11.220316, -74.198647


def get_coords(address: str, API_KEY: str) -> tuple:

    try:
        gmaps = googlemaps.Client(key=f'{API_KEY}')
        geocode_result = gmaps.geocode(address)

        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']

        results = (lat, lng)
    except:
        results = (pd.NA, pd.NA)

    return results


def cal_dist(geo_source: tuple, geo_destination: tuple, unit: str) -> float:

    if unit == 'km':
        distance = haversine(geo_source, geo_destination, Unit.KILOMETERS)
    elif unit == 'm':
        distance = haversine(geo_source, geo_destination, Unit.METERS)
    elif unit == 'miles':
        distance = haversine(geo_source, geo_destination, Unit.MILES)

    return round(distance, 2)


def distance_estac(geo_source: tuple, df, radio: int, unit: str):

    distancia = []
    source = []

    for i in range(len(df)):
        distancia.append(
            cal_dist(geo_source, (df['LAT'][i], df['LNG'][i]), unit))
        source.append(geo_source)

    new_df = df.copy()
    new_df['SOURCE'] = source
    new_df['DISTANCE'] = distancia
    new_df = new_df[new_df['DISTANCE'] <= radio]
    new_df = new_df.reset_index()
    new_df = new_df.drop(columns='index')

    return new_df.sort_values(by='DISTANCE', ascending=True)


def html_template(df, i: int) -> str:

    html = f"""<b>MARCA:</b> {df.Bandera[i]} <br>
            <b>NAME:</b> {df.Nombre_comercial[i]} <br>
            <b>PRODUCTO:</b> {df.Producto[i]} <br>
            <b>PRECIO:</b> {df.Precio[i]} <br>
            <b>DISTANCE:</b> {round(df.DISTANCE[i],2)}<br>
            <b>DIRECCION:</b> {df.Direccion[i]}<br>
            <b>UNIT:</b> {unit}<br>"""
    return html


def marker_rest(df, mapa, unit, oil, icono):

    df = df[df['Producto'] == oil]
    df = df.reset_index()
    df = df.drop(columns='index')
    color_ = ""

    for i in range(len(df)):

        if df['Precio'][i] == df['Precio'].min():
            color_ = 'darkgreen'
            html = html_template(df, i)
        elif df['Precio'][i] == df['Precio'].max():
            color_ = 'darkred'
            html = html_template(df, i)
        else:
            color_ = 'orange'
            html = html_template(df, i)

        iframe = folium.IFrame(html, figsize=(6, 3))
        popup = folium.Popup(iframe)
        folium.Marker(location=[df['LAT'][i], df['LNG'][i]], icon=folium.Icon(
            color=color_, icon_color='white', icon=icono, prefix='glyphicon'), popup=popup).add_to(mapa)

    return
