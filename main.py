
import os
currentWorkingDirectory = os.getcwd()
#currentWorkingDirectory = "/mount/src/berlingeoheatmap1/"

# -----------------------------------------------------------------------------

os.chdir(currentWorkingDirectory)
print("Current working directory\n" + os.getcwd())

import pandas                        as pd
from core import methods             as m1
from core import HelperTools         as ht

from config                          import pdict

# -----------------------------------------------------------------------------
@ht.timer
def main():
    """Generation of Streamlit App for visualizing electric charging stations & residents in Berlin
    
    The function performs the following steps:
    
    1. Load geospatial data for postal codes and districts in Berlin from CSV files.
    2. Load electric charging station data, preprocess it, and merge it with geospatial data.
    3. Count the number of charging stations in each postal code and district.
    4. Load resident data and preprocess it similarly, merging with geospatial data.
    5. Generate a Streamlit-based visualization that maps electric charging stations alongside 
       resident distribution.
    """

    # Load geospatial data for postal codes and districts

    df_geodat_plz = pd.read_csv(pdict["file_geodat_plz"], sep=';')
    df_geodat_dis = pd.read_csv(pdict["file_geodat_dis"], sep=';')


    # Load and preprocess electric charging station data

    df_lstat = pd.read_csv(pdict["file_lstations"], sep=';', skiprows=10)
    df_lstat.columns = df_lstat.columns.str.strip()
    # print(df_lstat.columns)
    # print(df_lstat.head())

    gdf_lstat2 = m1.preprop_lstat(df_lstat, df_geodat_plz, pdict)
    gdf_lstat3 = m1.count_plz_occurrences(gdf_lstat2)


    # Load and preprocess resident data

    df_residents = pd.read_csv(pdict["file_residents"], sep=',')
    # print(df_residents.columns)
    gdf_residents2 = m1.preprop_resid(df_residents, df_geodat_plz, pdict)

    # Generate the Streamlit visualization
    m1.make_streamlit_electric_Charging_resid(gdf_lstat3, gdf_residents2)

    
# -----------------------------------------------------------------------------------------------------------------------

    #


if __name__ == "__main__": 
    main()