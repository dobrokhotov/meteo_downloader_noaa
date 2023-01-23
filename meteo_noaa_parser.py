
import numpy as np
import pandas as pd

def meteo_parser(csv_file, out_file):

    '''
    PARSER FOR NOAA METEO DATA
    csv_file - raw noaa csv file
    out_file - path to output parced file
    format - output file format (csv or xlsx)
    '''

    df_parse = pd.read_csv(csv_file, low_memory=False)
    df = pd.DataFrame()

    # Station WMO ID (USAF) from STATION_LIST
    df['WMO_ID'] = df_parse['STATION']
    # Datetime in UTC
    df['DT_UTC'] = pd.to_datetime(df_parse['DATE'], format='%Y-%m-%dT%H:%M:%S')
    # Station latitude
    df['LAT'] = df_parse['LATITUDE']
    # Station lungitude
    df['LONG'] = df_parse['LONGITUDE']
    # Station height above sea level [Meters]
    df['HASL'] = df_parse['ELEVATION']
    # Official station name
    df['ST_NAME'] = df_parse['NAME']
    # Wind direction [Angular Degrees]
    df['WD'] = (df_parse['WND']
                .apply(lambda x: x[0:3])
                .astype('int64')
                .replace(999, np.nan)
                )
    # Wind speed [meters per second]
    df['WS'] = (df_parse['WND']
                .apply(lambda x: x[8:12])
                .astype('int64')
                .replace(9999, np.nan)
                .apply(lambda x: x / 10)
                )
    # The height above ground level (AGL) of the lowest cloud or obscuring phenomena layer aloft with 5/8 or
    # more summation total sky cover, which may be predominantly opaque, or the vertical visibility into
    # a surface-based obstruction [Meters]
    df['CLOUD_VIS'] = (df_parse['CIG']
                       .apply(lambda x: x[0:5])
                       .astype('int64')
                       .replace(99999, np.nan)
                       .replace(22000, np.nan)
                       )
    # Visibility [Meters]
    df['VIS'] = (df_parse['VIS']
                 .apply(lambda x: x[0:6])
                 .astype('int64')
                 .replace(999999, np.nan)
                 )
    # AIR TEMPERATURE [Degrees Celsius]
    df['TA'] = (df_parse['TMP']
                .apply(lambda x: x[0:5])
                .astype('int64')
                .replace(9999, np.nan)
                .apply(lambda x: x / 10)
                )
    # Dew Point temperature The temperature to which a given parcel of air must be cooled at constant pressure and water
    # vapor content in order for saturation to occur. [Degrees Celsius]
    df['DEW'] = (df_parse['DEW']
                 .apply(lambda x: x[0:5])
                 .astype('int64')
                 .replace(9999, np.nan)
                 .apply(lambda x: x / 10)
                 )
    # The air pressure relative to Mean Sea Level [Hectopascals]
    df['SLP'] = (df_parse['SLP']
                 .apply(lambda x: x[0:5])
                 .astype('int64')
                 .replace(99999, np.nan)
                 .apply(lambda x: x / 10)
                 )

    # There are additional data further in the program so they are implemented through try except

    # The quantity of time over which the LIQUID-PRECIPITATION was measured [Hours]
    try:
        df['PR_PERIOD'] = (df_parse['AA1']
                           .fillna('99')
                           .apply(lambda x: x[0:2])
                           .astype('int64')
                           .replace(99, np.nan)
                           )
    except Exception as e:
        print('Not Found', e)

    # The depth of LIQUID-PRECIPITATION that is measured at the time of an observation.
    try:
        df['PR'] = (df_parse['AA1']
                    .fillna('---9999')
                    .apply(lambda x: x[3:7])
                    .astype('int64')
                    .replace(9999, np.nan)
                    .apply(lambda x: x / 10)
                    )
    except Exception as e:
        print('Not Found', e)

    # The depth of snow and ice on the ground [centimeters]
    try:
        df['SNOW_DEPTH'] = (df_parse['AJ1']
                            .fillna('9999')
                            .apply(lambda x: x[0:4])
                            .astype('int64')
                            .replace(9999, np.nan)
                            )
    except Exception as e:
        print('Not Found', e)

    # The depth of the liquid content of solid precipitation that has accumulated on the ground [millimeters]
    try:
        df['SNOW_LIQ_EQ'] = (df_parse['AJ1']
                             .fillna('---------999999')
                             .apply(lambda x: x[9:15])
                             .astype('int64')
                             .replace(999999, np.nan)
                             .apply(lambda x: x / 10)
                             )
    except Exception as e:
        print('Not Found', e)

    # The quantity of time over which the SNOW-ACCUMULATION occurred.
    try:
        df['SNOW_ACCUM_TIME'] = (df_parse['AL1']
                                 .fillna('99')
                                 .apply(lambda x: x[0:2])
                                 .astype('int64')
                                 .replace(99, np.nan)
                                 )
    except Exception as e:
        print('Not Found', e)

    # The depth of a SNOW-ACCUMULATION [centimeters]
    try:
        df['SNOW_ACCUM'] = (df_parse['AL1']
                            .fillna('---999')
                            .apply(lambda x: x[3:6])
                            .astype('int64')
                            .replace(999, np.nan)
                            )
    except Exception as e:
        print('Not Found', e)

    # The code that denotes the fraction of the total celestial dome covered by a SKY-COVER-LAYER [- partial of 1]
    try:
        df['CLOUD_COVER'] = (df_parse['GA1']
                             .fillna('99')
                             .apply(lambda x: x[0:2])
                             .astype('int64')
                             .replace([99, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                                      [np.nan, 0.1, 2.5, 0.4, 0.5, 0.6, 0.75, 0.9, 1, np.nan, np.nan])
                             )
    except Exception as e:
        print('Not Found', e)

    # The height relative to a VERTICAL-REFERENCE-DATUM of the lowest surface of a cloud [Meters]
    try:
        df['CLOUD_HEIGHT'] = (df_parse['GA1']
                              .fillna('-------99999')
                              .apply(lambda x: x[7:11])
                              .astype('int64')
                              .replace(99999, np.nan)
                              )
    except Exception as e:
        print('Error: Not Found', e)

    # Classification of the clouds that comprise a SKY-COVER-LAYER.
    # 00 = Cirrus (Ci); 01 = Cirrocumulus (Cc); 02 = Cirrostratus (Cs); 03 = Altocumulus (Ac); 04 = Altostratus (As);
    # 05 = Nimbostratus (Ns); 06 = Stratocumulus (Sc); 07 = Stratus (St); 08 = Cumulus (Cu); 09 = Cumulonimbus (Cb);
    # 10 = Cloud not visible owing to darkness, fog, duststorm, sandstorm, or other analogous phenonomena/sky obcured;
    # 11 = Not used; 12 = Towering Cumulus (Tcu); 13 = Stratus fractus (Stfra); 14 = Stratocumulus Lenticular (Scsl);
    # 15 = Cumulus Fractus (Cufra); 16 = Cumulonimbus Mammatus (Cbmam); 17 = Altocumulus Lenticular (Acsl);
    # 18 = Altocumulus Castellanus (Accas); 19 = Altocumulus Mammatus (Acmam); 20 = Cirrocumulus Lenticular (Ccsl);
    # 21 = Cirrus and/or Cirrocumulus; 22 = jenkins-content-114Stratus and/or Fracto-stratus;
    # 23 = Cumulus and/or Fracto-cumulus
    try:
        df['CLOUD_SUBTYPE'] = (df_parse['GA1']
                               .fillna('--------------99')
                               .apply(lambda x: x[14:16])
                               .astype('int64')
                               .replace(
            [99, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
            [np.nan, 'Ci', 'Cc', 'Cs', 'Ac', 'As', 'Ns', 'Sc', 'St', 'Cu', 'Cb', 'Fog', np.nan, 'Tcu', 'Stfra',
             'Scsl', 'Cufra', 'Cbmam', 'Acsl', 'Accas', 'Acmam', 'Ccsl', 'Ci+Cc', 'St+Stfra', 'Cu+Cufra'])
                               )
    except Exception as e:
        print('Error: Not Found', e)

    # Classification of the clouds that comprise a SKY-COVER-LAYER.
    # 00 = Cirrus (Ci); 01 = Cirrocumulus (Cc); 02 = Cirrostratus (Cs); 03 = Altocumulus (Ac); 04 = Altostratus (As);
    # 05 = Nimbostratus (Ns); 06 = Stratocumulus (Sc); 07 = Stratus (St); 08 = Cumulus (Cu); 09 = Cumulonimbus (Cb);
    # 10 = Cloud not visible owing to darkness, fog, duststorm, sandstorm, or other analogous phenonomena/sky obcured;
    # 11 = Not used; 12 = Towering Cumulus (Cu); 13 = Stratus fractus (St); 14 = Stratocumulus Lenticular (Sc);
    # 15 = Cumulus Fractus (Cu); 16 = Cumulonimbus Mammatus (Cb); 17 = Altocumulus Lenticular (Ac);
    # 18 = Altocumulus Castellanus (Ac); 19 = Altocumulus Mammatus (Ac); 20 = Cirrocumulus Lenticular (Cc);
    # 21 = Cirrus and/or Cirrocumulus (Ci); 22 = jenkins-content-114Stratus and/or Fracto-stratus (St);
    # 23 = Cumulus and/or Fracto-cumulus (Cu)
    try:
        df['CLOUD_TYPE'] = (df_parse['GA1']
                            .fillna('--------------99')
                            .apply(lambda x: x[14:16])
                            .astype('int64')
                            .replace(
            [99, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23],
            [np.nan, 'Ci', 'Cc', 'Cs', 'Ac', 'As', 'Ns', 'Sc', 'St', 'Cu', 'Cb', 'Fog', np.nan, 'Cu', 'St',
             'Sc', 'Cu', 'Cb', 'Ac', 'Ac', 'Ac', 'Cc', 'Ci', 'St', 'Cu'])
                            )
    except Exception as e:
        print('Error: Not Found', e)

    # The code that denotes the fraction of the total celestial dome covered by a SKY-COVER-LAYER [- partial of 1]
    try:
        df['CLOUD_COVER_2'] = (df_parse['GF1']
                               .fillna('99')
                               .apply(lambda x: x[0:2])
                               .astype('int64')
                               .replace([99, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
                                        [np.nan, 0.1, 2.5, 0.4, 0.5, 0.6, 0.75, 0.9, 1, np.nan, np.nan, np.nan, np.nan,
                                         np.nan, np.nan,
                                         np.nan, np.nan, np.nan, np.nan, np.nan])
                               )
    except Exception as e:
        print('Not Found', e)

    # The code that represents the fraction of the celestial dome covered by all low clouds present. If
    # no low clouds are present; the code denotes the fraction covered by all middle level clouds present.
    try:
        df['CLOUD_COVER_LOW_OR_MIDDLE'] = (df_parse['GF1']
                                           .fillna('--------99')
                                           .apply(lambda x: x[8:10])
                                           .astype('int64')
                                           .replace(
            [99, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            [np.nan, 0.1, 2.5, 0.4, 0.5, 0.6, 0.75, 0.9, 1, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,
             np.nan, np.nan, np.nan, np.nan, np.nan])
                                           )
    except Exception as e:
        print('Not Found', e)

    df.to_csv(out_file)

    return df

