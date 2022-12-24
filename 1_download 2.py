#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Retrieval, cleaning and preparation
@author: polinarozhkova
"""
from sodapy import Socrata
import pandas as pd
import os

path = r'/Users/polinarozhkova/Desktop/GitHub/cr_eda_chicago/'
client = Socrata("data.cityofchicago.org/", None)

results = client.get_all('ijzp-q8t2', primary_type='HOMICIDE', limit=11669)
results_2 = client.get_all('gumc-mgzr', victimization_primary='HOMICIDE', limit=11550)
cdp_hom = pd.DataFrame.from_records(results)
cdp_hom.to_csv('inputs/chicago_data_portal_all.csv', index=False)
cdp_victims = pd.DataFrame.from_records(results_2)
cdp_victims.to_csv('inputs/victim_data.csv', index=False)

# homicides 2001-2019 with clearance status
fname_1 = 'inputs/Trace_Homicides_and_Shootings_2001_2019.xlsx'
fname_2 = 'inputs/FOIA_2019_to_2021_Clearance_Rates_Shooting_Homicides.xlsx'
fname_3 = 'inputs/chicago_data_portal_all.csv'
fname_4 = 'inputs/victim_data.csv'

trace_hom = pd.read_excel((os.path.join(path, fname_1)), sheet_name=1)
foia_hom = pd.read_excel((os.path.join(path, fname_2)), sheet_name=2)
cdp_hom = pd.read_csv(os.path.join(path, fname_3))
cdp_victims = pd.read_csv(os.path.join(path, fname_4))


# Cleaning and Preparation
def load_foia_hom(df):
    df_clean = df.rename(columns={'RD': 'case_number', 'HOMICIDE ID': 'id',
                                  'INJURY DATE': 'date', 'INJURY DESCRIPTION': 'injury_type',
                                  'DATE CLEARED': 'date_clear'})
    df_clean.columns = df_clean.columns.str.lower()
    df_clean = df_clean.drop(columns='cleared exceptionally')
    df_clean = df_clean[(df_clean['date'].dt.year >= 2001) & (df_clean['date'].dt.year < 2022)]
    df_clean['time_to_clear'] = (df_clean['date_clear'] - df_clean['date']).dt.days
    return df_clean


def load_trace_hom(df):
    df_clean = df.rename(columns={'RD': 'case_number', 'Injury Type': 'injury_type',
                                  'Cleared?2': 'cleared', 'Date Cleared': 'date_clear'})
    df_clean.columns = df_clean.columns.str.lower()
    df_clean = df_clean.dropna(subset=['id'])
    df_clean = df_clean[['case_number', 'id', 'date', 'injury_type', 'cleared', 'date_clear',
                         'beat', 'district']]
    df_clean['time_to_clear'] = (df_clean['date_clear'] - df_clean['date']).dt.days
    return df_clean


def prep_portal_df(df):
    df_new = df[['case_number', 'unique_id', 'date_x', 'block_x', 'primary_type',
                 'iucr', 'age', 'sex', 'race', 'month', 'day_of_week', 'hour',
                 'location_description_y', 'latitude_y', 'longitude_y', 'location_x', 'arrest',
                 'domestic', 'gunshot_injury_i', 'ward_x', 'community_area_x',
                 'street_outreach_organization', 'homicide_victim_first_name',
                 'homicide_victim_last_name']]
    df_new['date_x'] = df_new['date_x'].apply(pd.to_datetime)
    df_new['year'] = df_new['date_x'].dt.year
    df_new = df_new[(df_new['year'] >= 2001) &
                    (df_new['year'] < 2022)].drop_duplicates(subset=['unique_id'])
    return df_new


def merge_data(df_1, df_2):
    merged_df = pd.merge(df_1, df_2, how="inner", on=['case_number'])
    return merged_df


foia_df_clean = load_foia_hom(foia_hom)
trace_df_clean = load_trace_hom(trace_hom)
cdp_data = prep_portal_df(merge_data(cdp_victims, cdp_hom))

# In order to prevent repeated observations, only keep observation in Trace data if it
# doesn't reappear in the FOIA-ed dataset.
# Sources: for "NOT IN": ~something.isin(somewhere)
# https://stackoverflow.com/questions/19960077/how-to-filter-pandas-dataframe-using-in-and-not-in-like-in-sql
case_numbers = foia_df_clean['case_number']
trace_df_clean = trace_df_clean[~trace_df_clean['case_number'].isin(case_numbers)]
hom_clr_df = pd.concat([trace_df_clean, foia_df_clean], ignore_index=True, axis=0)


# merge chicago data portal data and downloaded data
merge_final = merge_data(cdp_data, hom_clr_df).drop_duplicates(subset=['unique_id'])
merge_final['year_cleared'] = merge_final['date_clear'].dt.year


hom_clr_df.to_csv(os.path.join(path, 'clean_data/hom_clearance.csv'), index=False)
cdp_data.to_csv(os.path.join(path, 'clean_data/city_portal_hom.csv'), index=False)
merge_final.to_csv(os.path.join(path, 'clean_data/merge_all.csv'), index=False)
