#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exploration and formatting for Static Plots
@author: polinarozhkova
"""
import pandas as pd
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

path = r'/Users/polinarozhkova/Desktop/GitHub/cr_eda_chicago/'
final_merge_df = pd.read_csv(os.path.join(path, 'clean_data/merge_all.csv'))
cr_reports = pd.read_excel(os.path.join(path, 'inputs/CR_from_CPD_Annual_Reports_copy.xlsx'))


all_cleared_df = final_merge_df[final_merge_df['cleared'] == 'Y']
cr_reports = cr_reports.fillna(np.isnan())

# plot 1
final_merge = final_merge_df[final_merge_df['year'] > 2000]
yr_month_map = pd.DataFrame(final_merge.groupby(['year', 'month'])
                            ['case_number'].count()).reset_index()
yr_month_map = yr_month_map.rename(
    columns={'case_number': 'homicides'}).pivot('year', 'month', 'homicides')

fig, ax = plt.subplots(figsize=(10, 10))
sns.heatmap(yr_month_map, cmap='RdYlGn_r',
            cbar_kws={'label': 'Count'})
ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=10)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontsize=10)
ax.set_xlabel('Month')
ax.set_ylabel('Year')
plt.title('Homicide Count in Chicago 2001 - 2021', fontdict={'fontsize': 12}, pad=14)
plt.savefig(os.path.join(path, 'plots/static_plot_1.eps'), format='eps', dpi=1000)

# plot 2
# number of homicides in data and number of homicides in the CPD annual reports don't always match
# this may be because clearance rates are calculated using # of incidents rather than # of victims


def line_subplots(df, col_1, col_2, col_3, t_1, t_2, t_3):
    plt.rcParams.update({'font.size': 9})
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.set_style("darkgrid")
    ax.plot(df.year, col_1, label=t_1, color='gold')
    ax.plot(df.year, col_2, label=t_2, color='lightcoral')
    ax.plot(df.year, col_3, label=t_3, color='cornflowerblue')
    ax.legend(loc='best')
    ax.set_xlabel('Year')
    ax.set_ylabel('Count')
    ax.set_xticks(range(2001, 2022))
    ax.set_title('Trends in Homicide and Clearance Counts 2001-2021', fontsize=15)
    return


line_subplots(cr_reports, cr_reports.homicide_count, cr_reports.total_cleared,
              cr_reports.firearm, 'Homicide', 'Cleared', 'Firearm')
plt.savefig(os.path.join(path, 'plots/static_plot_2.eps'), format='eps', dpi=1000)


# Sources:
# For heatmap: https://seaborn.pydata.org/generated/seaborn.heatmap.html;
# https://regenerativetoday.com/time-series-data-visualization-in-python/
# For annotations:
# https://jessica-miles.medium.com/adding-annotations-to-visualizations-using-matplotlib-279e9c770baa
# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.axvline.html
