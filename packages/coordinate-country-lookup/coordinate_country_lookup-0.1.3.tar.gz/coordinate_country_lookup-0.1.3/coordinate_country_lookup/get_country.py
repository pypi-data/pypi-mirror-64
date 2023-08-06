# For each latitude and longitude in 2000 year data, compute which country
# it is
import geopandas as gpd
from shapely.geometry import Point, Polygon
import os
from coordinate_country_lookup

shapefile_dir = os.path.join(os.path.dirname(mypackage.__file__), 'countries')
shapefile = os.path.join(templates_dir, 'ne_110m_admin_0_countries.shp')

# shapefile = '../countries/ne_110m_admin_0_countries.shp'
gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
gdf.columns = ['country', 'country_code', 'geometry']

polygons = list(gdf['geometry'])
countries = gdf['country'].values
country_codes = gdf['country_code'].values

def get_country(lat, lon, polygons=polygons, countries=countries, country_codes=country_codes):
    for i, polygon in enumerate(polygons):
        if Point(lon, lat).within(polygon):
            return countries[i], country_codes[i]
    return None, None
