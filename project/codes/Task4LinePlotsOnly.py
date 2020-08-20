#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 17:30:34 2020

@author: Jin Ning Huang
CSE 163 SUMMER 2020

This file contains the extension from Task 4. This one will function
similarity as "income_by_race" and "housing_cost_by_race" expect this script
will make lines.

NOTE: I am using local file, so please change the desirable filepath for your
computer.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()


def percentage_missing_data(df):
    '''
    Takes the giving Dataframe format and will count rows that contain NA
    values on the INCOME column. Then do the percentage calculation of the
    missing data and will print the float value.
    '''
    count_na = df['INCOME'].isna().sum()
    result = count_na / len(df) * 100

    return round(result, 2)


def income_line_plots(df):
    '''
    Will takes the given Dataframe format and filtering them into four
    different Dataframe for each of the income level. Then each of income
    level would be ploted into a line chart with race category. All of line
    plots will be save in png format.
    '''
    # filtering the income level
    income_value = df['INCOME']

    poverty = df[income_value < 20000]
    low_income = df[(income_value >= 20000) & (income_value < 45000)]
    middle_class = df[(
        income_value >= 45000) &
        (income_value < 150000)]
    high_income = df[income_value >= 150000]

    # line ploting
    plt.figure()
    sns.lineplot(data=poverty, x='YEAR', y='INCOME', hue='RACE', ci=None)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title('Poverty by Race')
    plt.savefig('poverty_race_line.png')

    plt.figure()
    sns.lineplot(data=low_income, x='YEAR', y='INCOME', hue='RACE', ci=None)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title('Low Income by Race')
    plt.savefig('low_income_race_line.png')

    plt.figure()
    sns.lineplot(data=middle_class, x='YEAR', y='INCOME', hue='RACE', ci=None)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title('Middle Class by Race')
    plt.savefig('middle_class_race_line.png')

    plt.figure()
    sns.lineplot(data=high_income, x='YEAR', y='INCOME', hue='RACE', ci=None)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title('High Income by Race')
    plt.savefig('high_income_race_line.png')


def housing_line_plots(df):
    '''
    Will takes the given Dataframe format and will plot a line chart with race
    category. Will save the plot in png format.
    '''
    plt.figure()
    sns.lineplot(data=df, x='YEAR', y='COSTS', hue='RACE', ci=None)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title('Housing Cost by Race')
    plt.savefig('housing_race_line.png')


def main():
    '''
    Will use the raw data of Housing Burden and turn it into a Dataframe format
    The main function will first do the percentage calculation of the missing
    data. Then will filtering the Dataframe by getting rid of NA value and
    remove the rows that contain string 'All' in the race column. Then the
    Dataframe will pass down into the two functions that would create five
    lines plots.
    '''
    burden_data = pd.read_csv(
        '~/Desktop/CSE/CSE 163/project/part 2/Task 4/' +
        'Burden.csv')

    get_percent = percentage_missing_data(burden_data)
    print('Missing Data: ' + str(get_percent) + "%")

    # filtering to get rid of NA
    burden_data = burden_data[burden_data['INCOME'].notna()]
    burden_data = burden_data[burden_data['RACE'] != 'All']

    # ploting functions
    income_line_plots(burden_data)
    housing_line_plots(burden_data)


if __name__ == '__main__':
    main()
