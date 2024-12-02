import pandas                        as pd
import geopandas                     as gpd
import core.HelperTools              as ht

import folium
# from folium.plugins import HeatMap
import streamlit as st
from streamlit_folium import folium_static
from branca.colormap import LinearColormap



def sort_by_plz_add_geometry(dfr, dfg, pdict): 
    """
    The function `sort_by_plz_add_geometry` sorts an input dataframe by postal code, merges it with
    geospatial data based on a specified geocode column, and returns a GeoDataFrame with geometry
    information.
    
    :param dfr: The `dfr` parameter is the input DataFrame containing postal code and other relevant
    data
    :param dfg: The `dfg` parameter in the `sort_by_plz_add_geometry` function refers to a GeoDataFrame
    containing geometries for postal codes. This GeoDataFrame likely includes spatial information such
    as polygons or points representing the geographic locations corresponding to postal codes
    :param pdict: The `pdict` parameter is a dictionary containing mapping of columns, including geocode
    information. It likely includes information on how to match columns between the input dataframe
    `dfr` and the geospatial dataframe `dfg` for merging based on a common geocode column
    :return: A geospatial dataframe with the merged data, including geometry, is being returned.
    """

    dframe                  = dfr.copy()
    df_geo                  = dfg.copy()
    
    # Sort the dataframe `dfr` by postal code (PLZ).
    sorted_df               = dframe\
        .sort_values(by='PLZ')\
        .reset_index(drop=True)\
        .sort_index()
    
    # Merge the sorted dataframe with a geospatial dataframe `dfg` on a geocode column in `pdict`.   
     
    sorted_df2              = sorted_df.merge(df_geo, on=pdict["geocode"], how ='left')
    sorted_df3              = sorted_df2.dropna(subset=['geometry'])

    # Converts the 'geometry' column to a GeoSeries and returns a GeoDataFrame.
    sorted_df3['geometry']  = gpd.GeoSeries.from_wkt(sorted_df3['geometry'])
    ret                     = gpd.GeoDataFrame(sorted_df3, geometry='geometry')
    
    return ret

# -----------------------------------------------------------------------------
@ht.timer
def preprop_lstat(dfr, dfg, pdict):
    """
    The function preprop_lstat preprocesses electric charging station data from a CSV file, filtering
    for stations in Berlin within specified postal codes and returning a GeoDataFrame with geometries.
    
    :param dfr: The `dfr` parameter in the `preprop_lstat` function is a DataFrame containing the
    electric charging station data. It likely includes information such as postal codes, states,
    latitude, longitude, and charging station power ratings. The function preprocesses this data by
    filtering for charging stations in Berlin within
    :param dfg: The parameter `dfg` in the `preprop_lstat` function is a GeoDataFrame that contains
    postal code geometries. This GeoDataFrame likely includes spatial information such as polygons or
    points representing the boundaries or locations of postal code areas in a geographic area, such as
    Berlin in this case
    :param pdict: The `pdict` parameter in the `preprop_lstat` function is a dictionary containing
    mappings and other parameters, including geocode information. It likely holds key-value pairs that
    are used within the function for processing the electric charging station data. If you provide the
    contents of the `pdict`
    :return: A GeoDataFrame with the charging stations data for Berlin within specified postal codes,
    including geometries, is being returned.
    """

    dframe                  = dfr.copy()
    df_geo                  = dfg.copy()
    
    dframe2               	= dframe.loc[:,['Postleitzahl', 'Bundesland', 'Breitengrad', 'Längengrad', 'Nennleistung Ladeeinrichtung [kW]']]
    dframe2.rename(columns  = {"Nennleistung Ladeeinrichtung [kW]":"KW", "Postleitzahl": "PLZ"}, inplace = True)

    # Convert to string
    dframe2['Breitengrad']  = dframe2['Breitengrad'].astype(str)
    dframe2['Längengrad']   = dframe2['Längengrad'].astype(str)

    # Now replace the commas with periods
    dframe2['Breitengrad']  = dframe2['Breitengrad'].str.replace(',', '.')
    dframe2['Längengrad']   = dframe2['Längengrad'].str.replace(',', '.')

    dframe3                 = dframe2[(dframe2["Bundesland"] == 'Berlin') & 
                                            (dframe2["PLZ"] > 10115) &  
                                            (dframe2["PLZ"] < 14200)]
    
    ret = sort_by_plz_add_geometry(dframe3, df_geo, pdict)
    
    return ret
    

# -----------------------------------------------------------------------------
@ht.timer
def count_plz_occurrences(df_lstat2):
    """
    The function `count_plz_occurrences` counts the number of charging stations per postal code in a
    GeoDataFrame.
    
    :param df_lstat2: The `df_lstat2` parameter is a GeoDataFrame that contains charging station data.
    The function `count_plz_occurrences` takes this GeoDataFrame as input and groups the data by postal
    code (PLZ), counting the occurrences of charging stations for each postal code. The function then
    returns a
    :return: The function `count_plz_occurrences` returns a DataFrame with the count of charging
    stations per postal code, including the geometry information.
    """

    # Group by PLZ and count occurrences, keeping geometry
    result_df = df_lstat2.groupby('PLZ').agg(
        Number=('PLZ', 'count'),
        geometry=('geometry', 'first')
    ).reset_index()
    
    return result_df
    
# -----------------------------------------------------------------------------
# @ht.timer
# def preprop_geb(dfr, pdict):
#     """Preprocessing dataframe from gebaeude.csv"""
#     dframe      = dfr.copy()
    
#     dframe2     = dframe .loc[:,['lag', 'bezbaw', 'geometry']]
#     dframe2.rename(columns      = {"bezbaw":"Gebaeudeart", "lag": "PLZ"}, inplace = True)
    
    
#     # Now, let's filter the DataFrame
#     dframe3 = dframe2[
#         dframe2['PLZ'].notna() &  # Remove NaN values
#         ~dframe2['PLZ'].astype(str).str.contains(',') &  # Remove entries with commas
#         (dframe2['PLZ'].astype(str).str.len() <= 5)  # Keep entries with 5 or fewer characters
#         ]
    
#     # Convert PLZ to numeric, coercing errors to NaN
#     dframe3['PLZ_numeric'] = pd.to_numeric(dframe3['PLZ'], errors='coerce')

#     # Filter for PLZ between 10000 and 14200
#     filtered_df = dframe3[
#         (dframe3['PLZ_numeric'] >= 10000) & 
#         (dframe3['PLZ_numeric'] <= 14200)
#     ]

#     # Drop the temporary numeric column
#     filtered_df2 = filtered_df.drop('PLZ_numeric', axis=1)
    
#     filtered_df3 = filtered_df2[filtered_df2['Gebaeudeart'].isin(['Freistehendes Einzelgebäude', 'Doppelhaushälfte'])]
    
#     filtered_df4 = (filtered_df3\
#                  .assign(PLZ=lambda x: pd.to_numeric(x['PLZ'], errors='coerce'))[['PLZ', 'Gebaeudeart', 'geometry']]
#                  .sort_values(by='PLZ')
#                  .reset_index(drop=True)
#                  )
    
#     ret                     = filtered_df4.dropna(subset=['geometry'])
        
#     return ret
    
# -----------------------------------------------------------------------------
@ht.timer
def preprop_resid(dfr, dfg, pdict):
    """
    The function preprop_resid preprocesses resident data by filtering for postal codes in Berlin within
    a specified range and returns a GeoDataFrame with geometries.
    
    :param dfr: The `dfr` parameter is a DataFrame containing resident data. It likely includes
    information such as postal codes, number of residents, latitude, and longitude for different
    locations
    :param dfg: The `dfg` parameter in the `preprop_resid` function is a GeoDataFrame containing the
    postal code geometries. It likely includes information about the shapes and locations of postal code
    areas in a geographic region, such as Berlin in this case. This data is used to spatially join the
    :param pdict: The `pdict` parameter in the `preprop_resid` function is a dictionary containing
    mappings and other parameters, including geocode information. It likely holds various settings,
    configurations, or data needed for processing the resident data
    :return: A GeoDataFrame with resident data, including geometries, is being returned.
    """
    
    dframe                  = dfr.copy()
    df_geo                  = dfg.copy()    
    
    dframe2               	= dframe.loc[:,['plz', 'einwohner', 'lat', 'lon']]
    dframe2.rename(columns  = {"plz": "PLZ", "einwohner": "Einwohner", "lat": "Breitengrad", "lon": "Längengrad"}, inplace = True)

    # Convert to string
    dframe2['Breitengrad']  = dframe2['Breitengrad'].astype(str)
    dframe2['Längengrad']   = dframe2['Längengrad'].astype(str)

    # Now replace the commas with periods
    dframe2['Breitengrad']  = dframe2['Breitengrad'].str.replace(',', '.')
    dframe2['Längengrad']   = dframe2['Längengrad'].str.replace(',', '.')

    dframe3                 = dframe2[ 
                                            (dframe2["PLZ"] > 10000) &  
                                            (dframe2["PLZ"] < 14200)]
    
    ret = sort_by_plz_add_geometry(dframe3, df_geo, pdict)
    
    return ret


# -----------------------------------------------------------------------------
@ht.timer
def make_streamlit_electric_Charging_resid(dfr1, dfr2):
    """
    This function is designed to create a Streamlit app for electric vehicle charging at residential
    locations using two input dataframes.
    
    :param dfr1: It seems like you were about to ask for an explanation of the parameters `dfr1` and
    `dfr2`. Could you please provide more context or finish your question so I can assist you better?
    :param dfr2: It seems like your message got cut off. Could you please provide more information about
    the parameters and what you would like to achieve with the function
    `make_streamlit_electric_Charging_resid(dfr1, dfr2)`?
    """
    
    dframe1 = dfr1.copy()
    dframe2 = dfr2.copy()


    # Streamlit app
    st.title('Heatmaps: Electric Charging Stations and Residents')

    # Create a radio button for layer selection
    # layer_selection = st.radio("Select Layer", ("Number of Residents per PLZ (Postal code)", "Number of Charging Stations per PLZ (Postal code)"))

    layer_selection = st.radio("Select Layer", ("Residents", "Charging_Stations"))

    # Create a Folium map
    m = folium.Map(location=[52.52, 13.40], zoom_start=10)

    if layer_selection == "Residents":
        
        # Create a color map for Residents
        color_map = LinearColormap(colors=['yellow', 'red'], vmin=dframe2['Einwohner'].min(), vmax=dframe2['Einwohner'].max())

        # Add polygons to the map for Residents
        for idx, row in dframe2.iterrows():
            folium.GeoJson(
                row['geometry'],
                style_function=lambda x, color=color_map(row['Einwohner']): {
                    'fillColor': color,
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': 0.7
                },
                tooltip=f"PLZ: {row['PLZ']}, Einwohner: {row['Einwohner']}"
            ).add_to(m)
        
        # Display the dataframe for Residents
        # st.subheader('Residents Data')
        # st.dataframe(gdf_residents2)

    else:
        # Create a color map for Numbers

        color_map = LinearColormap(colors=['yellow', 'red'], vmin=dframe1['Number'].min(), vmax=dframe1['Number'].max())

    # Add polygons to the map for Numbers
        for idx, row in dframe1.iterrows():
            folium.GeoJson(
                row['geometry'],
                style_function=lambda x, color=color_map(row['Number']): {
                    'fillColor': color,
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': 0.7
                },
                tooltip=f"PLZ: {row['PLZ']}, Number: {row['Number']}"
            ).add_to(m)

        # Display the dataframe for Numbers
        # st.subheader('Numbers Data')
        # st.dataframe(gdf_lstat3)

    # Add color map to the map
    color_map.add_to(m)
    
    folium_static(m, width=800, height=600)