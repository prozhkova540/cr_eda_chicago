#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exploration and formatting for Static Plots
@author: polinarozhkova
"""
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

path = r'/Users/polinarozhkova/Desktop/GitHub/cr_eda_chicago/'
final_merge_df = pd.read_csv(os.path.join(path, 'clean_data/merge_all.csv'))
cr_reports = pd.read_excel(os.path.join(path, 'inputs/CR_from_CPD_Annual_Reports_copy.xlsx'))

# plot 1
yr_month_map = pd.DataFrame(final_merge_df.groupby(['year', 'month'])
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
# I use the annual reports for CPD's "formal" clearance rate but rely on the data for hom counts
# The following graph displays how many cases remain open for each year as of april 2022
# The graph does not show how many cases were cleared each year

all_cleared_df = final_merge_df[final_merge_df['cleared'] == 'Y']

# all homicides and clearances
total_hom_yr = pd.DataFrame(final_merge_df.groupby(['year'])['case_number'].count()).reset_index()
clr_yr = pd.DataFrame(all_cleared_df.groupby(['year'])['case_number'].count()).reset_index()
total_commit_cleared = pd.merge(clr_yr, total_hom_yr, on=['year']).rename(
    columns={'case_number_y': 'hom_total', 'case_number_x': 'clear_total'})


# firearm homicides and firearm clearances
firearm = pd.DataFrame(final_merge_df.groupby(['year'])['gunshot_injury_i'].
                       apply(lambda x: (x == 'YES').sum())).reset_index()
firearm_clr = pd.DataFrame(all_cleared_df.groupby(['year'])['gunshot_injury_i'].
                           apply(lambda x: (x == 'YES').sum())).reset_index()
total_firearm = pd.merge(firearm, firearm_clr, on=['year']).rename(
    columns={'gunshot_injury_i_x': 'firearm_total', 'gunshot_injury_i_y': 'firearm_clear'})


dv = pd.DataFrame(final_merge_df.groupby(['year'])['domestic'].
                  apply(lambda x: (x == True).sum())).reset_index()
dv_clr = pd.DataFrame(all_cleared_df.groupby(['year'])['domestic'].
                      apply(lambda x: (x == True).sum())).reset_index()
total_dv = pd.merge(dv, dv_clr, on=['year']).rename(
    columns={'domestic_x': 'dv_total', 'domestic_y': 'dv_clear'})


total_commit_cleared = pd.melt(total_commit_cleared, id_vars=['year'],
                               value_vars=['hom_total', 'clear_total'],
                               var_name='case_status', value_name='Count')
total_firearm = pd.melt(total_firearm, id_vars=['year'],
                        value_vars=['firearm_total', 'firearm_clear'],
                        var_name='case_status', value_name='Count')
total_dv = pd.melt(total_dv, id_vars=['year'], value_vars=['dv_total', 'dv_clear'],
                   var_name='case_status', value_name='Count')


def line_subplots(df, ax_n):
    plt.rcParams.update({'font.size': 9})
    sns.set_style("darkgrid")
    sns.lineplot(data=df, x='year', y='Count',
                 hue='case_status', ax=ax_n, linewidth=0.75, palette=['#34495e', '#3498db'])
    ax_n.legend(loc='best')
    ax_n.set_xlabel('Year')
    ax_n.set_ylabel('Count')
    ax_n.set_xticks(range(2001, 2022))
    return


def plot_annotate(ax_n, y1, y2, y3):
    style = dict(size=10, color='red', alpha=0.75)
    ax_n.axvline(2001, linestyle='dashed', color='red', alpha=0.25)
    ax_n.axvline(2008, linestyle='dashed', color='red', alpha=0.25)
    ax_n.axvline(2020, linestyle='dashed', color='red', alpha=0.25)
    ax_n.text(2001, y1, '  9/11 Attack', ha='left',  **style)
    ax_n.text(2008, y2, 'Financial Crisis Starts  ', ha='right',  **style)
    ax_n.text(2020, y3, 'Covid-19 Lockdown  ', ha='right',  **style)
    return


fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(12, 15))
ax1, ax2, ax3 = axes.flatten()
line_subplots(total_commit_cleared, ax1)
line_subplots(total_firearm, ax2)
line_subplots(total_dv, ax3)
plot_annotate(ax1, 750, 650, 750)
plot_annotate(ax2, 700, 600, 700)
plot_annotate(ax3, 56, 52, 56)
ax1.set_title('Total Homicides')
ax2.set_title('Homicides Involving Firearms')
ax3.set_title('Domestic Violence Homicides')
plt.savefig(os.path.join(path, 'plots/static_plot_2.png'))

# Sources:
# For heatmap: https://seaborn.pydata.org/generated/seaborn.heatmap.html;
# https://regenerativetoday.com/time-series-data-visualization-in-python/
# For annotations:
# https://jessica-miles.medium.com/adding-annotations-to-visualizations-using-matplotlib-279e9c770baa
# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.axvline.html
