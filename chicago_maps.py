#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: polinarozhkova
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
import geopandas
import os


path = r'/Users/polinarozhkova/Desktop/GitHub/cr_eda_chicago/'


district_shp = os.path.join(path, 'PoliceDistrict', 'PoliceDistrict.shp')
df_district = geopandas.read_file(district_shp)
df_district['DIST_NUM'] = df_district['DIST_NUM'].astype(float)

beat_shp = os.path.join(path, 'Boundaries - Police Beats (current)',
                        'geo_export_7f053540-59bf-4d25-b453-b6f10b77c115.shp')
beat_df = geopandas.read_file(beat_shp)
beat_df['beat_num'] = beat_df['beat_num'].astype(float)
beat_df['district'] = beat_df['district'].astype(float)
beat_df = beat_df.rename(columns={'district': 'DIST_NUM'})

# Additional data: Homicides, Clearance Rates, Racial Demographics
final_merge_df = pd.read_csv(os.path.join(path, 'clean_data/merge_all.csv'))
cr_reports = pd.read_excel(os.path.join(path, 'inputs/CR_from_CPD_Annual_Reports_copy.xlsx'))
beats_race = pd.read_csv(os.path.join(path, 'inputs/beat_estimates.csv'))

# Racial Demographics by Beat
race_2021 = beats_race[beats_race['year'] == 2021].drop(
    columns='Unnamed: 0').reset_index(drop=True)
race_2021['perc_white'] = round((race_2021.white_nothisp/race_2021.tot_pop)*100, 2)
race_2021['perc_black'] = round((race_2021.black_nothisp/race_2021.tot_pop)*100, 2)
race_2021['perc_hisp'] = round((race_2021.tot_hisp/race_2021.tot_pop)*100, 2)
race_2021 = race_2021.rename(columns={'year': 'census_year'})


def clean(df):
    df = df.rename(columns={'ward_x': 'ward', 'beat': 'beat_num', 'district': 'DIST_NUM'})
    df['cleared'] = df['cleared'].map({'Y': 1, 'N': 0})
    df['gunshot_injury'] = final_merge_df['gunshot_injury_i'].map({'YES': True, 'NO': False})
    return df


final_merge_df = clean(final_merge_df)


def map_points(df, df_district):
    df_district = df_district.merge(df, on=['DIST_NUM']).reset_index()
    return df_district


def district_grouped(df, df_cleared, df_district):
    hom_district = df.groupby(['DIST_NUM'])['case_number'].count().reset_index()
    hom_district = hom_district.rename(columns={'case_number': 'homicide_count'})
    clear_district = df.groupby(['DIST_NUM'])['cleared'].sum().reset_index()
    hom_district = hom_district.merge(clear_district, on=['DIST_NUM']).reset_index()
    hom_district['dist_cr'] = hom_district.cleared/hom_district.homicide_count
    df_district = df_district.merge(hom_district)
    df_district = df_district.to_crs('EPSG:4326')
    return df_district


def district_cr(df):
    new_df = df[['DIST_NUM', 'dist_cr']]
    return new_df


def beat_grouped(df, df_cleared, beat_df, new_df):
    hom_beat = df.groupby(['beat_num'])['case_number'].count().reset_index()
    hom_beat = hom_beat.rename(columns={'case_number': 'homicide_count'})
    clear_beat = df.groupby(['beat_num'])['cleared'].sum().reset_index()
    hom_beat = hom_beat.merge(clear_beat, on=['beat_num']).reset_index()
    hom_race_merge = pd.merge(hom_beat, race_2021, how="inner", on=['beat_num'])
    hom_race_merge['beat_cr'] = hom_beat.cleared/hom_beat.homicide_count
    beat_df = beat_df.merge(hom_race_merge, on=['beat_num'])
    beat_df = beat_df.merge(new_df, on=['DIST_NUM'])
    beat_df = beat_df.to_crs('EPSG:4326')
    return beat_df


hom_2019 = final_merge_df[final_merge_df['year'] == 2019]
hom_2020 = final_merge_df[final_merge_df['year'] == 2020]
hom_2021 = final_merge_df[final_merge_df['year'] == 2021]


clear_2019 = final_merge_df[final_merge_df['year_cleared'] == 2019]
clear_2020 = final_merge_df[final_merge_df['year_cleared'] == 2020]
clear_2021 = final_merge_df[final_merge_df['year_cleared'] == 2021]


number_hom_2019 = map_points(hom_2019, df_district)
number_hom_2020 = map_points(hom_2020, df_district)
number_hom_2021 = map_points(hom_2021, df_district)


hom_dist_2019 = district_grouped(hom_2019, clear_2019, df_district)
hom_dist_2020 = district_grouped(hom_2020, clear_2020, df_district)
hom_dist_2021 = district_grouped(hom_2021, clear_2021, df_district)

dist_cr_2019 = district_cr(hom_dist_2019)
dist_cr_2020 = district_cr(hom_dist_2020)
dist_cr_2021 = district_cr(hom_dist_2021)


hom_beat_2019 = beat_grouped(hom_2019, clear_2019, beat_df, dist_cr_2019)
hom_beat_2020 = beat_grouped(hom_2020, clear_2020, beat_df, dist_cr_2020)
hom_beat_2021 = beat_grouped(hom_2021, clear_2021, beat_df, dist_cr_2021)

number_hom_2019 = geopandas.GeoDataFrame(number_hom_2019, geometry=geopandas.points_from_xy(
    number_hom_2019.longitude_y, number_hom_2019.latitude_y))

number_hom_2020 = geopandas.GeoDataFrame(number_hom_2020, geometry=geopandas.points_from_xy(
    number_hom_2020.longitude_y, number_hom_2020.latitude_y))

number_hom_2021 = geopandas.GeoDataFrame(number_hom_2021, geometry=geopandas.points_from_xy(
    number_hom_2021.longitude_y, number_hom_2021.latitude_y))


fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(25, 25))
sns.set_style("dark")
ax1, ax2, ax3 = axes.flatten()

divider = make_axes_locatable(ax1)
cax = divider.append_axes('right', size='3%', pad=0.1, label='test')
hom_dist_2019.plot(ax=ax1, column='dist_cr',  missing_kwds={'color': 'lightgrey'},
                   legend=True, cax=cax, cmap='Blues', legend_kwds={'format': '%.2f%%'})
# ax1 = hom_beat_2019.plot(ax=ax1, legend=True, cax=cax, alpha=0.2)
hom_beat_2019.plot(ax=ax1, column='dist_cr', legend=True, cax=cax, cmap='Blues')
number_hom_2019.plot(ax=ax1, column='race', cmap='RdYlGn', legend=True, markersize=5)
ax1.axis('off')


divider = make_axes_locatable(ax2)
cax = divider.append_axes('right', size='3%', pad=0.1)
ax2 = hom_dist_2020.plot(ax=ax2, column='dist_cr',  missing_kwds={'color': 'lightgrey'},
                         legend=True, cax=cax, cmap='Blues', legend_kwds={'format': '%.2f%%'})
# ax2 = hom_beat_2020.plot(ax=ax2, legend=True, cax=cax, alpha=0)
ax2 = hom_beat_2020.plot(ax=ax2, column='dist_cr', legend=True, cax=cax, cmap='Blues')
number_hom_2020.plot(ax=ax2, column='race', cmap='RdYlGn', legend=True, markersize=5)
ax2.axis('off')

divider = make_axes_locatable(ax3)
cax = divider.append_axes('right', size='3%', pad=0.1)
ax3 = hom_dist_2021.plot(ax=ax3, column='dist_cr',  missing_kwds={'color': 'lightgrey'},
                         legend=True, cax=cax, cmap='Blues', legend_kwds={'format': '%.2f%%'})
# ax3 = hom_beat_2021.plot(ax=ax3, legend=True, cax=cax, alpha=0)
ax3 = hom_beat_2021.plot(ax=ax3, column='dist_cr', legend=True, cax=cax, cmap='Blues')
number_hom_2021.plot(ax=ax3, column='race', cmap='RdYlGn', legend=True, markersize=5)
ax3.axis('off')

ax1.set_title('Homicide and Clearance Rate by District 2019')
ax2.set_title('Homicide and Clearance Rate by District 2020')
ax3.set_title('Homicide and Clearance Rate by District 2021')
plt.savefig(os.path.join(path, 'plots/homicide_clr_map.eps'), format='eps', dpi=1000)
