#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 12:45:15 2020

@author: Jin Ning Huang
CSE 163 SUMMER 2020

This file contains for entire Task 4.

NOTE: I am using local file, so please change the desirable filepath for your
computer.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


def income_stat(burden_data):
    '''
    Takes the given data and will show the regression plot of income
    Will save the plot figure in png format
    '''
    # filtering to get rid of NA
    burden_data = burden_data[burden_data['INCOME'].notna()]

    # filtering the income level
    income_value = burden_data['INCOME']

    poverty = burden_data[income_value < 20000]
    low_income = burden_data[(income_value >= 20000) & (income_value < 45000)]
    middle_class = burden_data[(income_value >= 45000) &
                               (income_value < 140000)]
    upper_middle = burden_data[(income_value >= 140000) &
                               (income_value < 150000)]
    high_income = burden_data[(income_value >= 150000) &
                              (income_value < 200000)]
    highest_tax = burden_data[(income_value >= 200000)]

    # groupby year for each income level
    poverty_report = poverty.groupby('YEAR')['INCOME'].mean()
    low_income_report = low_income.groupby('YEAR')['INCOME'].mean()
    middle_class_report = middle_class.groupby('YEAR')['INCOME'].mean()
    upper_middle_report = upper_middle.groupby('YEAR')['INCOME'].mean()
    high_income_report = high_income.groupby('YEAR')['INCOME'].mean()
    highest_tax_report = highest_tax.groupby('YEAR')['INCOME'].mean()

    # ploting
    fig, [[ax1, ax2], [ax3, ax4], [ax5, ax6]] = \
        plt.subplots(3, figsize=(12, 10), ncols=2)
    poverty_report.plot(ax=ax1)
    low_income_report.plot(ax=ax2)
    middle_class_report.plot(ax=ax3)
    upper_middle_report.plot(ax=ax4)
    high_income_report.plot(ax=ax5)
    highest_tax_report.plot(ax=ax6)

    # labeling
    ax1.set_title('Poverty Level')
    ax2.set_title('Low Income')
    ax3.set_title('Middle Class')
    ax4.set_title('Upper Middle Class')
    ax5.set_title('High Income')
    ax6.set_title('Highest Tax Brackets')

    plt.tight_layout()
    plt.savefig('income_level_overall.png')


def houseing_cost(burden_data):
    '''
    Takes the given data and create a line plot of the housing cost thrend.
    Will save the plot in png format
    '''
    housing_cost = burden_data.groupby('YEAR')['COSTS'].mean()

    fig, ax = plt.subplots(1)
    housing_cost.plot(ax=ax)
    plt.title('Average Housing Cost per Year')
    plt.savefig('housing_cost.png')


def income_by_race(burden_data):
    '''
    Takes the given data and create bar plots on unique races per income level
    Will save plot figure in png format.
    '''
    # filtering to get rid of NA
    burden_data = burden_data[burden_data['INCOME'].notna()]
    burden_data = burden_data[burden_data['RACE'] != 'All']

    # filtering the income level
    income_value = burden_data['INCOME']

    poverty = burden_data[income_value < 20000]
    low_income = burden_data[(income_value >= 20000) & (income_value < 45000)]
    middle_class = burden_data[(income_value >= 45000) &
                               (income_value < 150000)]
    high_income = burden_data[income_value >= 150000]

    # bar ploting
    sns.catplot(data=poverty, x='YEAR', y='INCOME', hue='RACE', kind='bar',
                height=10, aspect=2, ci=None)
    plt.title('Poverty by Race')
    plt.savefig('poverty_by_race.png')

    sns.catplot(data=low_income, x='YEAR', y='INCOME', hue='RACE', kind='bar',
                height=10, aspect=2, ci=None)
    plt.title('Low Income by Race')
    plt.savefig('low_income_by_race.png')

    sns.catplot(
        data=middle_class, x='YEAR', y='INCOME', hue='RACE', kind='bar',
        height=10, aspect=2, ci=None)
    plt.title('Middle Class by Race')
    plt.savefig('middle_class_by_race.png')

    sns.catplot(data=high_income, x='YEAR', y='INCOME', hue='RACE', kind='bar',
                height=10, aspect=2, ci=None)
    plt.title('High Income by Race')
    plt.savefig('high_income_by_race.png')


def housing_cost_by_race(burden_data):
    '''
    Takes the given data and make bar plot of housing cost for each race
    Will save the map into png format.
    '''
    # filtering
    burden_data = burden_data[burden_data['INCOME'].notna()]
    burden_data = burden_data[burden_data['RACE'] != 'All']

    # ploting
    sns.catplot(data=burden_data, x='YEAR', y='COSTS', hue='RACE', kind='bar',
                height=10, aspect=2, ci=None)
    plt.title('Housing Cost by Race')

    plt.savefig('housing_cost_by_race.png')


def main():
    '''
    Will use the raw data of Housing Burden and turn into a Dataframe.
    This Dataframe will pass down to diffrent functions that is doing it own
    tasks. The main function will be expected to create two plots of line
    charts and two plots of bar charts.
    '''
    burden_data = pd.read_csv(
        '~/Desktop/CSE/CSE 163/project/part 2/Task 4/' +
        'Burden.csv')

    income_stat(burden_data)
    houseing_cost(burden_data)
    income_by_race(burden_data)
    housing_cost_by_race(burden_data)


if __name__ == '__main__':
    main()
