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
final_merge_df = pd.read_csv(os.path.join(path, 'clean_data/merge_all.csv'))
cr_reports = pd.read_excel(os.path.join(path, 'inputs/CR_from_CPD_Annual_Reports_copy.xlsx'))

fname_2 = 'inputs/FOIA_2019_to_2021_Clearance_Rates_Shooting_Homicides.xlsx'
foia_hom = pd.read_excel((os.path.join(path, fname_2)), sheet_name=2)


# exceptional clearances 2019 - 2021
foia_hom['year_clear'] = foia_hom['DATE CLEARED'].dt.year
foia_hom['year'] = foia_hom['INJURY DATE'].dt.year

hom_year_df = pd.DataFrame(
    foia_hom.groupby(['year_clear', 'year', 'CLEARED'])['RD'].count()).reset_index()

clear_year_df = pd.DataFrame(
    foia_hom.groupby(['year_clear', 'CLEARED'])['RD'].count()).reset_index()

except_clear_year = pd.DataFrame(
    foia_hom.groupby(['year_clear', 'CLEARED', 'CLEARED EXCEPTIONALLY'])
    ['RD'].count()).reset_index()


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


# cases that remain open as of April 2022
def merge_data(df_1, df_2):
    merged_df = pd.merge(df_1, df_2, how="inner", on=['year', 'sex', 'race'])
    return merged_df


clear_interm = pd.DataFrame(all_cleared_df.groupby(['year', 'sex', 'race'])
                            ['case_number'].count()).reset_index()
clear_interm = clear_interm.rename(columns={'case_number': 'num_cleared'})

merged_df = merge_data(sex_grouped, clear_interm)
merged_df['open'] = merged_df.num_occur - merged_df.num_cleared
merged_df['perc_unsolved'] = merged_df.open/merged_df.num_occur
