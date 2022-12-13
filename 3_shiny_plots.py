#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data and Programming II - Final Project
Shiny Plots
@author: polinarozhkova
"""
from shiny import App, render, ui, reactive
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import geopandas
import os

path = r'/Users/polinarozhkova/Desktop/GitHub/final-project-homicide-cr-and-cpd-complaints/'
district_shp = os.path.join(path, 'PoliceDistrict', 'PoliceDistrict.shp')

df_district = geopandas.read_file(district_shp)
df_district['DIST_NUM'] = df_district['DIST_NUM'].astype(float)

beat_shp = os.path.join(path, 'Boundaries - Police Beats (current)',
                        'geo_export_7f053540-59bf-4d25-b453-b6f10b77c115.shp')
beat_df = geopandas.read_file(beat_shp)
beat_df['beat_num'] = beat_df['beat_num'].astype(float)

# Additional data: Homicides, Clearance Rates, Racial Demographics
final_merge_df = pd.read_csv(os.path.join(path, 'clean_data/merge_all.csv'))
cr_reports = pd.read_excel(os.path.join(path, 'inputs/CR_from_CPD_Annual_Reports_copy.xlsx'))
beats_race = pd.read_csv(os.path.join(path, 'inputs/beat_estimates.csv'))

# Homicides 2021
hom_2021 = final_merge_df[final_merge_df['year'] == 2021]
hom_2021 = hom_2021.rename(columns={'ward_x': 'ward', 'case_number': 'homicide_count',
                                    'district': 'DIST_NUM'})

# Homicides by district
hom_district = hom_2021.groupby(['DIST_NUM'])['homicide_count'].count().reset_index()
df_district = df_district.merge(hom_district, on=['DIST_NUM'])
df_district = df_district.to_crs('EPSG:3435')

# Homicides by beat
hom_beat = hom_2021.groupby(['beat'])['homicide_count'].count().reset_index()
hom_beat = hom_beat.rename(columns={'beat': 'beat_num', 'case_number': 'homicide_count'})

# Racial Demographics by Beat
race_2021 = beats_race[beats_race['year'] == 2021].drop(
    columns='Unnamed: 0').reset_index(drop=True)
race_2021['perc_white'] = round((race_2021.white_nothisp/race_2021.tot_pop)*100, 2)
race_2021['perc_black'] = round((race_2021.black_nothisp/race_2021.tot_pop)*100, 2)
race_2021['perc_hisp'] = round((race_2021.tot_hisp/race_2021.tot_pop)*100, 2)
hom_race_merge = pd.merge(hom_beat, race_2021, how="inner", on=['beat_num'])
beat_df = beat_df.merge(hom_race_merge, on=['beat_num'])
beat_df = beat_df.to_crs('EPSG:3435')


# Shiny Plot Options
df_choices = ['Black Pop. as Percentage of Total Population',
              'Hispanic Pop. as Percentage of Total Population',
              'White Pop. as Percentage of Total Population']

# second plot df
injury_df = pd.DataFrame(final_merge_df.groupby(['year', 'injury_type', 'cleared'])
                         ['case_number'].count()).reset_index()

app_ui = ui.page_fluid(
    ui.row(ui.column(4, ui.input_select(id='dataset',
                                        label="Select dataset:",
                                        choices=df_choices)), offset=8, align='left'),
    ui.row(ui.column(4, ui.output_plot(id='race_plot', width='500px', height='500px')),
           ui.column(4, ui.output_plot(id='hom_plot', width='500px', height='500px')),
           offset=12, align='right'),
    ui.input_select(id="st",
                    label="Choose year: ",
                    choices=list(injury_df['year'])),
    ui.output_plot(id='injury_plot', width='500px', height='500px'))


def server(input, output, session):
    fig, ax = plt.subplots(figsize=(8, 8))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='3%', pad=0.01, alpha=1)
    ax.axis('off')

    @reactive.Calc
    def get_data():
        df_dict = {'Black Pop. as Percentage of Total Population': beat_df['perc_black'],
                   'Hispanic Pop. as Percentage of Total Population': beat_df['perc_hisp'],
                   'White Pop. as Percentage of Total Population': beat_df['perc_white']}
        return df_dict[input.dataset()]

    @output
    @render.plot
    def race_plot():
        beat_df.plot(ax=ax, alpha=1, edgecolor='white', label='Chicago Wards', aspect=1,
                     column=get_data(), legend=True, cax=cax, cmap='Blues')
        ax.set_title('Racial Demographics (% of total pop.)')
        return fig

    @output
    @render.plot
    def hom_plot():
        df_district.plot(ax=ax, alpha=1, edgecolor='white', aspect=1,
                         column=df_district['homicide_count'], legend=True,
                         cax=cax, cmap='Purples')
        ax.set_title('Homicides in Chicago 2021 by Police District')
        return fig

    @reactive.Calc
    def injury_year():
        df = injury_df
        return df[df['year'] == input.st()]

    @output
    @render.plot
    def injury_plot():
        df = injury_df
        sns.set()
        ax = sns.barplot(data=df, x='injury_type', y='case_number', hue='cleared')
        ax.set_xlabel('Injury')
        ax.tick_params(axis='x', rotation=45)
        ax.set_ylabel('Count')
        ax.set_title(f'Homicide Injuries in {input.st()}')
        return ax


app = App(app_ui, server)


# Sources:
# EXTRACT FIRST N CHARACTERS FROM LEFT OF COLUMN
# https://www.datasciencemadesimple.com/return-first-n-character-from-left-of-column-in-pandas-python/
# reused sections of homework 4
