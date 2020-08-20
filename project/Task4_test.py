#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 10:59:45 2020

@author: Jin Ning Huang
CSE 163 SUMMER 2020

This file contains the testcases for Task 4 to ensure that data values are
correct. This will be testing for non-plots.

NOTE: I am using local file, so please change the desirable filepath for your
computer.
"""

import pandas as pd
from cse163_utils import assert_equals
from Task4_line_plots_only import percentage_missing_data


def burden_race_test(burden_data):
    '''
    Tests the section where the data focus in race factors
    '''
    assert_equals(5.18, percentage_missing_data(burden_data))
    assert_equals(4212, len(burden_data))

    filtered_race__burden = burden_data = burden_data[burden_data['INCOME'].
                                                      notna()]
    filtered_race__burden = filtered_race__burden[burden_data['RACE']
                                                  != 'All']

    assert_equals(3292, len(filtered_race__burden))
    assert_equals(5, len(filtered_race__burden['RACE'].unique()))

    income_value = filtered_race__burden['INCOME']

    poverty = filtered_race__burden[income_value < 20000]
    low_income = filtered_race__burden[(income_value >= 20000) &
                                       (income_value < 45000)]
    middle_class = filtered_race__burden[(
        income_value >= 45000) &
        (income_value < 150000)]
    high_income = filtered_race__burden[income_value >= 150000]

    assert_equals(516, len(poverty))
    assert_equals(714, len(low_income))
    assert_equals(1644, len(middle_class))
    assert_equals(418, len(high_income))


def burden_finance_test(burden_data):
    '''
    Tests the section where the data focus in finance factors
    '''
    burden_data = burden_data[burden_data['INCOME'].notna()]

    assert_equals(3994, len(burden_data))

    # filtering the income level
    income_value = burden_data['INCOME']

    # testing for income level only
    poverty = burden_data[income_value < 20000]
    low_income = burden_data[(income_value >= 20000) & (income_value < 45000)]
    middle_class = burden_data[(income_value >= 45000) &
                               (income_value < 140000)]
    upper_middle = burden_data[(income_value >= 140000) &
                               (income_value < 150000)]
    high_income = burden_data[(
        income_value >= 150000) &
        (income_value < 200000)]
    highest_tax = burden_data[(income_value >= 200000)]

    # the dataset
    assert_equals(633, len(poverty))
    assert_equals(855, len(low_income))
    assert_equals(1909, len(middle_class))
    assert_equals(78, len(upper_middle))
    assert_equals(361, len(high_income))
    assert_equals(158, len(highest_tax))

    # groupby year for each income level
    poverty_report = poverty.groupby('YEAR')['INCOME'].mean()
    low_income_report = low_income.groupby('YEAR')['INCOME'].mean()
    middle_class_report = middle_class.groupby('YEAR')['INCOME'].mean()
    upper_middle_report = upper_middle.groupby('YEAR')['INCOME'].mean()
    high_income_report = high_income.groupby('YEAR')['INCOME'].mean()
    highest_tax_report = highest_tax.groupby('YEAR')['INCOME'].mean()

    # using the max to check if the data is correct when comparing with the
    # visual plots
    assert_equals(14900.89834870455, poverty_report.max())
    assert_equals(2017, poverty_report.idxmax())

    assert_equals(34429.92969144941, low_income_report.max())
    assert_equals(2013, low_income_report.idxmax())

    assert_equals(79023.09430172438, middle_class_report.max())
    assert_equals(2017, middle_class_report.idxmax())

    assert_equals(147061.450347868, upper_middle_report.max())
    assert_equals(2008, upper_middle_report.idxmax())

    assert_equals(182074.8215933717, high_income_report.max())
    assert_equals(2014, high_income_report.idxmax())

    assert_equals(267469.361277445, highest_tax_report.max())
    assert_equals(2006, highest_tax_report.idxmax())

    # testing for houseing cost only
    housing_cost = burden_data.groupby('YEAR')['COSTS'].mean()
    assert_equals(13, len(housing_cost))
    assert_equals(2011, housing_cost.idxmax())
    assert_equals(1816.2050424440188, housing_cost.max())


def main():
    '''
    All the testing cases for entire Task 4, mostly to check the the dataset
    length and values
    '''

    burden_data = pd.read_csv(
        '~/Desktop/CSE/CSE 163/project/part 2/Task 4/' +
        'Burden.csv')

    burden_race_test(burden_data)
    burden_finance_test(burden_data)


if __name__ == '__main__':
    main()
