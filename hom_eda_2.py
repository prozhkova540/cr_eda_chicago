#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  1 15:31:30 2023

@author: polinarozhkova
"""
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

path = r'/Users/polinarozhkova/Desktop/GitHub/cr_eda_chicago/'
fname = 'inputs/FOIA_2019_to_2021_Clearance_Rates_Shooting_Homicides.xlsx'
foia_hom = pd.read_excel((os.path.join(path, fname)), sheet_name=2)
final_merge_df = pd.read_csv(os.path.join(path, 'clean_data/merge_all.csv'))
cr_reports = pd.read_excel(os.path.join(path, 'inputs/CR_from_CPD_Annual_Reports_copy.xlsx'))


def load_foia_hom(df):
    df_clean = df.rename(columns={'RD': 'case_number', 'HOMICIDE ID': 'id',
                                  'INJURY DATE': 'date', 'INJURY DESCRIPTION': 'injury_type',
                                  'DATE CLEARED': 'date_clear'})
    df_clean.columns = df_clean.columns.str.lower()
    df_clean = df_clean[df_clean['date'].dt.year < 2022]
    df_clean['time_to_clear'] = df_clean['date_clear'] - df_clean['date']
    return df_clean


def formal_clearance(df):
    df_new = df_clean[(df_clean['date'].dt.year >= 2001) & (df_clean['date'].dt.year < 2022)]
    df_clean['time_to_clear'] = df_clean['date_clear'] - df_clean['date']
    return df_clean


foia_df = load_foia_hom(foia_hom)

# exceptional clearances 2019 - 2021
hom_year_df = pd.DataFrame(
    foia_df.groupby(['year_clear', 'year', 'CLEARED'])['RD'].count()).reset_index()

clear_year_df = pd.DataFrame(
    foia_hom.groupby(['year_clear', 'CLEARED'])['RD'].count()).reset_index()

except_clear_year = pd.DataFrame(
    foia_hom.groupby(['year_clear', 'CLEARED', 'CLEARED EXCEPTIONALLY'])
    ['RD'].count()).reset_index()

# Cases and their clearance status
# This dataset does not include incidents that counted towards clearance rates prior to 2019
all_cleared_df = final_merge_df[final_merge_df['cleared'] == 'Y']


# race by yr
race_grouped = pd.DataFrame(final_merge_df.groupby(['year', 'race'])
                            ['case_number'].count()).reset_index()
race_grouped


# race and sex by year
sex_grouped = pd.DataFrame(final_merge_df.groupby(['year', 'sex', 'race'])
                           ['case_number'].count()).reset_index()
sex_grouped
sex_grouped = sex_grouped.rename(columns={'case_number': 'num_occur'})


# race cleared by year -- incidents occurring between 2001 and 2021
race_cleared_grouped = pd.DataFrame(all_cleared_df.groupby(['year_cleared', 'year', 'race'])
                                    ['case_number'].count()).reset_index()
race_cleared_grouped


sex_cleared_grouped = pd.DataFrame(all_cleared_df.groupby(['year_cleared', 'year', 'sex', 'race'])
                                   ['case_number'].count()).reset_index()
sex_cleared_grouped
